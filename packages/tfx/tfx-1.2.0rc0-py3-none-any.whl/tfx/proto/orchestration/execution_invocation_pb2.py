# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: tfx/proto/orchestration/execution_invocation.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from ml_metadata.proto import metadata_store_pb2 as ml__metadata_dot_proto_dot_metadata__store__pb2
from ml_metadata.proto import metadata_store_service_pb2 as ml__metadata_dot_proto_dot_metadata__store__service__pb2
from tfx.proto.orchestration import pipeline_pb2 as tfx_dot_proto_dot_orchestration_dot_pipeline__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='tfx/proto/orchestration/execution_invocation.proto',
  package='tfx.orchestration',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=_b('\n2tfx/proto/orchestration/execution_invocation.proto\x12\x11tfx.orchestration\x1a&ml_metadata/proto/metadata_store.proto\x1a.ml_metadata/proto/metadata_store_service.proto\x1a&tfx/proto/orchestration/pipeline.proto\"\xfa\x05\n\x13\x45xecutionInvocation\x12]\n\x14\x65xecution_properties\x18\x03 \x03(\x0b\x32?.tfx.orchestration.ExecutionInvocation.ExecutionPropertiesEntry\x12\x1b\n\x13output_metadata_uri\x18\x04 \x01(\t\x12I\n\ninput_dict\x18\x05 \x03(\x0b\x32\x35.tfx.orchestration.ExecutionInvocation.InputDictEntry\x12K\n\x0boutput_dict\x18\x06 \x03(\x0b\x32\x36.tfx.orchestration.ExecutionInvocation.OutputDictEntry\x12\x1c\n\x14stateful_working_dir\x18\x07 \x01(\t\x12\x0f\n\x07tmp_dir\x18\n \x01(\t\x12\x36\n\rpipeline_info\x18\x08 \x01(\x0b\x32\x1f.tfx.orchestration.PipelineInfo\x12\x36\n\rpipeline_node\x18\t \x01(\x0b\x32\x1f.tfx.orchestration.PipelineNode\x12\x14\n\x0c\x65xecution_id\x18\x0b \x01(\x03\x12\x17\n\x0fpipeline_run_id\x18\x0c \x01(\t\x1aN\n\x18\x45xecutionPropertiesEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12!\n\x05value\x18\x02 \x01(\x0b\x32\x12.ml_metadata.Value:\x02\x38\x01\x1aQ\n\x0eInputDictEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12.\n\x05value\x18\x02 \x01(\x0b\x32\x1f.ml_metadata.ArtifactStructList:\x02\x38\x01\x1aR\n\x0fOutputDictEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12.\n\x05value\x18\x02 \x01(\x0b\x32\x1f.ml_metadata.ArtifactStructList:\x02\x38\x01J\x04\x08\x01\x10\x02J\x04\x08\x02\x10\x03\"\xc2\x01\n\x14MLMDConnectionConfig\x12\x43\n\x1a\x64\x61tabase_connection_config\x18\x01 \x01(\x0b\x32\x1d.ml_metadata.ConnectionConfigH\x00\x12J\n\x18mlmd_store_client_config\x18\x02 \x01(\x0b\x32&.ml_metadata.MetadataStoreClientConfigH\x00\x42\x13\n\x11\x63onnection_configJ\x04\x08\x03\x10\x04\x62\x06proto3')
  ,
  dependencies=[ml__metadata_dot_proto_dot_metadata__store__pb2.DESCRIPTOR,ml__metadata_dot_proto_dot_metadata__store__service__pb2.DESCRIPTOR,tfx_dot_proto_dot_orchestration_dot_pipeline__pb2.DESCRIPTOR,])




_EXECUTIONINVOCATION_EXECUTIONPROPERTIESENTRY = _descriptor.Descriptor(
  name='ExecutionPropertiesEntry',
  full_name='tfx.orchestration.ExecutionInvocation.ExecutionPropertiesEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='tfx.orchestration.ExecutionInvocation.ExecutionPropertiesEntry.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='value', full_name='tfx.orchestration.ExecutionInvocation.ExecutionPropertiesEntry.value', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=_b('8\001'),
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=707,
  serialized_end=785,
)

_EXECUTIONINVOCATION_INPUTDICTENTRY = _descriptor.Descriptor(
  name='InputDictEntry',
  full_name='tfx.orchestration.ExecutionInvocation.InputDictEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='tfx.orchestration.ExecutionInvocation.InputDictEntry.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='value', full_name='tfx.orchestration.ExecutionInvocation.InputDictEntry.value', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=_b('8\001'),
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=787,
  serialized_end=868,
)

