from py3server.constants import HttpMethod, MediaType
from py3server.web.mapping.mapping import Mapping
from py3server.web.route_context import RouteContext


class GetMapping(Mapping):
    def __init__(self, path: str = '/', produces: MediaType = MediaType.APPLICATION_JSON) -> None:
        super(GetMapping, self).__init__()
        self.path: str = path
        self.produces: MediaType = produces

    def update_route_ctx(self, route_ctx: RouteContext) -> None:
        route_ctx.method = HttpMethod.GET
        route_ctx.path = self.path
        route_ctx.content_type = self.produces
