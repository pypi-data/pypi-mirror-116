from typing import Any, Optional

from django.db.models import lookups
from django.db.models.lookups import PostgresOperatorLookup, Transform

from . import Field
from .mixins import CheckFieldDefaultMixin

class JSONField(CheckFieldDefaultMixin, Field[Any, Any]):
    empty_strings_allowed: bool = ...
    description: Any = ...
    default_error_messages: Any = ...
    encoder: Any = ...
    decoder: Any = ...
    def __init__(
        self,
        verbose_name: Optional[Any] = ...,
        name: Optional[Any] = ...,
        encoder: Optional[Any] = ...,
        decoder: Optional[Any] = ...,
        **kwargs: Any
    ) -> None: ...
    def check(self, **kwargs: Any) -> Any: ...
    def deconstruct(self) -> Any: ...
    def from_db_value(self, value: Any, expression: Any, connection: Any) -> Any: ...
    def get_internal_type(self) -> Any: ...
    def get_prep_value(self, value: Any) -> Any: ...
    def get_transform(self, name: Any) -> Any: ...
    def validate(self, value: Any, model_instance: Any) -> None: ...
    def value_to_string(self, obj: Any) -> Any: ...
    def formfield(self, **kwargs: Any) -> Any: ...

class DataContains(PostgresOperatorLookup):
    lookup_name: str = ...
    postgres_operator: str = ...
    def as_sql(self, compiler: Any, connection: Any) -> Any: ...

class ContainedBy(PostgresOperatorLookup):
    lookup_name: str = ...
    postgres_operator: str = ...
    def as_sql(self, compiler: Any, connection: Any) -> Any: ...

class HasKeyLookup(PostgresOperatorLookup):
    logical_operator: Any = ...
    def as_sql(
        self, compiler: Any, connection: Any, template: Optional[Any] = ...
    ) -> Any: ...
    def as_mysql(self, compiler: Any, connection: Any) -> Any: ...
    def as_oracle(self, compiler: Any, connection: Any) -> Any: ...
    lhs: Any = ...
    rhs: Any = ...
    def as_postgresql(self, compiler: Any, connection: Any) -> Any: ...
    def as_sqlite(self, compiler: Any, connection: Any) -> Any: ...

class HasKey(HasKeyLookup):
    lookup_name: str = ...
    postgres_operator: str = ...
    prepare_rhs: bool = ...

class HasKeys(HasKeyLookup):
    lookup_name: str = ...
    postgres_operator: str = ...
    logical_operator: str = ...
    def get_prep_lookup(self) -> Any: ...

class HasAnyKeys(HasKeys):
    lookup_name: str = ...
    postgres_operator: str = ...
    logical_operator: str = ...

class JSONExact(lookups.Exact):
    can_use_none_as_rhs: bool = ...
    def process_rhs(self, compiler: Any, connection: Any) -> Any: ...

class KeyTransform(Transform):
    postgres_operator: str = ...
    postgres_nested_operator: str = ...
    key_name: Any = ...
    def __init__(self, key_name: Any, *args: Any, **kwargs: Any) -> None: ...
    def preprocess_lhs(
        self, compiler: Any, connection: Any, lhs_only: bool = ...
    ) -> Any: ...
    def as_mysql(self, compiler: Any, connection: Any) -> Any: ...
    def as_oracle(self, compiler: Any, connection: Any) -> Any: ...
    def as_postgresql(self, compiler: Any, connection: Any) -> Any: ...

class KeyTextTransform(KeyTransform):
    postgres_operator: str = ...
    postgres_nested_operator: str = ...

class KeyTransformTextLookupMixin:
    def __init__(self, key_transform: Any, *args: Any, **kwargs: Any) -> None: ...

class CaseInsensitiveMixin:
    def process_rhs(self, compiler: Any, connection: Any) -> Any: ...

class KeyTransformIsNull(lookups.IsNull):
    def as_oracle(self, compiler: Any, connection: Any) -> Any: ...
    def as_sqlite(self, compiler: Any, connection: Any) -> Any: ...

class KeyTransformIn(lookups.In):
    def process_rhs(self, compiler: Any, connection: Any) -> Any: ...

class KeyTransformExact(JSONExact):
    def process_rhs(self, compiler: Any, connection: Any) -> Any: ...
    def as_oracle(self, compiler: Any, connection: Any) -> Any: ...

class KeyTransformIExact(
    CaseInsensitiveMixin, KeyTransformTextLookupMixin, lookups.IExact
): ...
class KeyTransformIContains(
    CaseInsensitiveMixin, KeyTransformTextLookupMixin, lookups.IContains
): ...
class KeyTransformStartsWith(KeyTransformTextLookupMixin, lookups.StartsWith): ...
class KeyTransformIStartsWith(
    CaseInsensitiveMixin, KeyTransformTextLookupMixin, lookups.IStartsWith
): ...
class KeyTransformEndsWith(KeyTransformTextLookupMixin, lookups.EndsWith): ...
class KeyTransformIEndsWith(
    CaseInsensitiveMixin, KeyTransformTextLookupMixin, lookups.IEndsWith
): ...
class KeyTransformRegex(KeyTransformTextLookupMixin, lookups.Regex): ...
class KeyTransformIRegex(
    CaseInsensitiveMixin, KeyTransformTextLookupMixin, lookups.IRegex
): ...

class KeyTransformNumericLookupMixin:
    def process_rhs(self, compiler: Any, connection: Any) -> Any: ...

class KeyTransformLt(KeyTransformNumericLookupMixin, lookups.LessThan[Any]): ...
class KeyTransformLte(KeyTransformNumericLookupMixin, lookups.LessThanOrEqual): ...
class KeyTransformGt(KeyTransformNumericLookupMixin, lookups.GreaterThan): ...
class KeyTransformGte(
    KeyTransformNumericLookupMixin, lookups.GreaterThanOrEqual[Any]
): ...

class KeyTransformFactory:
    key_name: Any = ...
    def __init__(self, key_name: Any) -> None: ...
    def __call__(self, *args: Any, **kwargs: Any) -> Any: ...
