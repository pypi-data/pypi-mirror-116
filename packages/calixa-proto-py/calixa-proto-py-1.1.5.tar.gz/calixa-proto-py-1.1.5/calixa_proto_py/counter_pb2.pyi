# @generated by generate_proto_mypy_stubs.py.  Do not edit!
import sys
from google.protobuf.descriptor import (
    Descriptor as google___protobuf___descriptor___Descriptor,
    EnumDescriptor as google___protobuf___descriptor___EnumDescriptor,
    FileDescriptor as google___protobuf___descriptor___FileDescriptor,
)

from google.protobuf.internal.enum_type_wrapper import (
    _EnumTypeWrapper as google___protobuf___internal___enum_type_wrapper____EnumTypeWrapper,
)

from google.protobuf.message import (
    Message as google___protobuf___message___Message,
)

from google.protobuf.timestamp_pb2 import (
    Timestamp as google___protobuf___timestamp_pb2___Timestamp,
)

from typing import (
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

CounterTypeValue = typing___NewType('CounterTypeValue', builtin___int)
type___CounterTypeValue = CounterTypeValue
CounterType: _CounterType
class _CounterType(google___protobuf___internal___enum_type_wrapper____EnumTypeWrapper[CounterTypeValue]):
    DESCRIPTOR: google___protobuf___descriptor___EnumDescriptor = ...
    COUNTER_TYPE_UNSPECIFIED = typing___cast(CounterTypeValue, 0)
    COUNTER_TYPE_METRIC = typing___cast(CounterTypeValue, 1)
COUNTER_TYPE_UNSPECIFIED = typing___cast(CounterTypeValue, 0)
COUNTER_TYPE_METRIC = typing___cast(CounterTypeValue, 1)
type___CounterType = CounterType

GroupByValue = typing___NewType('GroupByValue', builtin___int)
type___GroupByValue = GroupByValue
GroupBy: _GroupBy
class _GroupBy(google___protobuf___internal___enum_type_wrapper____EnumTypeWrapper[GroupByValue]):
    DESCRIPTOR: google___protobuf___descriptor___EnumDescriptor = ...
    GROUP_BY_UNSPECIFIED = typing___cast(GroupByValue, 0)
    GROUP_BY_HOUR = typing___cast(GroupByValue, 1)
    GROUP_BY_DAY = typing___cast(GroupByValue, 2)
    GROUP_BY_WEEK = typing___cast(GroupByValue, 3)
    GROUP_BY_MONTH = typing___cast(GroupByValue, 4)
    GROUP_BY_YEAR = typing___cast(GroupByValue, 5)
GROUP_BY_UNSPECIFIED = typing___cast(GroupByValue, 0)
GROUP_BY_HOUR = typing___cast(GroupByValue, 1)
GROUP_BY_DAY = typing___cast(GroupByValue, 2)
GROUP_BY_WEEK = typing___cast(GroupByValue, 3)
GROUP_BY_MONTH = typing___cast(GroupByValue, 4)
GROUP_BY_YEAR = typing___cast(GroupByValue, 5)
type___GroupBy = GroupBy

AggregateOperationValue = typing___NewType('AggregateOperationValue', builtin___int)
type___AggregateOperationValue = AggregateOperationValue
AggregateOperation: _AggregateOperation
class _AggregateOperation(google___protobuf___internal___enum_type_wrapper____EnumTypeWrapper[AggregateOperationValue]):
    DESCRIPTOR: google___protobuf___descriptor___EnumDescriptor = ...
    AGGREGATE_OPERATION_UNSPECIFIED = typing___cast(AggregateOperationValue, 0)
    AGGREGATE_OPERATION_SUM = typing___cast(AggregateOperationValue, 1)
    AGGREGATE_OPERATION_AVG = typing___cast(AggregateOperationValue, 2)
    AGGREGATE_OPERATION_COUNT = typing___cast(AggregateOperationValue, 3)
AGGREGATE_OPERATION_UNSPECIFIED = typing___cast(AggregateOperationValue, 0)
AGGREGATE_OPERATION_SUM = typing___cast(AggregateOperationValue, 1)
AGGREGATE_OPERATION_AVG = typing___cast(AggregateOperationValue, 2)
AGGREGATE_OPERATION_COUNT = typing___cast(AggregateOperationValue, 3)
type___AggregateOperation = AggregateOperation

class CounterKey(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    organization_id: typing___Text = ...
    key: typing___Text = ...
    counter_type: type___CounterTypeValue = ...
    param: typing___Text = ...

    def __init__(self,
        *,
        organization_id : typing___Optional[typing___Text] = None,
        key : typing___Optional[typing___Text] = None,
        counter_type : typing___Optional[type___CounterTypeValue] = None,
        param : typing___Optional[typing___Text] = None,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"counter_type",b"counter_type",u"key",b"key",u"organization_id",b"organization_id",u"param",b"param"]) -> None: ...
type___CounterKey = CounterKey

class CounterObservation(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    amount: builtin___int = ...
    count: builtin___int = ...

    @property
    def key(self) -> type___CounterKey: ...

    @property
    def observed_at(self) -> google___protobuf___timestamp_pb2___Timestamp: ...

    def __init__(self,
        *,
        key : typing___Optional[type___CounterKey] = None,
        observed_at : typing___Optional[google___protobuf___timestamp_pb2___Timestamp] = None,
        amount : typing___Optional[builtin___int] = None,
        count : typing___Optional[builtin___int] = None,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions___Literal[u"key",b"key",u"observed_at",b"observed_at"]) -> builtin___bool: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"amount",b"amount",u"count",b"count",u"key",b"key",u"observed_at",b"observed_at"]) -> None: ...
type___CounterObservation = CounterObservation

class CounterValueAtTime(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    valuePresent: builtin___bool = ...
    value: builtin___int = ...

    @property
    def time(self) -> google___protobuf___timestamp_pb2___Timestamp: ...

    def __init__(self,
        *,
        valuePresent : typing___Optional[builtin___bool] = None,
        value : typing___Optional[builtin___int] = None,
        time : typing___Optional[google___protobuf___timestamp_pb2___Timestamp] = None,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions___Literal[u"time",b"time"]) -> builtin___bool: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"time",b"time",u"value",b"value",u"valuePresent",b"valuePresent"]) -> None: ...
type___CounterValueAtTime = CounterValueAtTime
