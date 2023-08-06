"""module for required validator."""
from ..fdef import Fdef
from ..exceptions import ValidationException
from .validator import Validator
from ..ctxs import VCtx


class PresentValidator(Validator):
    """Present validator marks a field as present. When validating, if no value
    is present in this field, validation will fail. This is useful for foreign
    key fields to do required validation.
    """

    def define(self, fdef: Fdef) -> None:
        fdef._required = True

    def validate(self, context: VCtx) -> None:
        if context.value is None:
            raise ValidationException(
                {context.keypath_root: (f'Value at \'{context.keypath_root}\''
                                        ' should be present.')},
                context.root)
