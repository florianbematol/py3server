import glob
import http.server
import importlib
import logging
import os
import sys
import typing as t

from py3server.http_handler import HttpHandler

LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO').upper()
logging.basicConfig(level=LOG_LEVEL)


class Booter:
    """"""

    logger: logging.Logger = logging.getLogger(__name__)

    def __init__(self, root_file: str) -> None:
        """"""
        self.running: bool = False
        self.root_file: str = root_file
        self.address: str = '0.0.0.0'
        self.port: int = 8080

    # TODO: Tests ?
    def run(self) -> None:  # pragma: no cover
        """
        Import all python files under `root_file`, and
        start the server listing on `address`:`port`.
        :return:
        """
        self.discover()

        self.logger.info(f'running server on http://{self.address}:{self.port}')
        server_address: t.Tuple[str, int] = (self.address, self.port)
        server: http.server.ThreadingHTTPServer = http.server.ThreadingHTTPServer(server_address, HttpHandler)

        try:
            self.running = True
            server.serve_forever()
        except KeyboardInterrupt:
            self.logger.info('Server closed')
            sys.exit(0)
        except Exception as e:
            self.logger.error(f'Unknown exception\t{str(e)}')
            sys.exit(1)

    def discover(self) -> None:
        """"""
        root_dir, root_filename = os.path.split(self.root_file)
        root_name: str = os.path.split(root_dir)[1]
        sys.path.append(os.path.dirname(root_dir))
        self.logger.debug(f'app root: \'{root_dir}\'')

        loop_path = f'{root_dir}/**/*.py'
        self.logger.debug(f'loop through python files in: \'{loop_path}\'')
        files: t.List[str] = [
            file for file in
            glob.glob(loop_path, recursive=True)
            if os.path.isfile(file) or file != self.root_file
        ]
        self.logger.debug(f'found {len(files)} files')

        self.logger.debug('import python modules')
        for file in files:
            module_path: str = file[file.index(root_name):-3].replace(os.sep, '.')
            self.logger.debug(f'module: {module_path}')
            importlib.import_module(module_path)
