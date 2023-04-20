# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: signer.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
from eth_jit_exitter import eth2_pb2 as eth2__pb2
from eth_jit_exitter import responsestate_pb2 as responsestate__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0csigner.proto\x12\x02v1\x1a\x1cgoogle/api/annotations.proto\x1a\neth2.proto\x1a\x13responsestate.proto\"Z\n\x0bSignRequest\x12\x14\n\npublic_key\x18\x01 \x01(\x0cH\x00\x12\x11\n\x07\x61\x63\x63ount\x18\x02 \x01(\tH\x00\x12\x0c\n\x04\x64\x61ta\x18\x03 \x01(\x0c\x12\x0e\n\x06\x64omain\x18\x04 \x01(\x0c\x42\x04\n\x02id\"5\n\x10MultisignRequest\x12!\n\x08requests\x18\x01 \x03(\x0b\x32\x0f.v1.SignRequest\"\x80\x01\n\x1cSignBeaconAttestationRequest\x12\x14\n\npublic_key\x18\x01 \x01(\x0cH\x00\x12\x11\n\x07\x61\x63\x63ount\x18\x02 \x01(\tH\x00\x12\x0e\n\x06\x64omain\x18\x03 \x01(\x0c\x12!\n\x04\x64\x61ta\x18\x04 \x01(\x0b\x32\x13.v1.AttestationDataB\x04\n\x02id\"S\n\x1dSignBeaconAttestationsRequest\x12\x32\n\x08requests\x18\x01 \x03(\x0b\x32 .v1.SignBeaconAttestationRequest\"\x7f\n\x19SignBeaconProposalRequest\x12\x14\n\npublic_key\x18\x01 \x01(\x0cH\x00\x12\x11\n\x07\x61\x63\x63ount\x18\x02 \x01(\tH\x00\x12\x0e\n\x06\x64omain\x18\x03 \x01(\x0c\x12#\n\x04\x64\x61ta\x18\x04 \x01(\x0b\x32\x15.v1.BeaconBlockHeaderB\x04\n\x02id\"C\n\x0cSignResponse\x12 \n\x05state\x18\x01 \x01(\x0e\x32\x11.v1.ResponseState\x12\x11\n\tsignature\x18\x02 \x01(\x0c\"8\n\x11MultisignResponse\x12#\n\tresponses\x18\x01 \x03(\x0b\x32\x10.v1.SignResponse2\x88\x04\n\x06Signer\x12\x42\n\x04Sign\x12\x0f.v1.SignRequest\x1a\x10.v1.SignResponse\"\x17\x82\xd3\xe4\x93\x02\x11\x12\x0f/v1/signer/sign\x12V\n\tMultisign\x12\x14.v1.MultisignRequest\x1a\x15.v1.MultisignResponse\"\x1c\x82\xd3\xe4\x93\x02\x16\x12\x14/v1/signer/multisign\x12u\n\x15SignBeaconAttestation\x12 .v1.SignBeaconAttestationRequest\x1a\x10.v1.SignResponse\"(\x82\xd3\xe4\x93\x02\"\x12 /v1/signer/signbeaconattestation\x12}\n\x16SignBeaconAttestations\x12!.v1.SignBeaconAttestationsRequest\x1a\x15.v1.MultisignResponse\")\x82\xd3\xe4\x93\x02#\x12!/v1/signer/signbeaconattestations\x12l\n\x12SignBeaconProposal\x12\x1d.v1.SignBeaconProposalRequest\x1a\x10.v1.SignResponse\"%\x82\xd3\xe4\x93\x02\x1f\x12\x1d/v1/signer/signbeaconproposalB{\n\x1e\x63om.wealdtech.eth2signerapi.v1B\x0bSignerProtoP\x01Z*github.com/wealdtech/eth2-signer-api/pb/v1\xaa\x02\rEth2Signer.v1\xca\x02\rEth2Signer\\v1b\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'signer_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\036com.wealdtech.eth2signerapi.v1B\013SignerProtoP\001Z*github.com/wealdtech/eth2-signer-api/pb/v1\252\002\rEth2Signer.v1\312\002\rEth2Signer\\v1'
  _SIGNER.methods_by_name['Sign']._options = None
  _SIGNER.methods_by_name['Sign']._serialized_options = b'\202\323\344\223\002\021\022\017/v1/signer/sign'
  _SIGNER.methods_by_name['Multisign']._options = None
  _SIGNER.methods_by_name['Multisign']._serialized_options = b'\202\323\344\223\002\026\022\024/v1/signer/multisign'
  _SIGNER.methods_by_name['SignBeaconAttestation']._options = None
  _SIGNER.methods_by_name['SignBeaconAttestation']._serialized_options = b'\202\323\344\223\002\"\022 /v1/signer/signbeaconattestation'
  _SIGNER.methods_by_name['SignBeaconAttestations']._options = None
  _SIGNER.methods_by_name['SignBeaconAttestations']._serialized_options = b'\202\323\344\223\002#\022!/v1/signer/signbeaconattestations'
  _SIGNER.methods_by_name['SignBeaconProposal']._options = None
  _SIGNER.methods_by_name['SignBeaconProposal']._serialized_options = b'\202\323\344\223\002\037\022\035/v1/signer/signbeaconproposal'
  _SIGNREQUEST._serialized_start=83
  _SIGNREQUEST._serialized_end=173
  _MULTISIGNREQUEST._serialized_start=175
  _MULTISIGNREQUEST._serialized_end=228
  _SIGNBEACONATTESTATIONREQUEST._serialized_start=231
  _SIGNBEACONATTESTATIONREQUEST._serialized_end=359
  _SIGNBEACONATTESTATIONSREQUEST._serialized_start=361
  _SIGNBEACONATTESTATIONSREQUEST._serialized_end=444
  _SIGNBEACONPROPOSALREQUEST._serialized_start=446
  _SIGNBEACONPROPOSALREQUEST._serialized_end=573
  _SIGNRESPONSE._serialized_start=575
  _SIGNRESPONSE._serialized_end=642
  _MULTISIGNRESPONSE._serialized_start=644
  _MULTISIGNRESPONSE._serialized_end=700
  _SIGNER._serialized_start=703
  _SIGNER._serialized_end=1223
# @@protoc_insertion_point(module_scope)
