import http.server
import json
import re
import typing as t

from py3server.constants import HttpMethod, MediaType
from py3server.web.params.body import Body
from py3server.web.params.path_param import PathParam
from py3server.web.params.query_param import QueryParam
from py3server.web.response import Response


class RouteContext:
    """"""

    def __init__(self, func: t.Callable) -> None:
        """"""
        # GLOBAL
        self.parent: object = None
        self.func: t.Callable = func

        # METHOD MAPPING
        self.method: HttpMethod = HttpMethod.NONE
        self.path: re.Pattern[str] = re.compile("")

        # STATUS MAPPING
        # self.status: int = 200

        # REQUEST CONTEXT
        self.req: t.Optional[http.server.BaseHTTPRequestHandler] = None
        self.query_params: t.Dict[str, str] = {}
        self.path_params: t.Dict[str, str] = {}
        self.body: t.AnyStr = ''
        self.content_type: MediaType = MediaType.NONE

    def get_path_regex(self, parent_path: str) -> re.Pattern:
        """"""
        start_path = '/'.join([x for x in [parent_path, self.path.replace('/', '', 1)] if x])

        _path_params = re.findall('{.*?}', start_path)

        temp = []
        for path_param in _path_params:
            k = path_param[1:-1].split(':', 1)
            name = k[0]
            reg = k[1] if len(k) == 2 else '.*?'

            if name not in temp:
                temp.append(name)
                start_path = start_path.replace(path_param, f'(?P<{name}>{reg})')
            else:
                raise Exception(f'Duplicated path params \'{name}\'')

        end_path = r'(/|)'
        query_params = r'(\?(?P<qp>.*)|)'

        path_regex = ''.join(['^', start_path, end_path, query_params, '$'])

        return re.compile(path_regex)

    def match_request(self, req: http.server.BaseHTTPRequestHandler) -> bool:
        return self.path.match(req.path) is not None

    def get_response(self, req: http.server.BaseHTTPRequestHandler) -> Response:
        self.update_context(req)

        params = {}
        for key, item in getattr(self.func, '__annotations__', {}).items():
            if isinstance(item, QueryParam):
                params[key] = item.get_value(self.query_params)
            elif isinstance(item, PathParam):
                params[key] = item.get_value(self.path_params)
            elif isinstance(item, Body) or item == Body:
                params[key] = self.body
            else:
                raise Exception(f'Unknown item type: {type(item).__name__} with key: {key}')

        response: Response = self.func(self.parent, **params)

        # data = bytes(json.dumps(content, separators=(',', ':'), ensure_ascii=False),
        #              'utf-8') if content is not None else None
        return response

    def update_context(self, req: http.server.BaseHTTPRequestHandler) -> None:
        """"""
        self.req = req
        self.query_params = {}
        self.path_params = {}

        # Query params
        groups = self.path.match(req.path).groupdict()
        if groups['qp']:
            for x in groups['qp'].split('&'):
                if x:
                    key, value = x.split('=')
                    self.query_params[key] = value
        del groups['qp']

        # Path params
        if groups:
            self.path_params = groups

        # Body
        body_length: int = int(req.headers.get('Content-Length', 0))
        if body_length > 0:
            self.body = req.rfile.read(body_length)

        if self.body:
            content_type = req.headers.get('Content-type')
            if content_type == 'application/json':
                self.body = json.loads(self.body)
            else:
                raise NotImplementedError(f'Content-type missing {content_type}')

    def get_content_type(self) -> str:
        """"""
        return self.content_type.value

    def get_content(self, content: any) -> bytes:
        """"""
        output: str
        if self.content_type == MediaType.APPLICATION_JSON:
            output = json.dumps(content, ensure_ascii=True)
        else:
            raise Exception(f'No manage content-type: {self.content_type}')

        return bytes(output, 'utf-8')
