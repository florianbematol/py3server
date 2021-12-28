from py3server.web.params.query_param import QueryParam


def test_query_param_init():
    # GIVEN & WHEN
    query_param: QueryParam = QueryParam('query_param_name', str, 'a default value')

    # THEN
    assert query_param.name == 'query_param_name'
    assert query_param._type == str
    assert query_param.default == 'a default value'


def test_query_param_get_value():
    # GIVEN
    query_params = {
        "key": "value"
    }
    query_param: QueryParam = QueryParam('key', str)

    # WHEN
    value: str = query_param.get_value(query_params)

    # THEN
    assert value == 'value'


def test_query_param_get_value_default_value():
    # GIVEN
    query_params = {
        "other_key": "value"
    }
    query_param: QueryParam = QueryParam('key', str, 'default value')

    # WHEN
    value: str = query_param.get_value(query_params)

    # THEN
    assert value == 'default value'


def test_query_param_get_value_not_found():
    # GIVEN
    query_params = {
        "key": "value"
    }
    query_param: QueryParam = QueryParam('other_key', str)

    # WHEN
    value: str = query_param.get_value(query_params)

    # THEN
    assert value is None
