from typing import Any, Optional

class MeasureBase:
    STANDARD_UNIT: Any = ...
    ALIAS: Any = ...
    UNITS: Any = ...
    LALIAS: Any = ...
    def __init__(self, default_unit: Optional[Any] = ..., **kwargs: Any) -> None: ...
    standard: Any = ...
    def __getattr__(self, name: Any) -> Any: ...
    def __eq__(self, other: Any) -> Any: ...
    def __lt__(self, other: Any) -> Any: ...
    def __add__(self, other: Any) -> Any: ...
    def __iadd__(self, other: Any) -> Any: ...
    def __sub__(self, other: Any) -> Any: ...
    def __isub__(self, other: Any) -> Any: ...
    def __mul__(self, other: Any) -> Any: ...
    def __imul__(self, other: Any) -> Any: ...
    def __rmul__(self, other: Any) -> Any: ...
    def __truediv__(self, other: Any) -> Any: ...
    def __itruediv__(self, other: Any) -> Any: ...
    def __bool__(self) -> Any: ...
    def default_units(self, kwargs: Any) -> Any: ...
    @classmethod
    def unit_attname(cls, unit_str: Any) -> Any: ...

class Distance(MeasureBase):
    STANDARD_UNIT: str = ...
    UNITS: Any = ...
    ALIAS: Any = ...
    LALIAS: Any = ...
    def __mul__(self, other: Any) -> Any: ...

class Area(MeasureBase):
    STANDARD_UNIT: Any = ...
    UNITS: Any = ...
    ALIAS: Any = ...
    LALIAS: Any = ...
    def __truediv__(self, other: Any) -> Any: ...

D = Distance
A = Area
