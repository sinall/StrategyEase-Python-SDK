# -*- coding: utf-8 -*-

# Begin of __future__ module
# End   of __future__ module

import time
import traceback

from kuanke.user_space_api import *

from shipane_sdk.client import *
from shipane_sdk.models import *
from shipane_sdk.support import *


class StrategyManager(object):
    THEMATIC_BREAK = '-' * 50

    def __init__(self, context, id):
        self._logger = _Infra.create_logger(__name__)
        self._id = id
        self._config = _Config()
        self._traders = OrderedDict()
        for trader_id, trader_config in self._config.build_trader_configs(self._id).items():
            trader = StrategyTrader(trader_config)
            self._traders[trader_id] = trader

    @property
    def id(self):
        return self._id

    @property
    def traders(self):
        return self._traders

    def purchase_new_stocks(self):
        for trader in self._traders.values():
            try:
                trader.purchase_new_stocks()
            except:
                self._logger.exception('[%s] 打新失败', trader.id)

    def execute(self, order):
        for trader in self._traders.values():
            try:
                trader.execute(order)
            except:
                self._logger.exception('[%s] 下单失败', trader.id)

    def cancel(self, order):
        for trader in self._traders.values():
            try:
                trader.cancel(order)
            except:
                self._logger.exception('[%s] 撤单失败', trader.id)

    def sync(self, context):
        stop_watch = StopWatch()
        stop_watch.start()
        self._logger.info("[%s] 开始同步", self._id)
        self._refresh()
        for id, trader in self._traders.items():
            trader.sync(context)
        stop_watch.stop()
        self._logger.info("[%s] 结束同步，总耗时[%s]", self._id, stop_watch.short_summary())
        self._logger.info(self.THEMATIC_BREAK)

    def _refresh(self):
        self._config.reload()
        trader_configs = self._config.build_trader_configs(self._id)
        for id, trader in self._traders.items():
            trader.set_config(trader_configs[id])


class StrategyTrader(object):
    def __init__(self, config):
        self._logger = _Infra.create_logger(__name__)
        self._config = config
        self._shipane_client = Client(self._logger, **config['client'])
        self._order_id_map = {}
        self._expire_before = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
        self._last_sync_portfolio_fingerprint = {}

    @property
    def id(self):
        return self._config['id']

    @property
    def client(self):
        return self._shipane_client

    def set_config(self, config):
        self._config = config

    def purchase_new_stocks(self):
        self._shipane_client.purchase_new_stocks()

    def execute(self, order):
        self._logger.info("[实盘易] 跟单：" + str(order))

        if not self._should_execute(order):
            return

        try:
            e_order = self._convert_order(order)
            actual_order = self._shipane_client.execute(**e_order)
            self._order_id_map[order.order_id] = actual_order['id']
            return actual_order
        except:
            self._logger.exception("[实盘易] 下单异常")

    def cancel(self, order):
        if order is None:
            self._logger.info('[实盘易] 委托为空，忽略撤单请求')
            return

        try:
            order_id = order if isinstance(order, int) else order.order_id
            if order_id in self._order_id_map:
                self._shipane_client.cancel(order_id=self._order_id_map[order_id])
            else:
                self._logger.warning('[实盘易] 未找到对应的委托编号')
        except:
            self._logger.exception("[实盘易] 撤单异常")

    def sync(self, context):
        stop_watch = StopWatch()
        stop_watch.start()
        self._logger.info("[%s] 开始同步", self.id)
        try:
            if self._sync_config['pre-clear-for-sim']:
                self._cancel_all_for_sim()
                self._logger.info("[%s] 模拟盘撤销全部订单已完成", self.id)
            target_portfolio = self._convert_portfolio(context.portfolio)
            if self._should_sync(context, target_portfolio):
                if self._sync_config['pre-clear-for-live'] and not self._sync_config['debug']:
                    self._shipane_client.cancel_all()
                    time.sleep(self._sync_config['order-interval'] / 1000.0)
                    self._logger.info("[%s] 实盘撤销全部订单已完成", self.id)

                is_sync = False
                for i in range(0, 2 + self._sync_config['extra-rounds']):
                    self._logger.info("[%s] 开始第[%d]轮同步", self.id, i + 1)
                    is_sync = self._sync_once(target_portfolio)
                    self._logger.info("[%s] 结束第[%d]轮同步", self.id, i + 1)
                    if is_sync:
                        self._last_sync_portfolio_fingerprint = target_portfolio.fingerprint
                        self._logger.info("[%s] 实盘已与模拟盘同步", self.id)
                        break
                    time.sleep(self._sync_config['round-interval'] / 1000.0)
                self._logger.info(u"[%s] 结束同步，状态：%s", self.id, "已完成" if is_sync else "未完成")
        except:
            self._logger.exception("[%s] 同步失败", self.id)
        stop_watch.stop()
        self._logger.info("[%s] 结束同步，耗时[%s]", self.id, stop_watch.short_summary())

    @property
    def _sync_config(self):
        return self._config['sync']

    def _should_execute(self, order):
        if order is None:
            self._logger.info('[实盘易] 委托为空，忽略下单请求')
            return False
        if self._is_expired(order):
            self._logger.info('[实盘易] 委托已过期，忽略下单请求')
            return False
        return True

    def _is_expired(self, order):
        return order.add_time < self._expire_before

    def _should_sync(self, context, target_portfolio):
        if not self._sync_config['enabled']:
            self._logger.info("[%s] 同步未启用，不进行同步", self.id)
            return False
        if _Infra.get_open_orders():
            self._logger.info("[%s] 有未完成订单，不进行同步", self.id)
            return False
        is_changed = target_portfolio.fingerprint != self._last_sync_portfolio_fingerprint
        if not is_changed:
            self._logger.info("[%s] 模拟持仓未改变，不进行同步", self.id)
        return is_changed

    def _cancel_all_for_sim(self):
        orders = _Infra.get_open_orders()
        for _order in orders.values():
            _Infra.cancel_order(_order)

    def _sync_once(self, target_portfolio):
        adjustment = self._create_adjustment(target_portfolio)
        self._log_progress(adjustment)
        self._execute_adjustment(adjustment)
        is_sync = adjustment.empty()
        return is_sync

    def _create_adjustment(self, target_portfolio):
        request = self._create_adjustment_request(target_portfolio)
        request_json = Adjustment.to_json(request)
        response_json = self._shipane_client.create_adjustment(request_json=request_json)
        adjustment = Adjustment.from_json(response_json)
        return adjustment

    def _create_adjustment_request(self, target_portfolio):
        context = AdjustmentContext(self._sync_config['reserved-securities'],
                                    self._sync_config['min-order-value'],
                                    self._sync_config['max-order-value'])
        request = Adjustment()
        request.target_portfolio = target_portfolio
        request.context = context
        return request

    def _convert_order(self, quant_order):
        order_type = 'LIMIT' if quant_order.limit > 0 else 'MARKET'
        e_order = dict(
            action=('BUY' if quant_order.is_buy else 'SELL'),
            symbol=quant_order.security,
            type=order_type,
            priceType=(0 if order_type == 'LIMIT' else 4),
            price=quant_order.limit,
            amount=quant_order.amount
        )
        return e_order

    def _convert_portfolio(self, quant_portfolio):
        portfolio = Portfolio()
        portfolio.available_cash = quant_portfolio.available_cash
        portfolio.total_value = quant_portfolio.total_value
        positions = dict()
        for security, quant_position in quant_portfolio.positions.items():
            position = self._convert_position(quant_position)
            positions[position.security] = position
        portfolio.positions = positions
        return portfolio

    def _convert_position(self, quant_position):
        position = Position()
        position.security = quant_position.security
        position.price = quant_position.price
        position.total_amount = quant_position.total_amount + quant_position.locked_amount
        position.closeable_amount = quant_position.closeable_amount
        position.value = quant_position.value
        return position

    def _log_progress(self, adjustment):
        self._logger.info("[%s] %s", self.id, adjustment.progress)

    def _execute_adjustment(self, adjustment):
        for batch in adjustment.batches:
            for order in batch:
                self._execute_order(order)
                time.sleep(self._sync_config['order-interval'] / 1000.0)
            time.sleep(self._sync_config['batch-interval'] / 1000.0)

    def _execute_order(self, order):
        try:
            if self._sync_config['debug']:
                self._logger.info("[%s] %s", self.id, order)
                return

            e_order = order.to_e_order()
            e_order['type'] = 'MARKET'
            e_order['priceType'] = 4
            self._shipane_client.execute(**e_order)
        except:
            self._logger.exception("[%s] 客户端下单失败", self.id)


