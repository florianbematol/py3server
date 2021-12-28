from pytest_mock import MockerFixture

from py3server.constants import HttpMethod
from py3server.context import Context
from py3server.web.mapping.mapping import Mapping
from py3server.web.route_context import RouteContext


def test_mapping_init():
    # GIVEN
    context: Context = Context()

    # WHEN
    mapping: Mapping = Mapping()

    # THEN
    assert mapping.context == context


def test_mapping_call_without_route_context(mocker: MockerFixture):
    # GIVEN
    def fake_route():
        pass

    mapping: Mapping = Mapping()
    update_route_ctx_spy: mocker.Mock = mocker.patch.object(mapping, 'update_route_ctx')
    add_route_ctx_spy: mocker.Mock = mocker.patch.object(Context, 'add_route_ctx')

    # WHEN
    route_ctx: RouteContext = mapping(fake_route)

    # THEN
    update_route_ctx_spy.assert_called_once()
    add_route_ctx_spy.assert_not_called()
    assert route_ctx is not None


def test_mapping_call_with_route_context(mocker: MockerFixture):
    # GIVEN
    context: Context = Context()
    route_ctx: RouteContext = mocker.Mock(RouteContext)
    route_ctx.method = HttpMethod.GET
    mapping: Mapping = Mapping()
    update_route_ctx_spy: mocker.Mock = mocker.patch.object(mapping, 'update_route_ctx')
    add_route_ctx_spy: mocker.Mock = mocker.patch.object(Context, 'add_route_ctx')

    # WHEN
    route_ctx: RouteContext = mapping(route_ctx)

    # THEN
    update_route_ctx_spy.assert_called_once_with(route_ctx)
    add_route_ctx_spy.assert_called_once_with(route_ctx)
    assert route_ctx is not None
