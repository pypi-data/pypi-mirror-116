"""module for alnum validator."""
from ..exceptions import ValidationException
from .validator import Validator
from ..ctxs import VCtx


class AlnumValidator(Validator):
    """Alnum validator raises if value is not made up of alpha and number."""

    def validate(self, context: VCtx) -> None:
        if context.value is None:
            return
        value = context.value
        if not value.isalnum():
            kp = context.keypath_root
            raise ValidationException(
                {kp: f'product_code \'{value}\' at \'{kp}\' is not made up of alpha and number.'},
                context.root
            )
