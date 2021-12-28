import typing as t


class Response(object):
    """"""

    def __init__(self, status: int, content: t.Union[object] = None) -> None:
        """"""
        self.status: int = status
        self.content: any = content
