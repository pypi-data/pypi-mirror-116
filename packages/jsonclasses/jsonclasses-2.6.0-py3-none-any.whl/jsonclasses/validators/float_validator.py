"""module for float validator."""
from typing import Any
from .type_validator import TypeValidator
from ..fdef import FieldType
from ..ctxs import TCtx


class FloatValidator(TypeValidator):
    """Date validator validate value against float type."""

    def __init__(self):
        super().__init__()
        self.cls = float
        self.field_type = FieldType.FLOAT

    def transform(self, context: TCtx) -> Any:
        if context.value is None:
            return None
        if type(context.value) is int:
            return float(context.value)
        return context.value
