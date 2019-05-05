# -*- coding: utf-8 -*-

# Begin of __future__ module
# End   of __future__ module

# Begin of external module
# End   of external module

import traceback

from kuanke.user_space_api import *

from strategyease_sdk.base_manager import *
from strategyease_sdk.models import *


class JoinQuantStrategyManagerFactory(BaseStrategyManagerFactory):
    def __init__(self, context):
        self._strategy_context = JoinQuantStrategyContext(context)
        super(JoinQuantStrategyManagerFactory, self).__init__()

    def _get_context(self):
        return self._strategy_context

    def _create_logger(self):
        return JoinQuantLogger()


class JoinQuantStrategyContext(BaseStrategyContext):
    def __init__(self, context):
        self._context = context

    def get_current_time(self):
        return self._context.current_dt

    def get_portfolio(self):
        quant_portfolio = self._context.portfolio
        portfolio = Portfolio()
        portfolio.available_cash = quant_portfolio.available_cash
        portfolio.total_value = quant_portfolio.total_value
        positions = dict()
        for security, quant_position in quant_portfolio.positions.items():
            position = self._convert_position(quant_position)
            positions[position.security] = position
        portfolio.positions = positions
        return portfolio

    def convert_order(self, quant_order):
        common_order = Order(
            id=quant_order.order_id,
            action=(OrderAction.OPEN if quant_order.is_buy else OrderAction.CLOSE),
            security=quant_order.security,
            price=quant_order.limit,
            amount=quant_order.amount,
            style=(OrderStyle.LIMIT if quant_order.limit > 0 else OrderStyle.MARKET),
            status=self._convert_status(quant_order.status),
            add_time=quant_order.add_time,
        )
        return common_order

    def get_orders(self):
        orders = get_orders()
        common_orders = []
        for order in orders.values():
            common_order = self.convert_order(order)
            common_orders.append(common_order)
        return common_orders

    def has_open_orders(self):
        return bool(get_open_orders())

    def cancel_open_orders(self):
        open_orders = get_open_orders()
        for open_order in open_orders.values():
            self.cancel_order(open_order)

    def cancel_order(self, open_order):
        return cancel_order(open_order)

    def read_file(self, path):
        return read_file(path)

    def is_sim_trade(self):
        return self._context.run_params.type == 'sim_trade'

    def is_backtest(self):
        return not self.is_sim_trade()

    def is_read_file_allowed(self):
        return True

    @staticmethod
    def _convert_position(quant_position):
        position = Position()
        position.security = quant_position.security
        position.price = quant_position.price
        position.total_amount = quant_position.total_amount + quant_position.locked_amount
        position.closeable_amount = quant_position.closeable_amount
        position.value = quant_position.value
        return position

    @staticmethod
    def _convert_status(quant_order_status):
        try:
            return OrderStatus(quant_order_status.value)
        except ValueError:
            return OrderStatus.open


class JoinQuantLogger(BaseLogger):
    def debug(self, msg, *args, **kwargs):
        log.debug(msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        log.info(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        log.warn(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        log.error(msg, *args, **kwargs)

    def exception(self, msg, *args, **kwargs):
        msg += "\n%s"
        args += (traceback.format_exc(),)
        log.error(msg, *args, **kwargs)
