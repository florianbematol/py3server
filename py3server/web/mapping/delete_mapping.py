from py3server.constants import HttpMethod, MediaType
from py3server.web.mapping.mapping import Mapping
from py3server.web.route_context import RouteContext


class DeleteMapping(Mapping):
    def __init__(self, path: str = '/') -> None:
        super(DeleteMapping, self).__init__()
        self.path: str = path
        self.produces: MediaType = MediaType.NONE

    def update_route_ctx(self, route_ctx: RouteContext) -> None:
        route_ctx.method = HttpMethod.DELETE
        route_ctx.path = self.path
        route_ctx.content_type = self.produces
