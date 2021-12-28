import http.server
from unittest.mock import Mock

import pytest

from py3server.app.exception import ExceptionHandler
from py3server.app.repository import Repository
from py3server.app.service import Service
from py3server.constants import Decorator, HttpMethod
from py3server.context import Context
from py3server.web.controllers.rest_controller import RestController
from py3server.web.route_context import RouteContext


def test_context_is_singleton():
    # GIVEN
    context1: Context = Context()

    # WHEN
    context2: Context = Context()

    # THEN
    assert context1 == context2


def test_context_add_decorator():
    # GIVEN
    context: Context = Context()
    fake_controller: RestController = Mock(RestController)
    fake_service: Service = Mock(Service)
    fake_repository: Repository = Mock(Repository)

    # WHEN
    context.add_decorator(Decorator.CONTROLLER, fake_controller)
    context.add_decorator(Decorator.SERVICE, fake_service)
    context.add_decorator(Decorator.REPOSITORY, fake_repository)

    # THEN
    assert len(context.decorators[Decorator.CONTROLLER]) == 1
    assert context.decorators[Decorator.CONTROLLER][0] == fake_controller

    assert len(context.decorators[Decorator.SERVICE]) == 1
    assert context.decorators[Decorator.SERVICE][0] == fake_service

    assert len(context.decorators[Decorator.REPOSITORY]) == 1
    assert context.decorators[Decorator.REPOSITORY][0] == fake_repository


def test_context_add_route_ctx():
    # GIVEN
    context: Context = Context()
    route_ctx: RouteContext = Mock(spec=RouteContext)
    route_ctx.method = HttpMethod.GET

    # WHEN
    context.add_route_ctx(route_ctx)

    # THEN
    assert len(context.route_contexts[route_ctx.method]) == 1
    assert context.route_contexts[route_ctx.method][0] == route_ctx


def test_context_add_exception_handler():
    # GIVEN
    context: Context = Context()
    exception_handler: ExceptionHandler = Mock(ExceptionHandler)

    # WHEN
    context.add_exception_handler(exception_handler)

    # THEN
    assert len(context.exception_handlers) == 1
    assert context.exception_handlers[0] == exception_handler


def test_context_get_clazz_instance():
    # GIVEN
    context: Context = Context()

    class FakeClass:
        pass

    # WHEN
    fake_class: FakeClass = context.get_clazz_instance(FakeClass)

    # THEN
    assert len(context.instances) == 1
    assert isinstance(fake_class, FakeClass)


def test_context_get_route_ctx():
    # GIVEN
    context: Context = Context()

    class FakeRouteCtx:
        def __init__(self) -> None:
            pass

        def match_request(self, req: http.server.BaseHTTPRequestHandler) -> bool:
            return True

    fake_route_ctx: FakeRouteCtx = FakeRouteCtx()

    context.route_contexts[HttpMethod.GET].append(fake_route_ctx)

    req: http.server.BaseHTTPRequestHandler = Mock(spec=http.server.BaseHTTPRequestHandler)
    # WHEN
    route_ctx: FakeRouteCtx = context.get_route_ctx(HttpMethod.GET, req)

    # THEN
    assert len(context.route_contexts[HttpMethod.GET]) == 1
    assert route_ctx == fake_route_ctx


def test_context_get_route_ctx_not_found():
    # GIVEN
    context: Context = Context()

    req: http.server.BaseHTTPRequestHandler = Mock(spec=http.server.BaseHTTPRequestHandler)
    req.path = "some_path"

    # WHEN & Then
    with pytest.raises(Exception, match=f"No route matching: {req.path}"):
        context.get_route_ctx(HttpMethod.GET, req)


def test_context_handle_exception():
    # GIVEN
    context: Context = Context()

    class FakeException(Exception):
        pass

    class FakeExceptionHandler:
        def __init__(self):
            self._type = Exception,

        def handle_exception(self, exception):
            return "response"

    context.exception_handlers.append(FakeExceptionHandler())

    # WHEN
    response: object = context.handle_exception(FakeException())

    # THEN
    assert response == "response"
