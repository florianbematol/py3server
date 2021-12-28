from py3server.web.params.path_param import PathParam


class IntPP(PathParam):
    """ Integer path parameter. """

    def __init__(self, name: str):
        """"""
        super(IntPP, self).__init__(name, int)
