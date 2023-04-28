from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AttestationData(_message.Message):
    __slots__ = ["beacon_block_root", "committee_index", "slot", "source", "target"]
    BEACON_BLOCK_ROOT_FIELD_NUMBER: _ClassVar[int]
    COMMITTEE_INDEX_FIELD_NUMBER: _ClassVar[int]
    SLOT_FIELD_NUMBER: _ClassVar[int]
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    TARGET_FIELD_NUMBER: _ClassVar[int]
    beacon_block_root: bytes
    committee_index: int
    slot: int
    source: Checkpoint
    target: Checkpoint
    def __init__(self, slot: _Optional[int] = ..., committee_index: _Optional[int] = ..., beacon_block_root: _Optional[bytes] = ..., source: _Optional[_Union[Checkpoint, _Mapping]] = ..., target: _Optional[_Union[Checkpoint, _Mapping]] = ...) -> None: ...

class BeaconBlockHeader(_message.Message):
    __slots__ = ["body_root", "parent_root", "proposer_index", "slot", "state_root"]
    BODY_ROOT_FIELD_NUMBER: _ClassVar[int]
    PARENT_ROOT_FIELD_NUMBER: _ClassVar[int]
    PROPOSER_INDEX_FIELD_NUMBER: _ClassVar[int]
    SLOT_FIELD_NUMBER: _ClassVar[int]
    STATE_ROOT_FIELD_NUMBER: _ClassVar[int]
    body_root: bytes
    parent_root: bytes
    proposer_index: int
    slot: int
    state_root: bytes
    def __init__(self, slot: _Optional[int] = ..., proposer_index: _Optional[int] = ..., parent_root: _Optional[bytes] = ..., state_root: _Optional[bytes] = ..., body_root: _Optional[bytes] = ...) -> None: ...

class Checkpoint(_message.Message):
    __slots__ = ["epoch", "root"]
    EPOCH_FIELD_NUMBER: _ClassVar[int]
    ROOT_FIELD_NUMBER: _ClassVar[int]
    epoch: int
    root: bytes
    def __init__(self, epoch: _Optional[int] = ..., root: _Optional[bytes] = ...) -> None: ...
