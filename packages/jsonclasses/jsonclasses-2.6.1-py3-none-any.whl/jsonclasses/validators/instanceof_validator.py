"""module for instanceof validator."""
from __future__ import annotations
from jsonclasses.jfield import JField
from typing import Any, Sequence, Union, cast, TYPE_CHECKING
from inflection import camelize
from ..fdef import (Fdef, FieldStorage, FieldType,
                                Nullability, WriteRule, ReadRule, Strictness)
from ..exceptions import ValidationException
from .validator import Validator
from ..keypath import concat_keypath, initial_keypaths
from ..rtypes import rtypes
from ..ctxs import VCtx, TCtx, JCtx
if TYPE_CHECKING:
    from ..jobject import JObject
    from ..types import Types
    InstanceOfType = Union[Types, str, type[JObject]]


class InstanceOfValidator(Validator):
    """InstanceOf validator validates and transforms JSON Class instance."""

    def __init__(self, raw_type: InstanceOfType) -> None:
        self.raw_type = raw_type

    def define(self, fdef: Fdef) -> None:
        fdef._field_type = FieldType.INSTANCE
        fdef._raw_inst_types = self.raw_type

    def validate(self, context: VCtx) -> None:
        from ..jobject import JObject
        if context.value is None:
            return
        types = rtypes(self.raw_type, context.config_owner)
        cls = cast(type[JObject], types.fdef.raw_inst_types)
        all_fields = context.all_fields
        if all_fields is None:
            all_fields = cls.cdef.config.validate_all_fields
        if not isinstance(context.value, cls):
            raise ValidationException({
                context.keypath_root: (f"Value at '{context.keypath_root}' "
                                       f"should be instance of "
                                       f"'{cls.__name__}'.")
            }, context.root)
        if context.mark_graph.has(context.value):
            return
        context.mark_graph.put(context.value)
        only_validate_modified = False
        modified_fields = []
        if not context.value.is_new:
            only_validate_modified = True
            modified_fields = list(initial_keypaths((context.value
                                                     .modified_fields)))
        keypath_messages = {}
        for field in context.value.__class__.cdef.fields:
            fname = field.name
            if field.fdef.field_storage == FieldStorage.EMBEDDED:
                if only_validate_modified and fname not in modified_fields:
                    continue
            try:
                field.types.validator.validate(context.new(
                    value=getattr(context.value, fname),
                    keypath_root=concat_keypath(context.keypath_root, fname),
                    keypath_owner=fname,
                    owner=context.value,
                    config_owner=context.value.__class__.cdef.config,
                    keypath_parent=fname,
                    parent=context.value,
                    fdef=field.fdef))
            except ValidationException as exception:
                if all_fields:
                    keypath_messages.update(exception.keypath_messages)
                else:
                    raise exception
        if len(keypath_messages) > 0:
            raise ValidationException(
                keypath_messages=keypath_messages,
                root=context.root)

    def _strictness_check(self,
                          context: TCtx,
                          dest: JObject) -> None:
        available_names = dest.__class__.cdef._available_names
        for k in context.value.keys():
            if k not in available_names:
                kp = concat_keypath(context.keypath_root, k)
                if context.keypath_root == '':
                    msg = f'Key \'{k}\' is not allowed.'
                else:
                    msg = f'Key \'{k}\' at \'{context.keypath_root}\' is not allowed.'
                raise ValidationException({kp: msg}, context.root)

    def _fill_default_value(self,
                            field: JField,
                            dest: JObject,
                            context: TCtx,
                            cls: type[JObject]):
        if field.default is not None:
            setattr(dest, field.name, field.default)
        else:
            tsfmd = field.types.validator.transform(context.new(
                value=None,
                keypath_root=concat_keypath(context.keypath_root, field.name),
                keypath_owner=field.name,
                owner=context.value,
                config_owner=cls.cdef.config,
                keypath_parent=field.name,
                parent=context.value,
                fdef=field.fdef))
            setattr(dest, field.name, tsfmd)

    def _has_field_value(self, field: JField, keys: Sequence[str]) -> bool:
        return field.json_name in keys or field.name in keys

    def _get_field_value(self,
                         field: JField,
                         context: TCtx) -> Any:
        field_value = context.value.get(field.json_name)
        if field_value is None and context.config_owner.camelize_json_keys:
            field_value = context.value.get(field.name)
        return field_value

    # pylint: disable=arguments-differ, too-many-locals, too-many-branches
    def transform(self, context: TCtx) -> Any:
        from ..types import Types
        from ..jobject import JObject
        # handle non normal value
        if context.value is None:
            return context.dest
        if not isinstance(context.value, dict):
            return context.dest if context.dest is not None else context.value
        # figure out types, cls and dest
        types = rtypes(self.raw_type, context.config_owner)
        cls = cast(type[JObject], types.fdef.raw_inst_types)
        this_pk_field = cls.cdef.primary_field
        if this_pk_field:
            pk = this_pk_field.name
            pk_value = cast(Union[str, int], context.value.get(pk))
        else:
            pk_value = None
        soft_apply_mode = False
        if context.dest is not None:
            dest = context.dest
            if pk_value is not None:
                context.mark_graph.putp(pk_value, dest)
        elif pk_value is not None:
            exist_item = context.mark_graph.getp(cls, pk_value)
            if exist_item is not None:
                dest = exist_item
                soft_apply_mode = True
            else:
                dest = cls()
                context.mark_graph.putp(pk_value, dest)
        else:
            dest = cls()
            context.mark_graph.put(dest)

        # strictness check
        strictness = cast(bool, cls.cdef.config.strict_input)
        if context.fdef is not None:
            if context.fdef.strictness == Strictness.STRICT:
                strictness = True
            elif context.fdef.strictness == Strictness.UNSTRICT:
                strictness = False
        if strictness:
            self._strictness_check(context, dest)
        # fill values
        dict_keys = list(context.value.keys())
        nonnull_ref_lists: list[str] = []
        for field in dest.__class__.cdef.fields:
            if not self._has_field_value(field, dict_keys):
                if field.fdef.is_ref:
                    fdef = field.fdef
                    if fdef.field_type == FieldType.LIST:
                        if fdef.collection_nullability == Nullability.NONNULL:
                            nonnull_ref_lists.append(field.name)
                    elif fdef.field_storage == FieldStorage.LOCAL_KEY:
                        tsfm = dest.__class__.cdef.config.key_transformer
                        refname = tsfm(field)
                        if context.value.get(refname) is not None:
                            setattr(dest, refname, context.value.get(refname))
                        crefname = camelize(refname, False)
                        if context.value.get(crefname) is not None:
                            setattr(dest, refname, context.value.get(crefname))
                    pass
                elif context.fill_dest_blanks and not soft_apply_mode:
                    self._fill_default_value(field, dest, context, cls)
                continue
            field_value = self._get_field_value(field, context)
            allow_write_field = True
            if field.fdef.write_rule == WriteRule.NO_WRITE:
                allow_write_field = False
            if field.fdef.write_rule == WriteRule.WRITE_ONCE:
                cfv = getattr(dest, field.name)
                if (cfv is not None) and (not isinstance(cfv, Types)):
                    allow_write_field = False
            if field.fdef.write_rule == WriteRule.WRITE_NONNULL:
                if field_value is None:
                    allow_write_field = False
            if not allow_write_field:
                if context.fill_dest_blanks:
                    self._fill_default_value(field, dest, context, cls)
                continue
            field_context = context.new(
                value=field_value,
                keypath_root=concat_keypath(context.keypath_root,
                                            field.name),
                keypath_owner=field.name,
                owner=context.value,
                config_owner=cls.cdef.config,
                keypath_parent=field.name,
                parent=context.value,
                fdef=field.fdef)
            tsfmd = field.types.validator.transform(field_context)
            setattr(dest, field.name, tsfmd)
        for cname in nonnull_ref_lists:
            if getattr(dest, cname) is None:
                setattr(dest, cname, [])
        return dest

    def tojson(self, context: JCtx) -> Any:
        if context.value is None:
            return None
        retval = {}
        entity_chain = context.entity_chain
        cls_name = context.value.__class__.__name__
        no_key_refs = cls_name in entity_chain
        for field in context.value.__class__.cdef.fields:
            field_value = getattr(context.value, field.name)
            fd = field.types.fdef
            jf_name = field.json_name
            ignore_writeonly = context.ignore_writeonly
            if fd.field_storage == FieldStorage.LOCAL_KEY and no_key_refs:
                continue
            if fd.field_storage == FieldStorage.FOREIGN_KEY and no_key_refs:
                continue
            if fd.read_rule == ReadRule.NO_READ and not ignore_writeonly:
                continue
            if fd.is_temp_field:
                continue
            item_context = context.new(
                value=field_value,
                fdef=field.fdef,
                entity_chain=[*entity_chain, cls_name])
            retval[jf_name] = field.types.validator.tojson(item_context)
        return retval

    def serialize(self, context: TCtx) -> Any:
        from ..jobject import JObject
        value = cast(JObject, context.value)
        if value is None:
            return None
        exist_item = context.mark_graph.get(value)
        if exist_item is not None:  # Don't do twice for an object
            return value
        context.mark_graph.put(value)
        should_update = True
        if not value.is_modified and not value.is_new:
            should_update = False
        for field in value.__class__.cdef.fields:
            if (field.fdef.is_ref
                    or field.fdef.is_inst
                    or should_update):
                if field.fdef.field_storage == FieldStorage.LOCAL_KEY:
                    if getattr(value, field.name) is None:
                        tsf = value.__class__.cdef.config.key_transformer
                        if getattr(value, tsf(field)) is not None:
                            continue
                field_value = getattr(value, field.name)
                field_context = context.new(
                    value=field_value,
                    keypath_root=concat_keypath(context.keypath_root,
                                                field.name),
                    keypath_owner=field.name,
                    owner=value,
                    config_owner=value.__class__.cdef.config,
                    keypath_parent=field.name,
                    parent=value,
                    fdef=field.fdef)
                tsfmd = field.types.validator.serialize(field_context)
                setattr(value, field.name, tsfmd)
        return value
