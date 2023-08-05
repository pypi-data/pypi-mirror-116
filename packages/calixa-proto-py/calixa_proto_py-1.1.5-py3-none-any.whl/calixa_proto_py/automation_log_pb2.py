# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: automation_log.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
import entity_pb2 as entity__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='automation_log.proto',
  package='calixa.domain.automation.log',
  syntax='proto3',
  serialized_options=b'\n\037io.calixa.domain.automation.logH\001P\001',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x14\x61utomation_log.proto\x12\x1c\x63\x61lixa.domain.automation.log\x1a\x1fgoogle/protobuf/timestamp.proto\x1a\x0c\x65ntity.proto\"\xab\x02\n\rAutomationLog\x12\n\n\x02id\x18\x01 \x01(\t\x12.\n\nstarted_at\x18\x02 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12/\n\x0b\x66inished_at\x18\x03 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12=\n\x06status\x18\x04 \x01(\x0e\x32-.calixa.domain.automation.log.ExecutionStatus\x12,\n\x06\x65ntity\x18\x64 \x01(\x0b\x32\x1c.calixa.domain.entity.Entity\x12\x30\n\nautomation\x18\x65 \x01(\x0b\x32\x1c.calixa.domain.entity.Entity\x12\x0e\n\x05\x65rror\x18\xe8\x07 \x01(\t*m\n\x0f\x45xecutionStatus\x12 \n\x1c\x45XECUTION_STATUS_UNSPECIFIED\x10\x00\x12\x1c\n\x18\x45XECUTION_STATUS_SUCCESS\x10\x01\x12\x1a\n\x16\x45XECUTION_STATUS_ERROR\x10\x02\x42%\n\x1fio.calixa.domain.automation.logH\x01P\x01\x62\x06proto3'
  ,
  dependencies=[google_dot_protobuf_dot_timestamp__pb2.DESCRIPTOR,entity__pb2.DESCRIPTOR,])

_EXECUTIONSTATUS = _descriptor.EnumDescriptor(
  name='ExecutionStatus',
  full_name='calixa.domain.automation.log.ExecutionStatus',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='EXECUTION_STATUS_UNSPECIFIED', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='EXECUTION_STATUS_SUCCESS', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='EXECUTION_STATUS_ERROR', index=2, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=403,
  serialized_end=512,
)
_sym_db.RegisterEnumDescriptor(_EXECUTIONSTATUS)

ExecutionStatus = enum_type_wrapper.EnumTypeWrapper(_EXECUTIONSTATUS)
EXECUTION_STATUS_UNSPECIFIED = 0
EXECUTION_STATUS_SUCCESS = 1
EXECUTION_STATUS_ERROR = 2



_AUTOMATIONLOG = _descriptor.Descriptor(
  name='AutomationLog',
  full_name='calixa.domain.automation.log.AutomationLog',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='calixa.domain.automation.log.AutomationLog.id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='started_at', full_name='calixa.domain.automation.log.AutomationLog.started_at', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='finished_at', full_name='calixa.domain.automation.log.AutomationLog.finished_at', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='status', full_name='calixa.domain.automation.log.AutomationLog.status', index=3,
      number=4, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='entity', full_name='calixa.domain.automation.log.AutomationLog.entity', index=4,
      number=100, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='automation', full_name='calixa.domain.automation.log.AutomationLog.automation', index=5,
      number=101, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='error', full_name='calixa.domain.automation.log.AutomationLog.error', index=6,
      number=1000, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=102,
  serialized_end=401,
)

_AUTOMATIONLOG.fields_by_name['started_at'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_AUTOMATIONLOG.fields_by_name['finished_at'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_AUTOMATIONLOG.fields_by_name['status'].enum_type = _EXECUTIONSTATUS
_AUTOMATIONLOG.fields_by_name['entity'].message_type = entity__pb2._ENTITY
_AUTOMATIONLOG.fields_by_name['automation'].message_type = entity__pb2._ENTITY
DESCRIPTOR.message_types_by_name['AutomationLog'] = _AUTOMATIONLOG
DESCRIPTOR.enum_types_by_name['ExecutionStatus'] = _EXECUTIONSTATUS
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

AutomationLog = _reflection.GeneratedProtocolMessageType('AutomationLog', (_message.Message,), {
  'DESCRIPTOR' : _AUTOMATIONLOG,
  '__module__' : 'automation_log_pb2'
  # @@protoc_insertion_point(class_scope:calixa.domain.automation.log.AutomationLog)
  })
_sym_db.RegisterMessage(AutomationLog)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
