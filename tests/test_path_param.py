import typing as t

import pytest

from py3server.web.params.path_param import PathParam


def test_path_param_init():
    # GIVEN & WHEN
    path_param: PathParam = PathParam('path_param_name', str)

    # THEN
    assert path_param.name == 'path_param_name'
    assert path_param._type == str


def test_path_param_get_value():
    # GIVEN
    path_param: PathParam = PathParam('path_param_name', str)
    path_params: t.Dict[str, str] = {
        'path_param_name': 'hello'
    }

    # WHEN
    value: str = path_param.get_value(path_params)

    # THEN
    assert value == 'hello'


def test_path_param_get_value_with_missing_key():
    # GIVEN
    path_param: PathParam = PathParam('path_param_name', str)
    path_params: t.Dict[str, str] = {
        'other_path_param_name': 'hello'
    }

    # WHEN & THEN
    with pytest.raises(Exception, match='Missing path parameter: path_param_name'):
        path_param.get_value(path_params)
