import os
import sys
import threading
import time

import pytest

from py3server.booter import Booter


@pytest.fixture(scope='session', autouse=True)
def run_server():
    server_path: str = os.path.join(os.path.dirname(__file__), 'project', 'main.py')
    server_dir, _ = os.path.split(server_path)

    sys.path.append(server_dir)

    booter: Booter = Booter(server_path)

    thread: threading.Thread = threading.Thread(target=lambda: booter.run())
    thread.daemon = True
    thread.start()

    while not booter.running:
        time.sleep(2)