class _Config(object):
    def __init__(self):
        self._data = dict()
        self.reload()

    @property
    def data(self):
        return self._data

    def reload(self):
        content = _Infra.read_file('shipane_sdk_config.yaml')
        stream = six.StringIO(content)
        self._data = yaml.load(stream, Loader=OrderedDictYAMLLoader)
        stream.close()

    def build_trader_configs(self, id):
        trader_configs = OrderedDict()
        for raw_manager_config in self._data['managers']:
            if raw_manager_config['id'] == id:
                for raw_trader_config in raw_manager_config['traders']:
                    trader_config = self._create_trader_config(raw_trader_config)
                    trader_configs[raw_trader_config['id']] = trader_config
                break
        return trader_configs

    def _create_trader_config(self, raw_trader_config):
        client_config = self._create_client_config(raw_trader_config)
        sync_config = raw_trader_config['sync']
        sync_config['reserved-securities'] = client_config['reserved-securities']
        result = {
            'id': raw_trader_config['id'],
            'client': client_config,
            'sync': sync_config
        }
        return result

    def _create_client_config(self, raw_trader_config):
        client_config = None
        for raw_gateway_config in self._data['gateways']:
            for raw_client_config in raw_gateway_config['clients']:
                if raw_client_config['id'] == raw_trader_config['client']:
                    client_config = copy.deepcopy(raw_gateway_config)
                    client_config.update(raw_client_config)
                    client_config['client'] = raw_client_config['query']
                    client_config['timeout'] = tuple([
                        raw_gateway_config['timeout']['connect'],
                        raw_gateway_config['timeout']['read']
                    ])
                    del client_config['clients']
                    break
                if client_config is not None:
                    break
        return client_config


class _Infra(object):
    @staticmethod
    def create_logger(name=None):
        try:
            log
            return _Logger()
        except NameError:
            import logging
            return logging.getLogger(name)

    @staticmethod
    def is_sim_trade(context):
        return context.run_params.type == 'sim_trade'

    @staticmethod
    def is_backtest(context):
        return not _Infra.is_sim_trade(context)

    @staticmethod
    def read_file(path):
        return read_file(path)

    @staticmethod
    def get_open_orders():
        return get_open_orders()

    @staticmethod
    def cancel_order(order):
        return cancel_order(order)

    @staticmethod
    def get_trades():
        return get_trades()


class _Logger(object):
    def debug(self, msg, *args, **kwargs):
        log.debug(msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        log.info(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        log.warn(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        log.error(msg, *args, **kwargs)

    def exception(self, msg, *args, **kwargs):
        msg = u"{}\n{}".format(msg, traceback.format_exc())
        log.error(msg, *args, **kwargs)
