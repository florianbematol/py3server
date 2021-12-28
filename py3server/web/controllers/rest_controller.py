from __future__ import annotations

import logging

from py3server.app.repository import Repository
from py3server.app.service import Service
from py3server.constants import Decorator
from py3server.web.route_context import RouteContext


class RestController(object):
    """"""

    logger: logging.Logger = logging.getLogger(__name__)

    def __init__(self, path: str = '/') -> None:
        """"""
        from py3server.context import Context
        self.context: Context = Context()
        self.clazz: object = None
        self.path: str = path

        self.context.add_decorator(Decorator.CONTROLLER, self)

    def __call__(self, clazz: object) -> RestController:
        self.logger.debug(f'add rest_controller f{clazz.__name__}')
        self.clazz = self.context.get_clazz_instance(clazz)

        # Discover class annotations and inject matching app object
        for name, _type in getattr(self.clazz, '__annotations__', dict()).items():
            # TODO: Replace object with Service
            if isinstance(_type, Service):
                service = self.context.get_clazz_instance(_type.clazz.__class__)
                self.logger.debug(f'inject service {service.__class__.__name__} => {clazz.__name__}')
                setattr(self.clazz, name, service)
            # TODO: Replace object with Repository
            elif isinstance(_type, Repository):
                repository = self.context.get_clazz_instance(_type.clazz.__class__)
                self.logger.debug(f'inject repository {repository.__class__.__name__} => {clazz.__name__}')
                setattr(self.clazz, name, repository)

        # Update decorated class routes
        for _name, method in clazz.__dict__.items():
            if method.__class__.__name__ == 'RouteContext':
                mapping: RouteContext = method
                mapping.parent = self.clazz
                mapping.path = mapping.get_path_regex(self.path)

        return self
