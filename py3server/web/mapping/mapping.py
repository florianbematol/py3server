from py3server.constants import HttpMethod
from py3server.context import Context
from py3server.web.route_context import RouteContext


class Mapping(object):
    """
    Base object for mapping object.
    """

    def __init__(self):
        """"""
        self.context = Context()

    def __call__(self, func: callable):
        """"""
        route_ctx: RouteContext = func if isinstance(func, RouteContext) else RouteContext(func)
        self.update_route_ctx(route_ctx)

        if route_ctx.method != HttpMethod.NONE:
            Context().add_route_ctx(route_ctx)

        return route_ctx

    def update_route_ctx(self, route_ctx: RouteContext) -> None:  # pragma: no cover
        """ Apply logic of child mapping object """
        raise NotImplementedError()
