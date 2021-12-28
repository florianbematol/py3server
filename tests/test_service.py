from pytest_mock import MockerFixture

from py3server.app.repository import Repository
from py3server.app.service import Service
from py3server.constants import Decorator
from py3server.context import Context


def test_service_init():
    # GIVEN
    context: Context = Context()

    # WHEN
    service: Service = Service()

    # THEN
    assert service.context == context
    assert context.decorators[Decorator.SERVICE][0] == service


def test_service_call(mocker: MockerFixture):
    # GIVEN
    context: Context = Context()

    service: Service = Service()
    service_other: Service = Service()
    repository: Repository = Repository()

    class FakeRepository:
        pass

    class FakeOtherService:
        pass

    class FakeService:
        var_a: str
        var_b: repository(FakeRepository)
        var_c: service_other(FakeOtherService)

    # WHEN
    service(FakeService)

    # THEN
    assert isinstance(service.clazz, FakeService)
    assert context.instances[hash(FakeService)] == service.clazz
    assert isinstance(service.clazz.var_b, FakeRepository)
    assert context.instances[hash(FakeRepository)] == service.clazz.var_b
    assert isinstance(service.clazz.var_c, FakeOtherService)
    assert context.instances[hash(FakeOtherService)] == service.clazz.var_c
