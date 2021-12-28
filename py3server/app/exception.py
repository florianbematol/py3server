import typing as t

T = t.TypeVar('T')


class ExceptionHandler(object):
    def __init__(self, types=None) -> None:
        """
        Handle exceptions matching `_type`.

        :param _type: List of Exception catch by this object. ( Default: [Exception] )
        """
        from py3server.context import Context
        if types is None:
            types = [Exception]
        self.context: Context = Context()
        self.types: t.List[type] = types
        self.clazz: t.Optional[T] = None

        self.context.add_exception_handler(self)

    def __call__(self, clazz: T) -> t.Type[T]:
        """
        Store the decorated clazz in ExceptionHandler.clazz.

        :param clazz: Class decorated.
        :return: Class decorated.
        """
        self.clazz = clazz()
        return self.clazz

    def accept(self, exception: T) -> bool:
        """"""
        return type(exception) in self.types

    def handle_exception(self, exception: Exception) -> None:
        """
        Call decorated class `handle_exception` method,
        and pass exception as first parameter.

        :param exception: Exception handled by this ExceptionHandler.
        """
        print(self.clazz, exception)
        self.clazz.handle_exception(exception)
