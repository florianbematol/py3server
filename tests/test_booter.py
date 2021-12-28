import importlib
import os
import tempfile
import typing as t
from unittest.mock import call

from pytest_mock import MockerFixture

from py3server.booter import Booter


def test_booter_init():
    # GIVEN
    root_file: str = "my/root/folder/file.py"

    # WHEN
    booter: Booter = Booter(root_file)

    # THEN
    assert booter.root_file == root_file
    assert booter.address == '0.0.0.0'
    assert booter.port == 8080


def test_booter_discover(mocker: MockerFixture) -> None:
    # GIVEN
    mocker.patch('importlib.import_module')

    temp_dir: tempfile.TemporaryDirectory = tempfile.TemporaryDirectory()
    _, temp_dir_name = os.path.split(temp_dir.name)
    main_file: str = 'main.py'

    valid_files: t.List[str] = ['file1.py', 'file2.py', 'file3.py']
    invalid_files: t.List[str] = ['invalid_file2.py.txt', 'invalid_file3']

    os.mkdir(os.path.join(temp_dir.name, 'not_a_file'))

    for file in [main_file] + valid_files + invalid_files:
        path: str = os.path.join(temp_dir.name, file)
        with open(path, "w+") as fp:
            pass

    booter: Booter = Booter(os.path.join(temp_dir.name, main_file))

    # WHEN
    booter.discover()

    # THEN
    importlib.import_module.assert_has_calls([
        call(f'{temp_dir_name}.{file.replace(".py", "")}') for file in valid_files
    ], any_order=True)

