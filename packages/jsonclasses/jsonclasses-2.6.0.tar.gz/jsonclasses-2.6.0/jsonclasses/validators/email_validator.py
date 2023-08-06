"""module for email validator."""
from re import compile, match
from ..exceptions import ValidationException
from .validator import Validator
from ..ctxs import VCtx


class EmailValidator(Validator):
    """Email validator raises if value is not valid email."""

    def validate(self, context: VCtx) -> None:
        if context.value is None:
            return
        value = context.value
        regex = compile(
            r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        )


        if match(regex, value) is None:
            kp = context.keypath_root
            raise ValidationException(
                {kp: f'email \'{value}\' at \'{kp}\' is not valid email.'},
                context.root
            )
