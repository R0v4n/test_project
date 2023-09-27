import pytest


def test_if_test_works(constant):
    value = constant
    assert value == 5


# @pytest.mark.parametrize("route", ["/download/{1}", "/diagram/"])
# def test_get_response(client, route):
#     response = client.get(route)
#     assert response.status_code == 200


def test_route_for_test(client):
    response = client.get('/route_for_test')
    assert response.json() == {'result': True}
    assert response.status_code == 200
