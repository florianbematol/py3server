import http.server
import json
import re

import pytest
from pytest_mock import MockerFixture

from py3server.constants import HttpMethod, MediaType
from py3server.web.params.body import Body
from py3server.web.params.path_param import PathParam
from py3server.web.params.query_param import QueryParam
from py3server.web.response import Response
from py3server.web.route_context import RouteContext


def test_route_context_init():
    # GIVEN & WHEN
    def fake_route_func():
        return

    route_context: RouteContext = RouteContext(fake_route_func)

    # THEN
    assert route_context.func == fake_route_func
    assert route_context.method == HttpMethod.NONE
    assert route_context.path == re.compile("")
    # assert route_context.status is None
    assert route_context.req is None
    assert route_context.query_params == {}
    assert route_context.path_params == {}
    assert route_context.body == ''
    assert route_context.content_type == MediaType.NONE


def test_route_context_get_path_regex():
    # GIVEN
    def fake_route_func():
        return

    route_context: RouteContext = RouteContext(fake_route_func)
    route_context.path = r'/child/{id:\w+}/info/{action}'
    parent_path: str = r'/parent/{folder}'

    # WHEN
    path: re.Pattern = route_context.get_path_regex(parent_path)

    # THEN
    assert path == re.compile(r'^/parent/(?P<folder>.*?)/child/(?P<id>\w+)/info/(?P<action>.*?)(/|)(\?(?P<qp>.*)|)$')


def test_route_context_get_path_regex_with_duplicated_path_params():
    # GIVEN
    route_context: RouteContext = RouteContext(lambda *x, **y: None)
    route_context.path = r'/child/{id:\w+}/info'
    parent_path: str = r'/parent/{id}'

    # WHEN & THEN
    with pytest.raises(Exception, match='Duplicated path params \'id\''):
        route_context.get_path_regex(parent_path)


def test_route_context_match_request(mocker: MockerFixture):
    # GIVEN
    req_path: str = '/some/path'

    route_context: RouteContext = RouteContext(lambda *x, **y: None)
    route_context.path = re.compile(req_path)

    req: http.server.BaseHTTPRequestHandler = mocker.Mock(http.server.BaseHTTPRequestHandler)
    req.path = req_path

    # WHEN
    match_request: bool = route_context.match_request(req)

    # THEN
    assert match_request


def test_route_context_match_request_not_matching(mocker: MockerFixture):
    # GIVEN
    route_ctx_path: str = '/some/path'
    req_path: str = '/some/other/path'

    route_context: RouteContext = RouteContext(lambda *x, **y: None)
    route_context.path = re.compile(route_ctx_path)

    req: http.server.BaseHTTPRequestHandler = mocker.Mock(http.server.BaseHTTPRequestHandler)
    req.path = req_path

    # WHEN
    match_request: bool = route_context.match_request(req)

    # THEN
    assert not match_request


def test_route_context_get_response_call_update_context(mocker: MockerFixture):
    # GIVEN
    def fake_func():
        return

    route_context: RouteContext = RouteContext(fake_func)
    req: http.server.BaseHTTPRequestHandler = mocker.Mock(http.server.BaseHTTPRequestHandler)

    update_context_patch: mocker.MagicMock = mocker.patch.object(route_context, 'update_context')
    mocker.patch.object(route_context, 'func')

    # WHEN
    route_context.get_response(req)

    # THEN
    update_context_patch.assert_called_once()


def test_route_context_get_response_func_call_with_query_params(mocker: MockerFixture):
    # GIVEN
    def fake_func():
        return

    query_params = {
        'a': 'test',
        'b': 55,
        'c': 'something_larger'
    }

    route_context: RouteContext = RouteContext(fake_func)
    route_context.query_params = query_params

    mocker.patch.object(route_context, 'update_context')
    func_spy: mocker.MagicMock = mocker.patch.object(route_context, 'func')

    route_context.func.__annotations__ = {
        'a': QueryParam('a', str),
        'b': QueryParam('b', int),
        'c': QueryParam('c', str)
    }

    req: http.server.BaseHTTPRequestHandler = mocker.Mock(http.server.BaseHTTPRequestHandler)

    # WHEN
    route_context.get_response(req)

    # THEN
    func_spy.assert_called_once_with(route_context.parent, **query_params)


