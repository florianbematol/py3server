from pytest_mock import MockerFixture

from py3server.constants import MediaType, HttpMethod
from py3server.context import Context
from py3server.web.mapping.get_mapping import GetMapping
from py3server.web.route_context import RouteContext


def test_get_mapping_init():
    # GIVEN
    context: Context = Context()

    # WHEN
    get_mapping: GetMapping = GetMapping()

    # THEN
    assert get_mapping.context == context
    assert get_mapping.path == '/'
    assert get_mapping.produces == MediaType.APPLICATION_JSON


def test_get_mapping_init_with_custom_path_and_produces():
    # GIVEN
    context: Context = Context()
    path: str = '/a/custom/path'
    produces: MediaType = MediaType.TEXT_PLAIN

    # WHEN
    get_mapping: GetMapping = GetMapping(path, produces)

    # THEN
    assert get_mapping.context == context
    assert get_mapping.path == path
    assert get_mapping.produces == produces


def test_get_mapping_update_route_ctx(mocker: MockerFixture):
    # GIVEN
    path: str = '/some/path'

    get_mapping: GetMapping = GetMapping(path)
    route_ctx: RouteContext = mocker.Mock(RouteContext)

    # WHEN
    get_mapping.update_route_ctx(route_ctx)

    # THEN
    assert route_ctx.method == HttpMethod.GET
    assert route_ctx.path == get_mapping.path
    assert route_ctx.content_type == get_mapping.produces
