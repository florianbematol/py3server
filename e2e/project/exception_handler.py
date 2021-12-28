from py3server.app.exception import ExceptionHandler
from py3server.web.response import Response


@ExceptionHandler()
class GlobalExceptionHandler(object):

    def handle_exception(self, exception: Exception):
        content: bytes = bytes('{"error": "ServerError", "message": "Server error. Contact administrator"}', "utf-8")
        return Response(500, 'application/json', content)
