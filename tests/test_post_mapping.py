from pytest_mock import MockerFixture

from py3server.constants import MediaType, HttpMethod
from py3server.context import Context
from py3server.web.mapping.post_mapping import PostMapping
from py3server.web.route_context import RouteContext


def test_post_mapping_init():
    # GIVEN
    context: Context = Context()

    # WHEN
    post_mapping: PostMapping = PostMapping()

    # THEN
    assert post_mapping.context == context
    assert post_mapping.path == '/'
    assert post_mapping.produces == MediaType.APPLICATION_JSON


def test_post_mapping_init_with_custom_path_and_produces():
    # GIVEN
    context: Context = Context()
    path: str = '/some/path'
    produces: MediaType = MediaType.TEXT_PLAIN

    # WHEN
    post_mapping: PostMapping = PostMapping(path, produces)

    # THEN
    assert post_mapping.context == context
    assert post_mapping.path == path
    assert post_mapping.produces == produces


def test_post_mapping_update_route_ctx(mocker: MockerFixture):
    # GIVEN
    path: str = '/some/path'

    post_mapping: PostMapping = PostMapping(path)
    route_ctx: RouteContext = mocker.Mock(RouteContext)

    # WHEN
    post_mapping.update_route_ctx(route_ctx)

    # THEN
    assert route_ctx.method == HttpMethod.POST
    assert route_ctx.path == post_mapping.path
    assert route_ctx.content_type == post_mapping.produces
