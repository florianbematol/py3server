class QueryParam(object):
    """
    ...
    Examples:
        @GetMapping('/users')
        def test(self, limit: QueryParam('limit', 10, int)):
            ...
    """

    def __init__(self, name: str, _type: type, default: any = None) -> None:
        self.name: str = name
        self.default = default
        self._type = _type

    def get_value(self, query_params: dict[str, str]):
        v = query_params.get(self.name, self.default)
        if v is not None:
            return self._type(v)
        return v
