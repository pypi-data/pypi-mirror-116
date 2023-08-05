from ctypes import c_char_p
from typing import Any, Optional

class gdal_char_p(c_char_p): ...

def bool_output(func: Any, argtypes: Any, errcheck: Optional[Any] = ...) -> Any: ...
def double_output(
    func: Any, argtypes: Any, errcheck: bool = ..., strarg: bool = ..., cpl: bool = ...
) -> Any: ...
def geom_output(func: Any, argtypes: Any, offset: Optional[Any] = ...) -> Any: ...
def int_output(func: Any, argtypes: Any, errcheck: Optional[Any] = ...) -> Any: ...
def int64_output(func: Any, argtypes: Any) -> Any: ...
def srs_output(func: Any, argtypes: Any) -> Any: ...
def const_string_output(
    func: Any,
    argtypes: Any,
    offset: Optional[Any] = ...,
    decoding: Optional[Any] = ...,
    cpl: bool = ...,
) -> Any: ...
def string_output(
    func: Any,
    argtypes: Any,
    offset: int = ...,
    str_result: bool = ...,
    decoding: Optional[Any] = ...,
) -> Any: ...
def void_output(
    func: Any, argtypes: Any, errcheck: bool = ..., cpl: bool = ...
) -> Any: ...
def voidptr_output(func: Any, argtypes: Any, errcheck: bool = ...) -> Any: ...
def chararray_output(func: Any, argtypes: Any, errcheck: bool = ...) -> Any: ...
