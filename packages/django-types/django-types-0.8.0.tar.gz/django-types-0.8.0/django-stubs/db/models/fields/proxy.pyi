from typing import Any

from django.db.models import fields

class OrderWrt(fields.IntegerField[Any]):
    def __init__(self, *args: Any, **kwargs: Any) -> None: ...
