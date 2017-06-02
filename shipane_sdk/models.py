# -*- coding: utf-8 -*-

from __future__ import division

from enum import Enum


class Adjustment(object):
    @staticmethod
    def to_json(instance):
        json = {
            'targetPortfolio': Portfolio.to_json(instance.target_portfolio),
            'context': AdjustmentContext.to_json(instance.context)
        }
        return json

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
        instance._progress = AdjustmentProgressGroup.from_json(json['progress'])
        return instance

    def empty(self):
        return not self.batches

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

    @property
    def batches(self):
        return self._batches

    @batches.setter
    def batches(self, value):
        self._batches = value

    @property
    def progress(self):
        return self._progress

    @progress.setter
    def progress(self, value):
        self._progress = value


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


class AdjustmentProgressGroup(object):
    @staticmethod
    def from_json(json):
        instance = AdjustmentProgressGroup()
        instance._today = AdjustmentProgress.from_json(json['today'])
        instance._overall = AdjustmentProgress.from_json(json['overall'])
        return instance

    def __str__(self):
        str = "今日进度：{0:>.0f}% -> {1:>.0f}%；总进度：{2:>.0f}% -> {3:>.0f}%".format(
            self.today.before * 100, self.today.after * 100,
            self.overall.before * 100, self.overall.after * 100
        )
        return str

    @property
    def today(self):
        return self._today

    @today.setter
    def today(self, value):
        self._today = value

    @property
    def overall(self):
        return self._overall

    @overall.setter
    def overall(self, value):
        self._overall = value


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

    def __init__(self, available_cash=None, total_value=None):
        self._available_cash = available_cash
        self._total_value = total_value
        self._positions_value = 0
        self._positions = dict()

    def __getitem__(self, security):
        return self._positions[security]

    def __setitem__(self, security, position):
        self._positions[security] = position

    @property
    def fingerprint(self):
        result = dict((security, position.total_amount) for security, position in self._positions.items())
        return result

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
        self._positions[position.security] = position

    def rebalance(self):
        if self._available_cash is None:
            self._available_cash = self._total_value - self._positions_value
        elif self._total_value is None:
            self._total_value = self._available_cash + self.positions_value
        if self._available_cash < 0:
            self._available_cash = 0
            self._total_value = self._positions_value

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

    def __init__(self, security=None, price=None, total_amount=0, closeable_amount=0):
        self._security = self._normalize_security(security)
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
        self._security = self._normalize_security(value)

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

    def _normalize_security(self, security):
        return security.split('.')[0] if security else None


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
        str = "以 {0:>7.3f}元 {1}{2} {3:>5} {4}".format(
            self.price,
            '限价' if self.style == OrderStyle.LIMIT else '市价',
            '买入' if self.action == OrderAction.OPEN else '卖出',
            self.amount,
            self.security
        )
        return str

    def to_e_order(self):
        e_order = dict(
            action='BUY' if self._action == OrderAction.OPEN else 'SELL',
            symbol=self._security,
            type=self._style,
            amount=self._amount
        )
        return e_order

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
