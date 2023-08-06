"""module for range validator."""
from typing import Union
from .validator import Validator
from .min_validator import MinValidator
from .max_validator import MaxValidator
from ..ctxs import VCtx


class RangeValidator(Validator):
    """A range validator validates value against a range."""

    def __init__(self, min_value: Union[int, float], max_value: Union[int, float]):
        self.min_value = min_value
        self.max_value = max_value

    def validate(self, context: VCtx) -> None:
        if context.value is None:
            return
        MinValidator(self.min_value).validate(context)
        MaxValidator(self.max_value).validate(context)
