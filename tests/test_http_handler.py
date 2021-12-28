from unittest.mock import Mock

from py3server.http_handler import HttpHandler


def test_http_handler_favicon_return_true():
    # GIVEN
    req: HttpHandler = Mock(HttpHandler)
    req.path = "/some/path/favicon.ico"

    # WHEN
    is_favicon: bool = HttpHandler.favicon(req)

    # THEN
    assert is_favicon


def test_http_handler_favicon_return_false():
    # GIVEN
    req: HttpHandler = Mock(HttpHandler)
    req.path = "/some/path/resource.xml"

    # WHEN
    is_favicon: bool = HttpHandler.favicon(req)

    # THEN
    assert is_favicon == False
