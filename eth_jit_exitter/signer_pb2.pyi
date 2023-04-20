from google.api import annotations_pb2 as _annotations_pb2
import eth2_pb2 as _eth2_pb2
import responsestate_pb2 as _responsestate_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MultisignRequest(_message.Message):
    __slots__ = ["requests"]
    REQUESTS_FIELD_NUMBER: _ClassVar[int]
    requests: _containers.RepeatedCompositeFieldContainer[SignRequest]
    def __init__(self, requests: _Optional[_Iterable[_Union[SignRequest, _Mapping]]] = ...) -> None: ...

class MultisignResponse(_message.Message):
    __slots__ = ["responses"]
    RESPONSES_FIELD_NUMBER: _ClassVar[int]
    responses: _containers.RepeatedCompositeFieldContainer[SignResponse]
    def __init__(self, responses: _Optional[_Iterable[_Union[SignResponse, _Mapping]]] = ...) -> None: ...

class SignBeaconAttestationRequest(_message.Message):
    __slots__ = ["account", "data", "domain", "public_key"]
    ACCOUNT_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    DOMAIN_FIELD_NUMBER: _ClassVar[int]
    PUBLIC_KEY_FIELD_NUMBER: _ClassVar[int]
    account: str
    data: _eth2_pb2.AttestationData
    domain: bytes
    public_key: bytes
    def __init__(self, public_key: _Optional[bytes] = ..., account: _Optional[str] = ..., domain: _Optional[bytes] = ..., data: _Optional[_Union[_eth2_pb2.AttestationData, _Mapping]] = ...) -> None: ...

class SignBeaconAttestationsRequest(_message.Message):
    __slots__ = ["requests"]
    REQUESTS_FIELD_NUMBER: _ClassVar[int]
    requests: _containers.RepeatedCompositeFieldContainer[SignBeaconAttestationRequest]
    def __init__(self, requests: _Optional[_Iterable[_Union[SignBeaconAttestationRequest, _Mapping]]] = ...) -> None: ...

class SignBeaconProposalRequest(_message.Message):
    __slots__ = ["account", "data", "domain", "public_key"]
    ACCOUNT_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    DOMAIN_FIELD_NUMBER: _ClassVar[int]
    PUBLIC_KEY_FIELD_NUMBER: _ClassVar[int]
    account: str
    data: _eth2_pb2.BeaconBlockHeader
    domain: bytes
    public_key: bytes
    def __init__(self, public_key: _Optional[bytes] = ..., account: _Optional[str] = ..., domain: _Optional[bytes] = ..., data: _Optional[_Union[_eth2_pb2.BeaconBlockHeader, _Mapping]] = ...) -> None: ...

class SignRequest(_message.Message):
    __slots__ = ["account", "data", "domain", "public_key"]
    ACCOUNT_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    DOMAIN_FIELD_NUMBER: _ClassVar[int]
    PUBLIC_KEY_FIELD_NUMBER: _ClassVar[int]
    account: str
    data: bytes
    domain: bytes
    public_key: bytes
    def __init__(self, public_key: _Optional[bytes] = ..., account: _Optional[str] = ..., data: _Optional[bytes] = ..., domain: _Optional[bytes] = ...) -> None: ...

class SignResponse(_message.Message):
    __slots__ = ["signature", "state"]
    SIGNATURE_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    signature: bytes
    state: _responsestate_pb2.ResponseState
    def __init__(self, state: _Optional[_Union[_responsestate_pb2.ResponseState, str]] = ..., signature: _Optional[bytes] = ...) -> None: ...