_EXECUTIONINVOCATION_OUTPUTDICTENTRY = _descriptor.Descriptor(
  name='OutputDictEntry',
  full_name='tfx.orchestration.ExecutionInvocation.OutputDictEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='tfx.orchestration.ExecutionInvocation.OutputDictEntry.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='value', full_name='tfx.orchestration.ExecutionInvocation.OutputDictEntry.value', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=_b('8\001'),
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=870,
  serialized_end=952,
)

_EXECUTIONINVOCATION = _descriptor.Descriptor(
  name='ExecutionInvocation',
  full_name='tfx.orchestration.ExecutionInvocation',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='execution_properties', full_name='tfx.orchestration.ExecutionInvocation.execution_properties', index=0,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='output_metadata_uri', full_name='tfx.orchestration.ExecutionInvocation.output_metadata_uri', index=1,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='input_dict', full_name='tfx.orchestration.ExecutionInvocation.input_dict', index=2,
      number=5, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='output_dict', full_name='tfx.orchestration.ExecutionInvocation.output_dict', index=3,
      number=6, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='stateful_working_dir', full_name='tfx.orchestration.ExecutionInvocation.stateful_working_dir', index=4,
      number=7, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='tmp_dir', full_name='tfx.orchestration.ExecutionInvocation.tmp_dir', index=5,
      number=10, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='pipeline_info', full_name='tfx.orchestration.ExecutionInvocation.pipeline_info', index=6,
      number=8, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='pipeline_node', full_name='tfx.orchestration.ExecutionInvocation.pipeline_node', index=7,
      number=9, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='execution_id', full_name='tfx.orchestration.ExecutionInvocation.execution_id', index=8,
      number=11, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='pipeline_run_id', full_name='tfx.orchestration.ExecutionInvocation.pipeline_run_id', index=9,
      number=12, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[_EXECUTIONINVOCATION_EXECUTIONPROPERTIESENTRY, _EXECUTIONINVOCATION_INPUTDICTENTRY, _EXECUTIONINVOCATION_OUTPUTDICTENTRY, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=202,
  serialized_end=964,
)


_MLMDCONNECTIONCONFIG = _descriptor.Descriptor(
  name='MLMDConnectionConfig',
  full_name='tfx.orchestration.MLMDConnectionConfig',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='database_connection_config', full_name='tfx.orchestration.MLMDConnectionConfig.database_connection_config', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='mlmd_store_client_config', full_name='tfx.orchestration.MLMDConnectionConfig.mlmd_store_client_config', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
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
    _descriptor.OneofDescriptor(
      name='connection_config', full_name='tfx.orchestration.MLMDConnectionConfig.connection_config',
      index=0, containing_type=None, fields=[]),
  ],
  serialized_start=967,
  serialized_end=1161,
)

_EXECUTIONINVOCATION_EXECUTIONPROPERTIESENTRY.fields_by_name['value'].message_type = ml__metadata_dot_proto_dot_metadata__store__pb2._VALUE
_EXECUTIONINVOCATION_EXECUTIONPROPERTIESENTRY.containing_type = _EXECUTIONINVOCATION
_EXECUTIONINVOCATION_INPUTDICTENTRY.fields_by_name['value'].message_type = ml__metadata_dot_proto_dot_metadata__store__service__pb2._ARTIFACTSTRUCTLIST
_EXECUTIONINVOCATION_INPUTDICTENTRY.containing_type = _EXECUTIONINVOCATION
_EXECUTIONINVOCATION_OUTPUTDICTENTRY.fields_by_name['value'].message_type = ml__metadata_dot_proto_dot_metadata__store__service__pb2._ARTIFACTSTRUCTLIST
_EXECUTIONINVOCATION_OUTPUTDICTENTRY.containing_type = _EXECUTIONINVOCATION
_EXECUTIONINVOCATION.fields_by_name['execution_properties'].message_type = _EXECUTIONINVOCATION_EXECUTIONPROPERTIESENTRY
_EXECUTIONINVOCATION.fields_by_name['input_dict'].message_type = _EXECUTIONINVOCATION_INPUTDICTENTRY
_EXECUTIONINVOCATION.fields_by_name['output_dict'].message_type = _EXECUTIONINVOCATION_OUTPUTDICTENTRY
_EXECUTIONINVOCATION.fields_by_name['pipeline_info'].message_type = tfx_dot_proto_dot_orchestration_dot_pipeline__pb2._PIPELINEINFO
_EXECUTIONINVOCATION.fields_by_name['pipeline_node'].message_type = tfx_dot_proto_dot_orchestration_dot_pipeline__pb2._PIPELINENODE
_MLMDCONNECTIONCONFIG.fields_by_name['database_connection_config'].message_type = ml__metadata_dot_proto_dot_metadata__store__pb2._CONNECTIONCONFIG
_MLMDCONNECTIONCONFIG.fields_by_name['mlmd_store_client_config'].message_type = ml__metadata_dot_proto_dot_metadata__store__pb2._METADATASTORECLIENTCONFIG
_MLMDCONNECTIONCONFIG.oneofs_by_name['connection_config'].fields.append(
  _MLMDCONNECTIONCONFIG.fields_by_name['database_connection_config'])
