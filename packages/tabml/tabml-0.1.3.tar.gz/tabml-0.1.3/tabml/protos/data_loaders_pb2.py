# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: tabml/protos/data_loaders.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='tabml/protos/data_loaders.proto',
  package='tabml.protos',
  syntax='proto2',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x1ftabml/protos/data_loaders.proto\x12\x0ctabml.protos\"\x88\x02\n\nDataLoader\x12\x10\n\x08\x63ls_name\x18\x01 \x02(\t\x12\x12\n\nbatch_size\x18\x02 \x01(\x05\x12\x1c\n\rgen_profiling\x18\x03 \x01(\x08:\x05\x66\x61lse\x12#\n\x1b\x66\x65\x61ture_manager_config_path\x18\x04 \x01(\t\x12\x19\n\x11\x66\x65\x61tures_to_model\x18\x05 \x03(\t\x12\x15\n\rtrain_filters\x18\x06 \x03(\t\x12\x1a\n\x12validation_filters\x18\x07 \x03(\t\x12\x1a\n\x12submission_filters\x18\x08 \x03(\t\x12\x14\n\x0ctest_filters\x18\t \x03(\t\x12\x11\n\tlabel_col\x18\n \x01(\t'
)




_DATALOADER = _descriptor.Descriptor(
  name='DataLoader',
  full_name='tabml.protos.DataLoader',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='cls_name', full_name='tabml.protos.DataLoader.cls_name', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='batch_size', full_name='tabml.protos.DataLoader.batch_size', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='gen_profiling', full_name='tabml.protos.DataLoader.gen_profiling', index=2,
      number=3, type=8, cpp_type=7, label=1,
      has_default_value=True, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='feature_manager_config_path', full_name='tabml.protos.DataLoader.feature_manager_config_path', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='features_to_model', full_name='tabml.protos.DataLoader.features_to_model', index=4,
      number=5, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='train_filters', full_name='tabml.protos.DataLoader.train_filters', index=5,
      number=6, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='validation_filters', full_name='tabml.protos.DataLoader.validation_filters', index=6,
      number=7, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='submission_filters', full_name='tabml.protos.DataLoader.submission_filters', index=7,
      number=8, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='test_filters', full_name='tabml.protos.DataLoader.test_filters', index=8,
      number=9, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='label_col', full_name='tabml.protos.DataLoader.label_col', index=9,
      number=10, type=9, cpp_type=9, label=1,
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
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=50,
  serialized_end=314,
)

DESCRIPTOR.message_types_by_name['DataLoader'] = _DATALOADER
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

DataLoader = _reflection.GeneratedProtocolMessageType('DataLoader', (_message.Message,), {
  'DESCRIPTOR' : _DATALOADER,
  '__module__' : 'tabml.protos.data_loaders_pb2'
  # @@protoc_insertion_point(class_scope:tabml.protos.DataLoader)
  })
_sym_db.RegisterMessage(DataLoader)


# @@protoc_insertion_point(module_scope)
