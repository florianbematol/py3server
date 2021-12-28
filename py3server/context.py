import http.server
import logging
import typing as t

from py3server.app.exception import ExceptionHandler
from py3server.app.repository import Repository
from py3server.app.service import Service
from py3server.constants import HttpMethod, Decorator
from py3server.utils.singleton import SingletonMeta
from py3server.web.controllers.rest_controller import RestController
from py3server.web.response import Response
from py3server.web.route_context import RouteContext

T = t.TypeVar('T')
DecoratedObj = t.Union[RestController, Repository, Service]


class Context(metaclass=SingletonMeta):
    """"""
    logger: logging.Logger = logging.getLogger(__name__)

    def __init__(self) -> None:
        """"""
        self.logger.info('init context')
        self.instances: t.Dict[hash, T] = {}
        self.decorators: t.Dict[Decorator, t.List[DecoratedObj]] = dict(
            [(x, []) for x in Decorator])
        self.route_contexts: t.Dict[HttpMethod, t.List[RouteContext]] = dict([(x, []) for x in HttpMethod])
        self.exception_handlers: t.List[ExceptionHandler] = []

    def add_decorator(self, decorator: Decorator, obj: DecoratedObj):
        """"""
        self.decorators[decorator].append(obj)

    def add_route_ctx(self, route_ctx: RouteContext) -> None:
        """"""
        self.route_contexts[route_ctx.method].append(route_ctx)

    def add_exception_handler(self, exception_handler: ExceptionHandler) -> None:
        """"""
        self.exception_handlers.append(exception_handler)

    def get_clazz_instance(self, clazz: object) -> any:
        """"""
        h = hash(clazz)
        if not self.instances.get(h):
            self.instances[h] = clazz()
        return self.instances[h]

    def get_route_ctx(self, method: HttpMethod, req: http.server.BaseHTTPRequestHandler) -> any:
        """"""
        route_ctx: t.Optional[object] = None

        for _route_ctx in self.route_contexts.get(method, []):
            if _route_ctx.match_request(req):
                route_ctx = _route_ctx
                break

        if route_ctx is None:
            raise Exception(f'No route matching: {req.path}')

        return route_ctx

    def handle_exception(self, exception: Exception) -> Response:
        """"""
        response: t.Optional[Response] = None

        for _exception in self.exception_handlers:
            print(_exception._type)
            if isinstance(exception, _exception._type):
                response: Response = _exception.handle_exception(exception)
                break
        return response
