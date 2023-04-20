from google.api import annotations_pb2 as _annotations_pb2
import endpoint_pb2 as _endpoint_pb2
import responsestate_pb2 as _responsestate_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Account(_message.Message):
    __slots__ = ["name", "public_key", "uuid"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    PUBLIC_KEY_FIELD_NUMBER: _ClassVar[int]
    UUID_FIELD_NUMBER: _ClassVar[int]
    name: str
    public_key: bytes
    uuid: bytes
    def __init__(self, name: _Optional[str] = ..., public_key: _Optional[bytes] = ..., uuid: _Optional[bytes] = ...) -> None: ...

class DistributedAccount(_message.Message):
    __slots__ = ["composite_public_key", "name", "participants", "public_key", "signing_threshold", "uuid"]
    COMPOSITE_PUBLIC_KEY_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    PARTICIPANTS_FIELD_NUMBER: _ClassVar[int]
    PUBLIC_KEY_FIELD_NUMBER: _ClassVar[int]
    SIGNING_THRESHOLD_FIELD_NUMBER: _ClassVar[int]
    UUID_FIELD_NUMBER: _ClassVar[int]
    composite_public_key: bytes
    name: str
    participants: _containers.RepeatedCompositeFieldContainer[_endpoint_pb2.Endpoint]
    public_key: bytes
    signing_threshold: int
    uuid: bytes
    def __init__(self, name: _Optional[str] = ..., public_key: _Optional[bytes] = ..., participants: _Optional[_Iterable[_Union[_endpoint_pb2.Endpoint, _Mapping]]] = ..., signing_threshold: _Optional[int] = ..., uuid: _Optional[bytes] = ..., composite_public_key: _Optional[bytes] = ...) -> None: ...

class ListAccountsRequest(_message.Message):
    __slots__ = ["paths"]
    PATHS_FIELD_NUMBER: _ClassVar[int]
    paths: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, paths: _Optional[_Iterable[str]] = ...) -> None: ...

class ListAccountsResponse(_message.Message):
    __slots__ = ["Accounts", "DistributedAccounts", "state"]
    ACCOUNTS_FIELD_NUMBER: _ClassVar[int]
    Accounts: _containers.RepeatedCompositeFieldContainer[Account]
    DISTRIBUTEDACCOUNTS_FIELD_NUMBER: _ClassVar[int]
    DistributedAccounts: _containers.RepeatedCompositeFieldContainer[DistributedAccount]
    STATE_FIELD_NUMBER: _ClassVar[int]
    state: _responsestate_pb2.ResponseState
    def __init__(self, state: _Optional[_Union[_responsestate_pb2.ResponseState, str]] = ..., Accounts: _Optional[_Iterable[_Union[Account, _Mapping]]] = ..., DistributedAccounts: _Optional[_Iterable[_Union[DistributedAccount, _Mapping]]] = ...) -> None: ...