def test_route_context_get_response_func_call_with_path_params(mocker: MockerFixture):
    # GIVEN
    def fake_func():
        return

    path_params = {
        'a': 2,
        'b': 'delete',
    }

    route_context: RouteContext = RouteContext(fake_func)
    route_context.path_params = path_params

    mocker.patch.object(route_context, 'update_context')
    func_spy: mocker.MagicMock = mocker.patch.object(route_context, 'func')

    route_context.func.__annotations__ = {
        'a': PathParam('a', int),
        'b': PathParam('b', str),
    }

    req: http.server.BaseHTTPRequestHandler = mocker.Mock(http.server.BaseHTTPRequestHandler)

    # WHEN
    route_context.get_response(req)

    # THEN
    func_spy.assert_called_once_with(route_context.parent, **path_params)


def test_route_context_get_response_func_call_with_body(mocker: MockerFixture):
    # GIVEN
    def fake_func():
        return

    body = {
        'firstname': 'Florian',
        'lastname': 'Bématol'
    }

    route_context: RouteContext = RouteContext(fake_func)
    route_context.body = body

    mocker.patch.object(route_context, 'update_context')
    func_spy: mocker.MagicMock = mocker.patch.object(route_context, 'func')

    route_context.func.__annotations__ = {
        'body': Body(),
    }

    req: http.server.BaseHTTPRequestHandler = mocker.Mock(http.server.BaseHTTPRequestHandler)

    # WHEN
    route_context.get_response(req)

    # THEN
    func_spy.assert_called_once_with(route_context.parent, body=body)


def test_route_context_get_response_return_func_response(mocker: MockerFixture):
    # GIVEN
    response: Response = Response(202, {
        'id': 1,
        'user': 'Someone Then'
    })

    route_context: RouteContext = RouteContext(lambda *x, **y: response)

    mocker.patch.object(route_context, 'update_context')

    req: http.server.BaseHTTPRequestHandler = mocker.Mock(http.server.BaseHTTPRequestHandler)

    # WHEN
    ret_response: Response = route_context.get_response(req)

    # THEN
    assert ret_response.status == response.status
    assert ret_response.content == response.content


def test_route_context_get_response_with_unknown_annotations_type(mocker: MockerFixture):
    # GIVEN
    route_context: RouteContext = RouteContext(lambda *x, **y: None)

    mocker.patch.object(route_context, 'update_context')

    route_context.func.__annotations__ = {
        "unknown": str()
    }

    req: http.server.BaseHTTPRequestHandler = mocker.Mock(http.server.BaseHTTPRequestHandler)

    # WHEN & THEN
    with pytest.raises(Exception, match='Unknown item type: str with key: unknown'):
        route_context.get_response(req)


def test_route_context_update_context_set_req(mocker: MockerFixture):
    # GIVEN
    route_context: RouteContext = RouteContext(lambda *x, **y: None)
    route_context.path = '/users'
    route_context.path = route_context.get_path_regex('/api/v1')

    req: http.server.BaseHTTPRequestHandler = mocker.Mock(http.server.BaseHTTPRequestHandler)
    req.path = '/api/v1/users'
    req.headers = {}

    # WHEN
    route_context.update_context(req)

    # THEN
    assert route_context.req == req


