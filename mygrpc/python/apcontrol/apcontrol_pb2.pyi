from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

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

class APLinks(_message.Message):
    __slots__ = ("src_dpid", "dst_dpid", "port_no")
    SRC_DPID_FIELD_NUMBER: _ClassVar[int]
    DST_DPID_FIELD_NUMBER: _ClassVar[int]
    PORT_NO_FIELD_NUMBER: _ClassVar[int]
    src_dpid: str
    dst_dpid: str
    port_no: int
    def __init__(self, src_dpid: _Optional[str] = ..., dst_dpid: _Optional[str] = ..., port_no: _Optional[int] = ...) -> None: ...

class APLinksResponse(_message.Message):
    __slots__ = ("ap_links",)
    AP_LINKS_FIELD_NUMBER: _ClassVar[int]
    ap_links: _containers.RepeatedCompositeFieldContainer[APLinks]
    def __init__(self, ap_links: _Optional[_Iterable[_Union[APLinks, _Mapping]]] = ...) -> None: ...
