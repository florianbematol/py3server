from py3server.web.response import Response


def test_response_init():
    # GIVEN
    status: int = 200
    content: object = {
        "firstname": "Florian",
        "lastname": "Bématol"
    }

    # WHEN
    response: Response = Response(status, content)

    # THEN
    assert response.status == status
    assert response.content == content
