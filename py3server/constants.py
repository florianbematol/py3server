from enum import IntEnum, Enum


class LogLevel(IntEnum):
    """"""
    TRACE = 0
    DEBUG = 1
    INFO = 2
    WARN = 3
    ERROR = 4
    FATAL = 5


class HttpMethod(Enum):
    """"""
    NONE = 'NONE'
    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'
    DELETE = 'DELETE'


class Decorator(Enum):
    """"""
    CONTROLLER = 'CONTROLLER'
    SERVICE = 'SERVICE'
    REPOSITORY = 'REPOSITORY'


class MediaType(Enum):
    """"""
    NONE = 'NONE'
    APPLICATION_JSON = 'application/json'
    TEXT_PLAIN = 'text/plain'
