from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class APInfoRequest(_message.Message):
    __slots__ = ("dpid", "portName")
    DPID_FIELD_NUMBER: _ClassVar[int]
    PORTNAME_FIELD_NUMBER: _ClassVar[int]
    dpid: str
    portName: str
    def __init__(self, dpid: _Optional[str] = ..., portName: _Optional[str] = ...) -> None: ...

class APInfoReply(_message.Message):
    __slots__ = ("status",)
    STATUS_FIELD_NUMBER: _ClassVar[int]
    status: str
    def __init__(self, status: _Optional[str] = ...) -> None: ...
