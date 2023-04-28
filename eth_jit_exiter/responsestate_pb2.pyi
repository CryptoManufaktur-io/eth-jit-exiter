from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from typing import ClassVar as _ClassVar

DENIED: ResponseState
DESCRIPTOR: _descriptor.FileDescriptor
FAILED: ResponseState
SUCCEEDED: ResponseState
UNKNOWN: ResponseState

class ResponseState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
