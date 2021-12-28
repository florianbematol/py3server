import pytest

from py3server.context import Context
from py3server.utils.singleton import SingletonMeta


@pytest.fixture(autouse=True)
def clean_up_context():
    """
    Before each tests delete all saved instances.
    :return:
    """
    Context._instance = None
