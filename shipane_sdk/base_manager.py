# -*- coding: utf-8 -*-

import time

import tushare as ts

from shipane_sdk.client import *
from shipane_sdk.models import *
from shipane_sdk.support import *


class BaseStrategyManagerFactory(object):
    def __init__(self):
        self._config = self._create_config()

    def create(self, id):
        traders = self._create_traders(id)
        return StrategyManager(id, self._create_logger(), self._config, traders, self._get_context())

    def _get_context(self):
        pass

    def _create_traders(self, id):
        traders = OrderedDict()
        for trader_id, trader_config in self._config.build_trader_configs(id).items():
            trader = self._create_trader(trader_config)
            traders[trader_id] = trader
        return traders

    def _create_trader(self, trader_config):
        return StrategyTrader(self._create_logger(), trader_config, self._get_context())

    def _create_logger(self):
        pass

    def _create_config(self):
        return StrategyConfig(self._get_context())


class BaseStrategyContext(object):
    def get_portfolio(self):
        pass

    def convert_order(self, quant_order):
        pass

    def has_open_orders(self):
        pass

    def cancel_open_orders(self):
        pass

    def cancel_order(self, quant_order):
        pass

    def read_file(self, path):
        pass

    def is_sim_trade(self):
        pass

    def is_backtest(self):
        pass

    def is_read_file_allowed(self):
        return False


class BaseLogger(object):
    def debug(self, msg, *args, **kwargs):
        pass

    def info(self, msg, *args, **kwargs):
        pass

    def warning(self, msg, *args, **kwargs):
        pass

    def error(self, msg, *args, **kwargs):
        pass

    def exception(self, msg, *args, **kwargs):
        pass


class StrategyManager(object):
    THEMATIC_BREAK = '-' * 50

    def __init__(self, id, logger, config, traders, strategy_context):
        self._id = id
        self._logger = logger
        self._config = config
        self._traders = traders
        self._strategy_context = strategy_context

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

    def repo(self):
        security = '131810'
        quote_df = ts.get_realtime_quotes(security)
        order = {
            'action': 'SELL',
            'symbol': security,
            'type': 'LIMIT',
            'price': float(quote_df['bid'][0]),
            'amountProportion': 'ALL'
        }
        for trader in self._traders.values():
            try:
                trader.execute(**order)
            except:
                self._logger.exception('[%s] 逆回购失败', trader.id)

    def execute(self, order=None, **kwargs):
        if order is None and not kwargs:
            return
        for trader in self._traders.values():
            try:
                trader.execute(order, **kwargs)
            except:
                self._logger.exception('[%s] 下单失败', trader.id)

    def cancel(self, order):
        for trader in self._traders.values():
            try:
                trader.cancel(order)
            except:
                self._logger.exception('[%s] 撤单失败', trader.id)

    def work(self):
        stop_watch = StopWatch()
        stop_watch.start()
        self._logger.info("[%s] 开始工作", self._id)
        self._refresh()
        for id, trader in self._traders.items():
            trader.work()
        stop_watch.stop()
        self._logger.info("[%s] 结束工作，总耗时[%s]", self._id, stop_watch.short_summary())
        self._logger.info(self.THEMATIC_BREAK)

    def _refresh(self):
        if not self._strategy_context.is_read_file_allowed():
            return
        self._config.reload()
        trader_configs = self._config.build_trader_configs(self._id)
        for id, trader in self._traders.items():
            trader.set_config(trader_configs[id])


