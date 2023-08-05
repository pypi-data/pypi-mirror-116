# @generated by generate_proto_mypy_stubs.py.  Do not edit!
import sys
from google.protobuf.descriptor import (
    Descriptor as google___protobuf___descriptor___Descriptor,
    EnumDescriptor as google___protobuf___descriptor___EnumDescriptor,
    FileDescriptor as google___protobuf___descriptor___FileDescriptor,
)

from google.protobuf.internal.containers import (
    RepeatedCompositeFieldContainer as google___protobuf___internal___containers___RepeatedCompositeFieldContainer,
)

from google.protobuf.internal.enum_type_wrapper import (
    _EnumTypeWrapper as google___protobuf___internal___enum_type_wrapper____EnumTypeWrapper,
)

from google.protobuf.message import (
    Message as google___protobuf___message___Message,
)

from typing import (
    Iterable as typing___Iterable,
    Mapping as typing___Mapping,
    MutableMapping as typing___MutableMapping,
    NewType as typing___NewType,
    Optional as typing___Optional,
    Text as typing___Text,
    cast as typing___cast,
)

from typing_extensions import (
    Literal as typing_extensions___Literal,
)


builtin___bool = bool
builtin___bytes = bytes
builtin___float = float
builtin___int = int


DESCRIPTOR: google___protobuf___descriptor___FileDescriptor = ...

RelatedDataTypeValue = typing___NewType('RelatedDataTypeValue', builtin___int)
type___RelatedDataTypeValue = RelatedDataTypeValue
RelatedDataType: _RelatedDataType
class _RelatedDataType(google___protobuf___internal___enum_type_wrapper____EnumTypeWrapper[RelatedDataTypeValue]):
    DESCRIPTOR: google___protobuf___descriptor___EnumDescriptor = ...
    RELATED_DATA_TYPE_UNSPECIFIED = typing___cast(RelatedDataTypeValue, 0)
    RELATED_DATA_TYPE_COUPON = typing___cast(RelatedDataTypeValue, 1)
    RELATED_DATA_TYPE_SUBSCRIPTION = typing___cast(RelatedDataTypeValue, 2)
    RELATED_DATA_TYPE_OPPORTUNITY = typing___cast(RelatedDataTypeValue, 3)
    RELATED_DATA_TYPE_TASK = typing___cast(RelatedDataTypeValue, 4)
    RELATED_DATA_TYPE_SLACK_CHANNEL = typing___cast(RelatedDataTypeValue, 10000)
RELATED_DATA_TYPE_UNSPECIFIED = typing___cast(RelatedDataTypeValue, 0)
RELATED_DATA_TYPE_COUPON = typing___cast(RelatedDataTypeValue, 1)
RELATED_DATA_TYPE_SUBSCRIPTION = typing___cast(RelatedDataTypeValue, 2)
RELATED_DATA_TYPE_OPPORTUNITY = typing___cast(RelatedDataTypeValue, 3)
RELATED_DATA_TYPE_TASK = typing___cast(RelatedDataTypeValue, 4)
RELATED_DATA_TYPE_SLACK_CHANNEL = typing___cast(RelatedDataTypeValue, 10000)
type___RelatedDataType = RelatedDataType

RelatedDataFieldTypeValue = typing___NewType('RelatedDataFieldTypeValue', builtin___int)
type___RelatedDataFieldTypeValue = RelatedDataFieldTypeValue
RelatedDataFieldType: _RelatedDataFieldType
class _RelatedDataFieldType(google___protobuf___internal___enum_type_wrapper____EnumTypeWrapper[RelatedDataFieldTypeValue]):
    DESCRIPTOR: google___protobuf___descriptor___EnumDescriptor = ...
    RELATED_DATA_FIELD_TYPE_UNSPECIFIED = typing___cast(RelatedDataFieldTypeValue, 0)
    RELATED_DATA_FIELD_TYPE_AMOUNT = typing___cast(RelatedDataFieldTypeValue, 1)
    RELATED_DATA_FIELD_TYPE_BOOLEAN = typing___cast(RelatedDataFieldTypeValue, 2)
    RELATED_DATA_FIELD_TYPE_COUNTRY = typing___cast(RelatedDataFieldTypeValue, 3)
    RELATED_DATA_FIELD_TYPE_CURRENCY = typing___cast(RelatedDataFieldTypeValue, 4)
    RELATED_DATA_FIELD_TYPE_DATE = typing___cast(RelatedDataFieldTypeValue, 5)
    RELATED_DATA_FIELD_TYPE_ENUM = typing___cast(RelatedDataFieldTypeValue, 6)
    RELATED_DATA_FIELD_TYPE_MICROS = typing___cast(RelatedDataFieldTypeValue, 7)
    RELATED_DATA_FIELD_TYPE_NUMBER = typing___cast(RelatedDataFieldTypeValue, 8)
    RELATED_DATA_FIELD_TYPE_PERCENTAGE = typing___cast(RelatedDataFieldTypeValue, 9)
    RELATED_DATA_FIELD_TYPE_STRING = typing___cast(RelatedDataFieldTypeValue, 10)
    RELATED_DATA_FIELD_TYPE_RENDERABLE = typing___cast(RelatedDataFieldTypeValue, 11)
