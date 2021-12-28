import http.server

from py3server.constants import HttpMethod
from py3server.context import Context
from py3server.web.response import Response
from py3server.web.route_context import RouteContext


class HttpHandler(http.server.BaseHTTPRequestHandler):

    # TODO: Test this method
    @staticmethod
    def dispatch(req: http.server.BaseHTTPRequestHandler, method: HttpMethod) -> None:  # pragma: no cover
        """"""
        if HttpHandler.favicon(req):
            return

        context: Context = Context()
        route_ctx: RouteContext = context.get_route_ctx(method, req)

        try:
            response: Response = route_ctx.get_response(req)
        except Exception as e:
            response: Response = context.handle_exception(e)

        if not isinstance(response, Response):
            raise Exception(f'Invalid response object type {response.__class__}. Expected {Response} type.')

        req.send_response(response.status)
        req.send_header('Content-type', route_ctx.get_content_type())
        req.end_headers()
        req.wfile.write(route_ctx.get_content(response.content))

    @staticmethod
    def favicon(req: http.server.BaseHTTPRequestHandler) -> bool:
        """ Return true if the current request is a favicon.ico """
        if 'favicon.ico' in req.path:
            # We skip any favicon.icon request
            req.send_response(404)
            req.end_headers()
            return True
        return False

    def do_GET(self) -> None:  # pragma: no cover
        """ Handle GET request """
        HttpHandler.dispatch(self, HttpMethod.GET)

    def do_POST(self) -> None:  # pragma: no cover
        """ Handle POST request """
        HttpHandler.dispatch(self, HttpMethod.POST)

    def do_PUT(self) -> None:  # pragma: no cover
        """ Handle POST request """
        HttpHandler.dispatch(self, HttpMethod.PUT)

    def do_DELETE(self) -> None:  # pragma: no cover
        """ Handle POST request """
        HttpHandler.dispatch(self, HttpMethod.DELETE)