class StrategyTrader(object):
    def __init__(self, logger, config, strategy_context):
        self._logger = logger
        self._config = config
        self._strategy_context = strategy_context
        self._shipane_client = Client(self._logger, **config['client'])
        self._order_id_to_info_map = {}
        self._expire_before = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
        self._last_sync_portfolio_fingerprint = None

    @property
    def id(self):
        return self._config['id']

    @property
    def client(self):
        return self._shipane_client

    def set_config(self, config):
        self._config = config

    def purchase_new_stocks(self):
        if not self._pre_check():
            return

        self._shipane_client.purchase_new_stocks()

    def execute(self, order=None, **kwargs):
        if not self._pre_check():
            return

        if order is None:
            common_order = Order.from_e_order(**kwargs)
        else:
            common_order = self._normalize_order(order)

        try:
            actual_order = self._execute(common_order)
            return actual_order
        except Exception:
            self._logger.exception("[实盘易] 下单异常")

    def cancel(self, order):
        if not self._pre_check():
            return

        try:
            self._cancel(order)
        except:
            self._logger.exception("[实盘易] 撤单异常")

    def work(self):
        if not self._pre_check():
            return

        if self._config['mode'] == 'SYNC':
            self._sync()
        else:
            self._follow()

    def _sync(self):
        stop_watch = StopWatch()
        stop_watch.start()
        self._logger.info("[%s] 开始同步", self.id)
        try:
            if self._sync_config['pre-clear-for-sim']:
                self._cancel_all_for_sim()
                self._logger.info("[%s] 模拟盘撤销全部订单已完成", self.id)
            target_portfolio = self._strategy_context.get_portfolio()
            if self._should_sync(target_portfolio):
                if self._sync_config['pre-clear-for-live'] and not self._config['dry-run']:
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

    def _follow(self):
        stop_watch = StopWatch()
        stop_watch.start()
        self._logger.info("[%s] 开始跟单", self.id)
        try:
            common_orders = []
            all_common_orders = self._strategy_context.get_orders()
            for common_order in all_common_orders:
                if common_order.add_time >= self._strategy_context.get_current_time():
                    if common_order.status == OrderStatus.canceled:
                        origin_order = copy.deepcopy(common_order)
                        origin_order.status = OrderStatus.open
                        common_orders.append(origin_order)
                    else:
                        common_orders.append(common_order)
                if common_order.status == OrderStatus.canceled:
                    common_orders.append(common_order)

            common_orders = sorted(common_orders, key=lambda o: _PrioritizedOrder(o))
            for common_order in common_orders:
                if common_order.status != OrderStatus.canceled:
                    try:
                        self._execute(common_order)
                    except:
                        self._logger.exception("[实盘易] 下单异常")
                else:
                    try:
                        self._cancel(common_order)
                    except:
                        self._logger.exception("[实盘易] 撤单异常")
        except:
            self._logger.exception("[%s] 跟单失败", self.id)
        stop_watch.stop()
        self._logger.info("[%s] 结束跟单，耗时[%s]", self.id, stop_watch.short_summary())

    @property
    def _sync_config(self):
        return self._config['sync']

    def _execute(self, order):
        if not self._should_run():
            self._logger.info("[%s] %s", self.id, order)
            return None
        actual_order = self._do_execute(order)
        return actual_order

    def _cancel(self, order):
        if not self._should_run():
            self._logger.info("[%s] 撤单 [%s]", self.id, order)
            return
        self._do_cancel(order)

    def _do_execute(self, order):
        common_order = self._normalize_order(order)
        e_order = common_order.to_e_order()
        actual_order = self._shipane_client.execute(**e_order)
        self._order_id_to_info_map[common_order.id] = {'id': actual_order['id'], 'canceled': False}
        return actual_order

    def _do_cancel(self, order):
        if order is None:
            self._logger.info('[实盘易] 委托为空，忽略撤单请求')
            return

        if isinstance(order, int):
            quant_order_id = order
        else:
            common_order = self._normalize_order(order)
            quant_order_id = common_order.id

        try:
            order_info = self._order_id_to_info_map[quant_order_id]
            if not order_info['canceled']:
                order_info['canceled'] = True
                self._shipane_client.cancel(order_id=order_info['id'])
        except KeyError:
            self._logger.warning('[实盘易] 未找到对应的委托编号')
            self._order_id_to_info_map[quant_order_id] = {'id': None, 'canceled': True}

    def _normalize_order(self, order):
        if isinstance(order, Order):
            common_order = order
        else:
            common_order = self._strategy_context.convert_order(order)
        return common_order

    def _should_run(self):
        if self._config['dry-run']:
            self._logger.debug("[实盘易] 当前为排练模式，不执行下单、撤单请求")
            return False
        return True

    def _is_expired(self, common_order):
        return common_order.add_time < self._expire_before

    def _pre_check(self):
        if not self._config['enabled']:
            self._logger.info("[%s] 交易未启用，不执行", self.id)
            return False
        if self._strategy_context.is_backtest():
            self._logger.info("[%s] 当前为回测环境，不执行", self.id)
            return False
        return True

    def _should_sync(self, target_portfolio):
        if self._strategy_context.has_open_orders():
            self._logger.info("[%s] 有未完成订单，不进行同步", self.id)
            return False
        is_changed = target_portfolio.fingerprint != self._last_sync_portfolio_fingerprint
        if not is_changed:
            self._logger.info("[%s] 模拟持仓未改变，不进行同步", self.id)
        return is_changed

    def _cancel_all_for_sim(self):
        self._strategy_context.cancel_open_orders()

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
        context = AdjustmentContext(self._sync_config['other-value'],
                                    self._sync_config['total-value-deviation-rate'],
                                    self._sync_config['reserved-securities'],
                                    self._sync_config['min-order-value'],
                                    self._sync_config['max-order-value'])
        request = Adjustment()
        request.target_portfolio = target_portfolio
        request.context = context
        return request

    def _log_progress(self, adjustment):
        self._logger.info("[%s] %s", self.id, adjustment.progress)

    def _execute_adjustment(self, adjustment):
        for batch in adjustment.batches:
            for order in batch:
                self._execute(order)
                time.sleep(self._sync_config['order-interval'] / 1000.0)
            time.sleep(self._sync_config['batch-interval'] / 1000.0)


