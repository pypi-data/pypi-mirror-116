from typing import Any

from django.db.models import Lookup, Transform
from django.db.models.lookups import Exact

from .search import SearchVectorExact

class PostgresSimpleLookup(Lookup[Any]):
    operator: str

class DataContains(PostgresSimpleLookup): ...
class ContainedBy(PostgresSimpleLookup): ...
class Overlap(PostgresSimpleLookup): ...
class HasKey(PostgresSimpleLookup): ...
class HasKeys(PostgresSimpleLookup): ...
class HasAnyKeys(HasKeys): ...
class Unaccent(Transform): ...
class SearchLookup(SearchVectorExact): ...
class TrigramSimilar(PostgresSimpleLookup): ...
class JSONExact(Exact): ...
