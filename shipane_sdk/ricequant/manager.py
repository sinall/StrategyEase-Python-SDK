# -*- coding: utf-8 -*-

# Begin of __future__ module
# End   of __future__ module

# Begin of external module
# End   of external module

import traceback

from shipane_sdk.base_manager import *
from shipane_sdk.models import *


class RiceQuantStrategyManagerFactory(BaseStrategyManagerFactory):
    def __init__(self, context):
        self._strategy_context = RiceQuantStrategyContext(context)
        super(RiceQuantStrategyManagerFactory, self).__init__()

    def _get_context(self):
        return self._strategy_context

    def _create_logger(self):
        return RiceQuantLogger()


class RiceQuantStrategyContext(BaseStrategyContext):
    def __init__(self, context):
        self._context = context

    def get_current_time(self):
        return self._context.now

    def get_portfolio(self):
        quant_portfolio = self._context.portfolio
        portfolio = Portfolio()
        portfolio.available_cash = quant_portfolio.cash
        portfolio.total_value = quant_portfolio.total_value
        positions = dict()
        for order_book_id, quant_position in quant_portfolio.positions.items():
            position = self._convert_position(quant_position)
            positions[position.security] = position
        portfolio.positions = positions
        return portfolio

    def convert_order(self, quant_order):
        status = {
            ORDER_STATUS.PENDING_NEW: OrderStatus.open,
            ORDER_STATUS.ACTIVE: OrderStatus.open,
            ORDER_STATUS.FILLED: OrderStatus.filled,
            ORDER_STATUS.CANCELLED: OrderStatus.canceled,
            ORDER_STATUS.REJECTED: OrderStatus.rejected,
        }.get(quant_order.ORDER_STATUS)
        common_order = Order(
            id=quant_order.order_id,
            action=(OrderAction.OPEN if quant_order.side == SIDE.BUY else OrderAction.CLOSE),
            security=quant_order.order_book_id,
            price=quant_order.price,
            amount=quant_order.quantity,
            style=(OrderStyle.LIMIT if quant_order.price > 0 else OrderStyle.MARKET),
            status=status,
            add_time=quant_order.datetime,
        )
        return common_order

    def get_orders(self):
        pass

    def has_open_orders(self):
        return bool(get_open_orders())

    def cancel_open_orders(self):
        open_orders = get_open_orders()
        for open_order in open_orders.values():
            self.cancel_order(open_order)

    def cancel_order(self, open_order):
        return cancel_order(open_order)

    def read_file(self, path):
        return get_file(path)

    def is_sim_trade(self):
        return self._context.run_info.run_type == RUN_TYPE.PAPER_TRADING

    def is_backtest(self):
        return not self.is_sim_trade()

    def is_read_file_allowed(self):
        return False

    @staticmethod
    def _convert_position(quant_position):
        position = Position()
        position.security = quant_position.order_book_id
        position.price = quant_position.avg_price
        position.total_amount = quant_position.quantity
        position.closeable_amount = quant_position.sellable
        position.value = quant_position.market_value
        return position


class RiceQuantLogger(BaseLogger):
    def debug(self, msg, *args, **kwargs):
        if not args:
            logger.debug(msg)
        else:
            logger.debug(msg % args)

    def info(self, msg, *args, **kwargs):
        if not args:
            logger.info(msg)
        else:
            logger.info(msg % args)

    def warning(self, msg, *args, **kwargs):
        if not args:
            logger.warning(msg)
        else:
            logger.warning(msg % args)

    def error(self, msg, *args, **kwargs):
        if not args:
            logger.error(msg)
        else:
            logger.error(msg % args)

    def exception(self, msg, *args, **kwargs):
        msg += "\n%s"
        args += (traceback.format_exc(),)
        logger.error(msg % args)
