from py3server.web.params.int_query_param import IntQP


def test_int_qp_init():
    # GIVEN & WHEN
    int_query_param: IntQP = IntQP('query_param_name')

    # THEN
    assert int_query_param.name == 'query_param_name'
    assert int_query_param._type == int