RELATED_DATA_FIELD_TYPE_UNSPECIFIED = typing___cast(RelatedDataFieldTypeValue, 0)
RELATED_DATA_FIELD_TYPE_AMOUNT = typing___cast(RelatedDataFieldTypeValue, 1)
RELATED_DATA_FIELD_TYPE_BOOLEAN = typing___cast(RelatedDataFieldTypeValue, 2)
RELATED_DATA_FIELD_TYPE_COUNTRY = typing___cast(RelatedDataFieldTypeValue, 3)
RELATED_DATA_FIELD_TYPE_CURRENCY = typing___cast(RelatedDataFieldTypeValue, 4)
RELATED_DATA_FIELD_TYPE_DATE = typing___cast(RelatedDataFieldTypeValue, 5)
RELATED_DATA_FIELD_TYPE_ENUM = typing___cast(RelatedDataFieldTypeValue, 6)
RELATED_DATA_FIELD_TYPE_MICROS = typing___cast(RelatedDataFieldTypeValue, 7)
RELATED_DATA_FIELD_TYPE_NUMBER = typing___cast(RelatedDataFieldTypeValue, 8)
RELATED_DATA_FIELD_TYPE_PERCENTAGE = typing___cast(RelatedDataFieldTypeValue, 9)
RELATED_DATA_FIELD_TYPE_STRING = typing___cast(RelatedDataFieldTypeValue, 10)
RELATED_DATA_FIELD_TYPE_RENDERABLE = typing___cast(RelatedDataFieldTypeValue, 11)
type___RelatedDataFieldType = RelatedDataFieldType

class RelatedData(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    class PropertiesEntry(google___protobuf___message___Message):
        DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
        key: typing___Text = ...

        @property
        def value(self) -> type___Property: ...

        def __init__(self,
            *,
            key : typing___Optional[typing___Text] = None,
            value : typing___Optional[type___Property] = None,
            ) -> None: ...
        def HasField(self, field_name: typing_extensions___Literal[u"value",b"value"]) -> builtin___bool: ...
        def ClearField(self, field_name: typing_extensions___Literal[u"key",b"key",u"value",b"value"]) -> None: ...
    type___PropertiesEntry = PropertiesEntry

    field: typing___Text = ...
    display: typing___Text = ...
    field_type: type___RelatedDataFieldTypeValue = ...
    has_other: builtin___bool = ...
    associated_with: typing___Text = ...

    @property
    def values(self) -> google___protobuf___internal___containers___RepeatedCompositeFieldContainer[type___Value]: ...

    @property
    def properties(self) -> typing___MutableMapping[typing___Text, type___Property]: ...

    def __init__(self,
        *,
        field : typing___Optional[typing___Text] = None,
        display : typing___Optional[typing___Text] = None,
        field_type : typing___Optional[type___RelatedDataFieldTypeValue] = None,
        has_other : typing___Optional[builtin___bool] = None,
        values : typing___Optional[typing___Iterable[type___Value]] = None,
        associated_with : typing___Optional[typing___Text] = None,
        properties : typing___Optional[typing___Mapping[typing___Text, type___Property]] = None,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"associated_with",b"associated_with",u"display",b"display",u"field",b"field",u"field_type",b"field_type",u"has_other",b"has_other",u"properties",b"properties",u"values",b"values"]) -> None: ...
type___RelatedData = RelatedData

class Value(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    foreign_key: typing___Text = ...
    display_name: typing___Text = ...

    def __init__(self,
        *,
        foreign_key : typing___Optional[typing___Text] = None,
        display_name : typing___Optional[typing___Text] = None,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"display_name",b"display_name",u"foreign_key",b"foreign_key"]) -> None: ...
type___Value = Value

class Property(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    field_type: type___RelatedDataFieldTypeValue = ...
    value: typing___Text = ...

    def __init__(self,
        *,
        field_type : typing___Optional[type___RelatedDataFieldTypeValue] = None,
        value : typing___Optional[typing___Text] = None,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"field_type",b"field_type",u"value",b"value"]) -> None: ...
type___Property = Property
