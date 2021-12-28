from py3server.web.params.int_path_param import IntPP


def test_int_pp_init():
    # GIVEN & WHEN
    int_path_param: IntPP = IntPP('path_param_name')

    # THEN
    assert int_path_param.name == 'path_param_name'
    assert int_path_param._type == int