class StrategyConfig(object):
    def __init__(self, strategy_context):
        self._strategy_context = strategy_context
        self._data = dict()
        self.reload()

    @property
    def data(self):
        return self._data

    def reload(self):
        content = self._strategy_context.read_file('shipane_sdk_config.yaml')
        stream = six.BytesIO(content)
        self._data = yaml.load(stream, Loader=OrderedDictYAMLLoader)
        self._proxies = self._create_proxy_configs()
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

    def _create_proxy_configs(self):
        proxies = {}
        for raw_proxy_config in self._data['proxies']:
            id = raw_proxy_config['id']
            proxies[id] = raw_proxy_config
        return proxies

    def _create_trader_config(self, raw_trader_config):
        client_config = self._create_client_config(raw_trader_config)
        trader_config = copy.deepcopy(raw_trader_config)
        trader_config['client'] = client_config
        if 'sync' in trader_config:
            trader_config['sync']['reserved-securities'] = client_config.pop('reserved_securities', [])
            trader_config['sync']['other-value'] = client_config.pop('other_value', [])
            trader_config['sync']['total-value-deviation-rate'] = client_config.pop('total_value_deviation_rate', [])
        return trader_config

    def _create_client_config(self, raw_trader_config):
        client_config = None
        for raw_gateway_config in self._data['gateways']:
            for raw_client_config in raw_gateway_config['clients']:
                if raw_client_config['id'] == raw_trader_config['client']:
                    connection_method = raw_gateway_config['connection-method']
                    client_config = {
                        'connection_method': connection_method,
                        'key': raw_gateway_config['key'],
                        'timeout': tuple([
                            raw_gateway_config['timeout']['connect'],
                            raw_gateway_config['timeout']['read'],
                        ]),
                        'client': raw_client_config['query'],
                        'reserved_securities': raw_client_config['reserved-securities'],
                        'other_value': raw_client_config['other-value'],
                        'total_value_deviation_rate': raw_client_config['total-value-deviation-rate'],
                    }
                    if connection_method == 'DIRECT':
                        client_config.update({
                            'host': raw_gateway_config['host'],
                            'port': raw_gateway_config['port'],
                        })
                    else:
                        proxy_config = self._proxies[raw_gateway_config['proxy']]
                        client_config.update({
                            'proxy_base_url': proxy_config['base-url'],
                            'proxy_username': proxy_config['username'],
                            'proxy_password': proxy_config['password'],
                            'instance_id': raw_gateway_config['instance-id'],
                        })
                    break
                if client_config is not None:
                    break
        return client_config


class _PrioritizedOrder(object):
    def __init__(self, order):
        self.order = order

    def __lt__(self, other):
        x = self.order
        y = other.order
        if x.add_time != y.add_time:
            return x.add_time < y.add_time
        if x.status == OrderStatus.canceled:
            if y.status == OrderStatus.canceled:
                return x.id < y.id
            else:
                return False
        else:
            if y.status == OrderStatus.canceled:
                return True
            else:
                return x.id < y.id

    def __gt__(self, other):
        return other.__lt__(self)

    def __eq__(self, other):
        return (not self.__lt__(other)) and (not other.__lt__(self))

    def __le__(self, other):
        return not self.__gt__(other)

    def __ge__(self, other):
        return not self.__lt__(other)

    def __ne__(self, other):
        return not self.__eq__(other)
