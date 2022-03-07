from pytest import mark
from faker import Faker, providers


def test_get_all_rate_response_is_404_because_no_data_from_database(client):
    response = client.get("/api/rate")
    assert response.status_code == 404


def test_get_one_rate_response_is_404_because_no_data_from_database(client):
    response = client.get("/api/rate")
    assert response.status_code == 404


def test_create_rate_response_is_201(client, fake_rate):
    response = client.post("/api/rate", json=fake_rate)
    assert response.status_code == 201


@mark.parametrize("parametro", [0, 6, 7, -1])
def test_create_rate_with_wrong_rate_data_response_is_400(client, fake_rate, parametro):
    fake_rate["rate"] = parametro
    response = client.post("/api/rate", json=fake_rate)
    assert response.status_code == 400


def test_create_rate_without_rate_data_response_is_400(client, fake_rate):
    fake_rate["rate"] = None
    response = client.post("/api/rate", json=fake_rate)
    assert response.status_code == 400


def test_create_rate_with_wrong_max_title_data_response_is_404(client, fake_rate):
    fake = Faker()
    fake_rate["title"] = fake.pystr(min_chars=256, max_chars=256)
    response = client.post("/api/rate", json=fake_rate)
    assert response.status_code == 400


def test_create_rate_without_content_data_response_is_400(client, fake_rate):
    fake = Faker()
    fake_rate["content"] = None
    response = client.post("/api/rate", json=fake_rate)
    assert response.status_code == 400


def test_create_rate_with_wrong_type_data_response_is_400(client, fake_rate):
    fake = Faker()
    fake_rate["type_rate"] = "MOVIE"
    response = client.post("/api/rate", json=fake_rate)
    assert response.status_code == 422


def test_create_rate_response_title_is_equal_title_inserted(client, fake_rate):
    response = client.post("/api/rate", json=fake_rate)
    assert response.json["title"] == fake_rate["title"]


def test_create_rate_response_content_is_equal_content_inserted(client, fake_rate):
    response = client.post("/api/rate", json=fake_rate)
    assert response.json["content"] == fake_rate["content"]


def test_create_rate_response_rate_type_is_equal_rate_type_inserted(client, fake_rate):
    response = client.post("/api/rate", json=fake_rate)
    assert response.json["rate_type"] == fake_rate["rate_type"]


def test_create_rate_response_rate_is_equal_rate_inserted(client, fake_rate):
    response = client.post("/api/rate", json=fake_rate)
    assert response.json["rate"] == fake_rate["rate"]


def test_create_rate_response_have_rate_date_posted(client, fake_rate):
    response = client.post("/api/rate", json=fake_rate)
    assert response.json["date_posted"]


def test_create_rate_response_have_rate_id(client, fake_rate):
    response = client.post("/api/rate", json=fake_rate)
    assert response.json["id"]


def test_get_all_rate_response_is_200(client):
    response = client.get("/api/rate")
    assert response.status_code == 200


def test_get_one_rate_response_is_200(client):
    response = client.get("/api/rate/1")
    assert response.status_code == 200


def test_get_one_invalid_rate_response_is_404(client):
    response = client.get("/api/rate/0")
    assert response.status_code == 404


def test_update_rate_response_is_200(client, fake_rate):
    response = client.put("/api/rate/1", json=fake_rate)
    assert response.status_code == 200


def test_update_rate_response_is_equal_to_json_inserted(client, fake_rate):
    client.put("/api/rate/2", json=fake_rate)
    response = client.get("/api/rate/2")
    assert response.json["content"] == fake_rate["content"]


def test_update_invalid_rate_response_is_404(client, fake_rate):
    response = client.put("/api/rate/555555", json=fake_rate)
    assert response.status_code == 404


def test_delete_rate_response_is_204(client):
    response = client.delete("/api/rate/1")
    assert response.status_code == 200


def test_delete_invalid_rate_response_is_404(client):
    response = client.delete("/api/rate/555555")
    assert response.status_code == 404


def test_delete_rate_number_of_rate_is_less(client):
    response = client.get("/api/rate")
    number_of_rate_berofe = len(response.json)
    client.delete("/api/rate/2")
    response = client.get("/api/rate")
    number_of_rate_after = len(response.json)
    assert (number_of_rate_after + 1) == number_of_rate_berofe