_MLMDCONNECTIONCONFIG.fields_by_name['database_connection_config'].containing_oneof = _MLMDCONNECTIONCONFIG.oneofs_by_name['connection_config']
_MLMDCONNECTIONCONFIG.oneofs_by_name['connection_config'].fields.append(
  _MLMDCONNECTIONCONFIG.fields_by_name['mlmd_store_client_config'])
_MLMDCONNECTIONCONFIG.fields_by_name['mlmd_store_client_config'].containing_oneof = _MLMDCONNECTIONCONFIG.oneofs_by_name['connection_config']
DESCRIPTOR.message_types_by_name['ExecutionInvocation'] = _EXECUTIONINVOCATION
DESCRIPTOR.message_types_by_name['MLMDConnectionConfig'] = _MLMDCONNECTIONCONFIG
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

ExecutionInvocation = _reflection.GeneratedProtocolMessageType('ExecutionInvocation', (_message.Message,), {

  'ExecutionPropertiesEntry' : _reflection.GeneratedProtocolMessageType('ExecutionPropertiesEntry', (_message.Message,), {
    'DESCRIPTOR' : _EXECUTIONINVOCATION_EXECUTIONPROPERTIESENTRY,
    '__module__' : 'tfx.proto.orchestration.execution_invocation_pb2'
    # @@protoc_insertion_point(class_scope:tfx.orchestration.ExecutionInvocation.ExecutionPropertiesEntry)
    })
  ,

  'InputDictEntry' : _reflection.GeneratedProtocolMessageType('InputDictEntry', (_message.Message,), {
    'DESCRIPTOR' : _EXECUTIONINVOCATION_INPUTDICTENTRY,
    '__module__' : 'tfx.proto.orchestration.execution_invocation_pb2'
    # @@protoc_insertion_point(class_scope:tfx.orchestration.ExecutionInvocation.InputDictEntry)
    })
  ,

  'OutputDictEntry' : _reflection.GeneratedProtocolMessageType('OutputDictEntry', (_message.Message,), {
    'DESCRIPTOR' : _EXECUTIONINVOCATION_OUTPUTDICTENTRY,
    '__module__' : 'tfx.proto.orchestration.execution_invocation_pb2'
    # @@protoc_insertion_point(class_scope:tfx.orchestration.ExecutionInvocation.OutputDictEntry)
    })
  ,
  'DESCRIPTOR' : _EXECUTIONINVOCATION,
  '__module__' : 'tfx.proto.orchestration.execution_invocation_pb2'
  # @@protoc_insertion_point(class_scope:tfx.orchestration.ExecutionInvocation)
  })
_sym_db.RegisterMessage(ExecutionInvocation)
_sym_db.RegisterMessage(ExecutionInvocation.ExecutionPropertiesEntry)
_sym_db.RegisterMessage(ExecutionInvocation.InputDictEntry)
_sym_db.RegisterMessage(ExecutionInvocation.OutputDictEntry)

MLMDConnectionConfig = _reflection.GeneratedProtocolMessageType('MLMDConnectionConfig', (_message.Message,), {
  'DESCRIPTOR' : _MLMDCONNECTIONCONFIG,
  '__module__' : 'tfx.proto.orchestration.execution_invocation_pb2'
  # @@protoc_insertion_point(class_scope:tfx.orchestration.MLMDConnectionConfig)
  })
_sym_db.RegisterMessage(MLMDConnectionConfig)


_EXECUTIONINVOCATION_EXECUTIONPROPERTIESENTRY._options = None
_EXECUTIONINVOCATION_INPUTDICTENTRY._options = None
_EXECUTIONINVOCATION_OUTPUTDICTENTRY._options = None
# @@protoc_insertion_point(module_scope)
