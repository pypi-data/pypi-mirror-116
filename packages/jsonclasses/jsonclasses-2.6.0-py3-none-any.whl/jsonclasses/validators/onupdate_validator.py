"""module for onupdate validator."""
from typing import Callable, Any, cast
from inspect import signature
from .validator import Validator
from ..ctxs import TCtx


class OnUpdateValidator(Validator):
    """On update validator is called when value is modified and saving is
    triggered.
    """

    def __init__(self, callback: Callable) -> None:
        if not callable(callback):
            raise ValueError('onupdate argument is not callable')
        params_len = len(signature(callback).parameters)
        if params_len > 3:
            raise ValueError('not a valid onupdate callable')
        self.callback = callback

    def serialize(self, context: TCtx) -> Any:
        from ..jobject import JObject
        name = context.keypath_parent
        parent = cast(JObject, context.parent)
        if name not in parent.previous_values:
            return context.value
        prev_value = parent.previous_values[name]
        params_len = len(signature(self.callback).parameters)
        if params_len == 0:
            self.callback()
        elif params_len == 1:
            self.callback(context.value)
        elif params_len == 2:
            self.callback(prev_value, context.value)
        elif params_len == 3:
            self.callback(prev_value,
                          context.value,
                          context)
        return context.value
