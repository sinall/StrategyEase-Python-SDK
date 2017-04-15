# -*- coding: utf-8 -*-

from __future__ import division

from enum import Enum


class AdjustmentRequest(object):
    @staticmethod
    def to_json(instance):
        json = {
            'targetPortfolio': Portfolio.to_json(instance.target_portfolio),
            'context': AdjustmentContext.to_json(instance.context)
        }
        return json

    def __init__(self, target_portfolio, context):
        self._target_portfolio = target_portfolio
        self._context = context

    @property
    def target_portfolio(self):
        return self._target_portfolio

    @target_portfolio.setter
    def target_portfolio(self, value):
        self._target_portfolio = value

    @property
    def context(self):
        return self._context

    @context.setter
    def context(self, value):
        self._context = value


class AdjustmentContext(object):
    @staticmethod
    def to_json(instance):
        json = {
            'minOrderValue': instance.min_order_value,
            'maxOrderValue': instance.max_order_value,
            'reservedSecurities': instance.reserved_securities,
        }
        return json

    def __init__(self, reserved_securities, min_order_value, max_order_value):
        self._reserved_securities = reserved_securities
        self._min_order_value = min_order_value
        self._max_order_value = max_order_value

    @property
    def reserved_securities(self):
        return self._reserved_securities

    @reserved_securities.setter
    def reserved_securities(self, value):
        self._reserved_securities = value

    @property
    def min_order_value(self):
        return self._min_order_value

    @min_order_value.setter
    def min_order_value(self, value):
        self._min_order_value = value

    @property
    def max_order_value(self):
        return self._max_order_value

    @max_order_value.setter
    def max_order_value(self, value):
        self._max_order_value = value


class Adjustment(object):
    @classmethod
    def from_json(cls, json):
        instance = Adjustment()
        instance.id = json.get('id', None)
        instance.status = json.get('status', None)
        batches = []
        for batch_json in json['batches']:
            batch = []
            for order_json in batch_json:
                batch.append(Order.from_json(order_json))
            batches.append(batch)
        instance.batches = batches
        progress_json = json['progress']
        instance._today_progress = AdjustmentProgress.from_json(progress_json['today'])
        instance._overall_progress = AdjustmentProgress.from_json(progress_json['overall'])
        return instance

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._status = value

    @property
    def batches(self):
        return self._batches

    @batches.setter
    def batches(self, value):
        self._batches = value

    @property
    def today_progress(self):
        return self._today_progress

    @today_progress.setter
    def today_progress(self, value):
        self._today_progress = value

    @property
    def overall_progress(self):
        return self._overall_progress

    @overall_progress.setter
    def overall_progress(self, value):
        self._overall_progress = value


class AdjustmentProgress(object):
    @staticmethod
    def from_json(json):
        instance = AdjustmentProgress()
        instance.before = json['before']
        instance.after = json['after']
        return instance

    @property
    def before(self):
        return self._before

    @before.setter
    def before(self, value):
        self._before = value

    @property
    def after(self):
        return self._after

    @after.setter
    def after(self, value):
        self._after = value


class Portfolio(object):
    @staticmethod
    def to_json(instance):
        positions_json = {}
        for security, position in instance.positions.items():
            positions_json[security] = Position.to_json(position)
        json = {
            'availableCash': instance.available_cash,
            'totalValue': instance.total_value,
            'positionsValue': instance.positions_value,
            'positions': positions_json
        }
        return json

    def __init__(self, available_cash=0):
        self._available_cash = available_cash
        self._total_value = available_cash
        self._positions_value = 0
        self._positions = dict()

    def __getitem__(self, security):
        return self._positions[security]

    def __setitem__(self, security, position):
        self._positions[security] = position

    @property
    def available_cash(self):
        return self._available_cash

    @available_cash.setter
    def available_cash(self, value):
        self._available_cash = value

    @property
    def total_value(self):
        return self._total_value

    @total_value.setter
    def total_value(self, value):
        self._total_value = value

    @property
    def positions_value(self):
        return self._positions_value

    @positions_value.setter
    def positions_value(self, value):
        self._positions_value = value

    @property
    def positions(self):
        return self._positions

    @positions.setter
    def positions(self, value):
        self._positions = value

    def add_position(self, position):
        self._positions_value += position.value
        self._total_value += position.value
        self._positions[position.security] = position


class Position(object):
    @staticmethod
    def to_json(instance):
        json = {
            'security': instance.security,
            'price': instance.price,
            'totalAmount': instance.total_amount,
            'closeableAmount': instance.closeable_amount,
        }
        return json

    def __init__(self, security, price=None, total_amount=0, closeable_amount=0):
        self._security = security
        self._price = price
        self._total_amount = total_amount
        self._closeable_amount = total_amount if closeable_amount is None else closeable_amount
        if price is not None and total_amount is not None:
            self._value = price * total_amount

    @property
    def security(self):
        return self._security

    @security.setter
    def security(self, value):
        self._security = value

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        self._price = value

    @property
    def total_amount(self):
        return self._total_amount

    @total_amount.setter
    def total_amount(self, value):
        self._total_amount = value

    @property
    def closeable_amount(self):
        return self._closeable_amount

    @closeable_amount.setter
    def closeable_amount(self, value):
        self._closeable_amount = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value
        self._total_amount = self._value / self._price


class OrderAction(Enum):
    OPEN = 'OPEN'
    CLOSE = 'CLOSE'


class OrderStyle(Enum):
    LIMIT = 'LIMIT'
    MARKET = 'MARKET'


class Order(object):
    @staticmethod
    def from_json(json):
        order = Order()
        order.action = OrderAction.OPEN if json['action'] == 'BUY' else OrderAction.CLOSE
        order.security = json['symbol']
        order.price = json['price']
        order.amount = json['amount']
        return order

    def __init__(self, action=None, security=None, amount=None, price=None, style=None):
        self._action = action
        self._security = security
        self._amount = amount
        self._price = price
        self._style = style

    def __str__(self):
        return '{0} {1:>5} {2:>5} {3} on {4:>7.3f}'.format(self._style.name, self._action.name, self._amount,
                                                           self._security,
                                                           self._price)

    @property
    def value(self):
        return self._amount * self._price

    @property
    def action(self):
        return self._action

    @action.setter
    def action(self, value):
        self._action = value

    @property
    def security(self):
        return self._security

    @security.setter
    def security(self, value):
        self._security = value

    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, value):
        self._amount = value

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        self._price = value

    @property
    def style(self):
        return self._style

    @style.setter
    def style(self, value):
        self._style = value
