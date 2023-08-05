from django.db.models.aggregates import Aggregate

from .mixins import OrderableAggMixin

class ArrayAgg(OrderableAggMixin, Aggregate): ...
class BitAnd(Aggregate): ...
class BitOr(Aggregate): ...
class BoolAnd(Aggregate): ...
class BoolOr(Aggregate): ...
class JSONBAgg(Aggregate): ...
class StringAgg(OrderableAggMixin, Aggregate): ...
