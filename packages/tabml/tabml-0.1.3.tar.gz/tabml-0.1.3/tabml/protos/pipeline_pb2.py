# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: tabml/protos/pipeline.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from tabml.protos import model_wrappers_pb2 as tabml_dot_protos_dot_model__wrappers__pb2
from tabml.protos import trainers_pb2 as tabml_dot_protos_dot_trainers__pb2
from tabml.protos import data_loaders_pb2 as tabml_dot_protos_dot_data__loaders__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='tabml/protos/pipeline.proto',
  package='tabml.protos',
  syntax='proto2',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x1btabml/protos/pipeline.proto\x12\x0ctabml.protos\x1a!tabml/protos/model_wrappers.proto\x1a\x1btabml/protos/trainers.proto\x1a\x1ftabml/protos/data_loaders.proto\"5\n\rModelAnalysis\x12\x0f\n\x07metrics\x18\x01 \x03(\t\x12\x13\n\x0b\x62y_features\x18\x02 \x03(\t\" \n\x05Saver\x12\x17\n\x0fsubmission_name\x18\x01 \x01(\t\"\x80\x02\n\x06\x43onfig\x12\x13\n\x0b\x63onfig_name\x18\x07 \x02(\t\x12-\n\x0b\x64\x61ta_loader\x18\x01 \x02(\x0b\x32\x18.tabml.protos.DataLoader\x12\x31\n\rmodel_wrapper\x18\x02 \x02(\x0b\x32\x1a.tabml.protos.ModelWrapper\x12&\n\x07trainer\x18\x03 \x02(\x0b\x32\x15.tabml.protos.Trainer\x12\x33\n\x0emodel_analysis\x18\x08 \x01(\x0b\x32\x1b.tabml.protos.ModelAnalysis\x12\"\n\x05saver\x18\x05 \x01(\x0b\x32\x13.tabml.protos.Saver'
  ,
  dependencies=[tabml_dot_protos_dot_model__wrappers__pb2.DESCRIPTOR,tabml_dot_protos_dot_trainers__pb2.DESCRIPTOR,tabml_dot_protos_dot_data__loaders__pb2.DESCRIPTOR,])




_MODELANALYSIS = _descriptor.Descriptor(
  name='ModelAnalysis',
  full_name='tabml.protos.ModelAnalysis',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='metrics', full_name='tabml.protos.ModelAnalysis.metrics', index=0,
      number=1, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='by_features', full_name='tabml.protos.ModelAnalysis.by_features', index=1,
      number=2, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
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
  serialized_start=142,
  serialized_end=195,
)


_SAVER = _descriptor.Descriptor(
  name='Saver',
  full_name='tabml.protos.Saver',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='submission_name', full_name='tabml.protos.Saver.submission_name', index=0,
      number=1, type=9, cpp_type=9, label=1,
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
  serialized_start=197,
  serialized_end=229,
)


_CONFIG = _descriptor.Descriptor(
  name='Config',
  full_name='tabml.protos.Config',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='config_name', full_name='tabml.protos.Config.config_name', index=0,
      number=7, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='data_loader', full_name='tabml.protos.Config.data_loader', index=1,
      number=1, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='model_wrapper', full_name='tabml.protos.Config.model_wrapper', index=2,
      number=2, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='trainer', full_name='tabml.protos.Config.trainer', index=3,
      number=3, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='model_analysis', full_name='tabml.protos.Config.model_analysis', index=4,
      number=8, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='saver', full_name='tabml.protos.Config.saver', index=5,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
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
  serialized_start=232,
  serialized_end=488,
)

_CONFIG.fields_by_name['data_loader'].message_type = tabml_dot_protos_dot_data__loaders__pb2._DATALOADER
_CONFIG.fields_by_name['model_wrapper'].message_type = tabml_dot_protos_dot_model__wrappers__pb2._MODELWRAPPER
_CONFIG.fields_by_name['trainer'].message_type = tabml_dot_protos_dot_trainers__pb2._TRAINER
_CONFIG.fields_by_name['model_analysis'].message_type = _MODELANALYSIS
_CONFIG.fields_by_name['saver'].message_type = _SAVER
DESCRIPTOR.message_types_by_name['ModelAnalysis'] = _MODELANALYSIS
DESCRIPTOR.message_types_by_name['Saver'] = _SAVER
DESCRIPTOR.message_types_by_name['Config'] = _CONFIG
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

ModelAnalysis = _reflection.GeneratedProtocolMessageType('ModelAnalysis', (_message.Message,), {
  'DESCRIPTOR' : _MODELANALYSIS,
  '__module__' : 'tabml.protos.pipeline_pb2'
  # @@protoc_insertion_point(class_scope:tabml.protos.ModelAnalysis)
  })
_sym_db.RegisterMessage(ModelAnalysis)

Saver = _reflection.GeneratedProtocolMessageType('Saver', (_message.Message,), {
  'DESCRIPTOR' : _SAVER,
  '__module__' : 'tabml.protos.pipeline_pb2'
  # @@protoc_insertion_point(class_scope:tabml.protos.Saver)
  })
_sym_db.RegisterMessage(Saver)

Config = _reflection.GeneratedProtocolMessageType('Config', (_message.Message,), {
  'DESCRIPTOR' : _CONFIG,
  '__module__' : 'tabml.protos.pipeline_pb2'
  # @@protoc_insertion_point(class_scope:tabml.protos.Config)
  })
_sym_db.RegisterMessage(Config)


# @@protoc_insertion_point(module_scope)
