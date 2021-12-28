from __future__ import annotations

import logging

from py3server.app.repository import Repository
from py3server.constants import Decorator


class Service(object):
    """"""

    logger: logging.Logger = logging.getLogger(__name__)

    def __init__(self) -> None:
        """"""
        from py3server.context import Context
        self.context: Context = Context()
        self.clazz: object = None

        self.context.add_decorator(Decorator.SERVICE, self)

    def __call__(self, clazz: object) -> Service:
        """"""
        self.logger.debug(f'add service {clazz.__name__}')
        self.clazz = self.context.get_clazz_instance(clazz)

        # Discover class annotations and inject matching app object
        for name, _type in getattr(self.clazz, '__annotations__', {}).items():
            if isinstance(_type, Service):
                service = self.context.get_clazz_instance(_type.clazz.__class__)
                self.logger.debug(f'inject service {service.__class__.__name__} => {clazz.__name__}.{name}')
                setattr(self.clazz, name, service)
            elif isinstance(_type, Repository):
                repository = self.context.get_clazz_instance(_type.clazz.__class__)
                self.logger.debug(f'inject repository {repository.__class__.__name__} => {clazz.__name__}.{name}')
                setattr(self.clazz, name, repository)

        return self
