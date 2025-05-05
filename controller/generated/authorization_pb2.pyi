from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class SendSUB(_message.Message):
    __slots__ = ("user_id",)
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    def __init__(self, user_id: _Optional[str] = ...) -> None: ...

class SendToken(_message.Message):
    __slots__ = ("token",)
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    token: str
    def __init__(self, token: _Optional[str] = ...) -> None: ...

class ReturnTokens(_message.Message):
    __slots__ = ("access", "refresh")
    ACCESS_FIELD_NUMBER: _ClassVar[int]
    REFRESH_FIELD_NUMBER: _ClassVar[int]
    access: str
    refresh: str
    def __init__(self, access: _Optional[str] = ..., refresh: _Optional[str] = ...) -> None: ...

class ReturnAccess(_message.Message):
    __slots__ = ("access",)
    ACCESS_FIELD_NUMBER: _ClassVar[int]
    access: str
    def __init__(self, access: _Optional[str] = ...) -> None: ...

class ReturnRefresh(_message.Message):
    __slots__ = ("refresh",)
    REFRESH_FIELD_NUMBER: _ClassVar[int]
    refresh: str
    def __init__(self, refresh: _Optional[str] = ...) -> None: ...

class ReturnUserId(_message.Message):
    __slots__ = ("user_id",)
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    def __init__(self, user_id: _Optional[str] = ...) -> None: ...

class ReturnLogoutState(_message.Message):
    __slots__ = ("message",)
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    message: str
    def __init__(self, message: _Optional[str] = ...) -> None: ...