def test_route_context_update_context_set_query_params(mocker: MockerFixture):
    # GIVEN
    route_context: RouteContext = RouteContext(lambda *x, **y: None)
    route_context.path = '/users'
    route_context.path = route_context.get_path_regex('/api/v1')

    req: http.server.BaseHTTPRequestHandler = mocker.Mock(http.server.BaseHTTPRequestHandler)
    req.path = "/api/v1/users?view=full&enable=true"
    req.headers = {}

    # WHEN
    route_context.update_context(req)

    # THEN
    assert route_context.query_params == {
        "view": "full",
        "enable": "true"
    }
    # assert route_context.body == {'data': 'name', 'version': 1}


def test_route_context_update_context_set_path_params(mocker: MockerFixture):
    # GIVEN
    route_context: RouteContext = RouteContext(lambda *x, **y: None)
    route_context.path = '/users/{id}/action/{action}'
    route_context.path = route_context.get_path_regex('/api/v1')

    req: http.server.BaseHTTPRequestHandler = mocker.Mock(http.server.BaseHTTPRequestHandler)
    req.path = "/api/v1/users/10/action/delete"
    req.headers = {}

    # WHEN
    route_context.get_response(req)

    # THEN
    assert route_context.path_params == {
        "id": "10",
        "action": "delete"
    }


def test_route_context_update_context_set_body(mocker: MockerFixture):
    # GIVEN
    req_body: str = json.dumps({
        'firstname': 'Someone',
        'lastname': 'Else'
    })

    route_context: RouteContext = RouteContext(lambda *x, **y: None)
    route_context.path = '/users'
    route_context.path = route_context.get_path_regex('/api/v1')

    req: http.server.BaseHTTPRequestHandler = mocker.Mock(http.server.BaseHTTPRequestHandler)
    req.path = "/api/v1/users"
    req.headers = {
        'Content-Length': len(req_body),
        'Content-type': 'application/json'
    }
    req.rfile = type('object', (object,), {
        'read': lambda x: req_body
    })

    # WHEN
    route_context.update_context(req)

    # THEN
    assert route_context.body == json.loads(req_body)


def test_route_context_update_context_with_invalid_content_type(mocker: MockerFixture):
    # GIVEN
    req_body: str = json.dumps({
        'firstname': 'Someone',
        'lastname': 'Else'
    })

    route_context: RouteContext = RouteContext(lambda *x, **y: None)
    route_context.path = '/some/path'
    route_context.path = route_context.get_path_regex('/api/v1')

    req: http.server.BaseHTTPRequestHandler = mocker.Mock(http.server.BaseHTTPRequestHandler)
    req.path = '/api/v1/some/path'
    req.headers = {
        'Content-Length': len(req_body),
        'Content-type': 'unknown/content-type'
    }
    req.rfile = type('object', (object,), {
        'read': lambda x: req_body
    })

    # WHEN & THEN
    with pytest.raises(NotImplementedError, match=f'Content-type missing unknown/content-type'):
        route_context.update_context(req)


def test_route_context_get_content_type():
    # GIVEN
    route_context: RouteContext = RouteContext(lambda *x, **y: None)
    route_context.content_type = MediaType.APPLICATION_JSON

    # WHEN
    content_type: str = route_context.get_content_type()

    # THEN
    assert content_type == MediaType.APPLICATION_JSON.value


def test_route_context_get_content():
    # GIVEN
    data = {
        'firstname': 'user_firstname',
        'lastname': 'user_lastname'
    }
    route_context: RouteContext = RouteContext(lambda *x, **y: None)
    route_context.content_type = MediaType.APPLICATION_JSON

    # WHEN
    content: bytes = route_context.get_content(data)

    # THEN
    assert content == bytes(json.dumps(data, ensure_ascii=True), 'utf-8')


def test_route_context_get_content_with_invalid_content_type():
    # GIVEN
    route_context: RouteContext = RouteContext(lambda *x, **y: None)

    # WHEN & THEN
    with pytest.raises(Exception, match=f'No manage content-type: {MediaType.NONE}'):
        route_context.get_content(None)
