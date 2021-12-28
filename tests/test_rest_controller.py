from pytest_mock import MockerFixture

from py3server.app.repository import Repository
from py3server.app.service import Service
from py3server.constants import Decorator
from py3server.context import Context
from py3server.web.controllers.rest_controller import RestController


def test_rest_controller_init():
    # GIVEN
    context: Context = Context()

    # WHEN
    rest_controller: RestController = RestController()

    # THEN
    assert rest_controller.context == context
    assert rest_controller.path == '/'
    assert context.decorators[Decorator.CONTROLLER][0] == rest_controller


def test_rest_controller_call(mocker: MockerFixture):
    # GIVEN
    context: Context = Context()
    rest_controller: RestController = RestController()
    service: Service = Service()
    repository: Repository = Repository()

    class FakeRepository:
        pass

    class FakeService:
        pass

    class RouteContext:
        instance = None

        def __call__(self, *args, **kwargs):
            RouteContext.instance = self
            return self

        def get_path_regex(self, root_path: str):
            return f'{root_path} some_path'

    fake_route_ctx_spy: mocker.MagicMock = mocker.spy(RouteContext, 'get_path_regex')

    class FakeRestController:
        var_a: str
        var_b: service(FakeService)
        var_c: repository(FakeRepository)

        @RouteContext()
        def route(self):
            pass

    # WHEN
    rest_controller(FakeRestController)

    # THEN
    assert isinstance(rest_controller.clazz, FakeRestController)
    assert context.instances[hash(FakeRestController)] == rest_controller.clazz

    assert isinstance(rest_controller.clazz.var_b, FakeService)
    assert context.instances[hash(FakeService)] == rest_controller.clazz.var_b

    assert isinstance(rest_controller.clazz.var_c, FakeRepository)
    assert context.instances[hash(FakeRepository)] == rest_controller.clazz.var_c

    assert RouteContext.instance.parent == rest_controller.clazz
    assert RouteContext.instance.path == f'{rest_controller.path} some_path'
    fake_route_ctx_spy.assert_called_once_with(RouteContext.instance, rest_controller.path)
