class PathParam(object):
    """
    Indicate that a route function's parameter will receive request url matching path param.
    Examples:
        @GetMapping('/users/{id}')
        def test(self, user_id: PathParam('id', str)):
            ...
    """

    def __init__(self, name: str, _type: type) -> None:
        """"""
        self.name: str = name
        self._type = _type

    def get_value(self, path_params: dict[str, str]):
        if self.name in path_params.keys():
            v = path_params.get(self.name)
            if v:
                v = self._type(v)
            return v
        raise Exception(f'Missing path parameter: {self.name}')
