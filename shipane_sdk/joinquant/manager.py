# -*- coding: utf-8 -*-

# Begin of __future__ module
# End   of __future__ module

# Begin of external module
# End   of external module

import traceback

from kuanke.user_space_api import *

from shipane_sdk.base_manager import *
from shipane_sdk.models import *


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

    @staticmethod
    def _convert_position(quant_position):
        position = Position()
        position.security = quant_position.security
        position.price = quant_position.price
        position.total_amount = quant_position.total_amount + quant_position.locked_amount
        position.closeable_amount = quant_position.closeable_amount
        position.value = quant_position.value
        return position


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
