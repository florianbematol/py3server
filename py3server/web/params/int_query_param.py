from py3server.web.params.query_param import QueryParam


class IntQP(QueryParam):
    """ Integer query parameter. """

    def __init__(self, name: str, default: int = None):
        super(IntQP, self).__init__(name, int, default)
