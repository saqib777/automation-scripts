# ReqRes Public API Test Suite
# Full CRUD coverage + auth + pagination
# https://reqres.in

import pytest
import requests


BASE_URL = "https://reqres.in/api"


@pytest.fixture(scope="session")
def session():
    s = requests.Session()
    s.headers.update({"Content-Type": "application/json"})
    return s


class TestUsers:

    def test_get_users_list(self, session):
        r = session.get(f"{BASE_URL}/users", params={"page": 1})
        assert r.status_code == 200
        data = r.json()
        assert "data" in data
        assert data["page"] == 1
        assert len(data["data"]) > 0

    def test_get_single_user(self, session):
        r = session.get(f"{BASE_URL}/users/2")
        assert r.status_code == 200
        user = r.json()["data"]
        assert user["id"] == 2
        assert "email"      in user
        assert "first_name" in user
        assert "last_name"  in user

    def test_user_not_found(self, session):
        r = session.get(f"{BASE_URL}/users/999")
        assert r.status_code == 404

    def test_create_user(self, session):
        payload = {"name": "Mohammed Saqib", "job": "QA Engineer"}
        r = session.post(f"{BASE_URL}/users", json=payload)
        assert r.status_code == 201
        data = r.json()
        assert data["name"] == "Mohammed Saqib"
        assert data["job"]  == "QA Engineer"
        assert "id" in data
        assert "createdAt" in data

    def test_update_user_put(self, session):
        payload = {"name": "Saqib Updated", "job": "SDET"}
        r = session.put(f"{BASE_URL}/users/2", json=payload)
        assert r.status_code == 200
        data = r.json()
        assert data["name"] == "Saqib Updated"
        assert data["job"]  == "SDET"
        assert "updatedAt" in data

    def test_update_user_patch(self, session):
        payload = {"job": "Senior QA"}
        r = session.patch(f"{BASE_URL}/users/2", json=payload)
        assert r.status_code == 200
        assert r.json()["job"] == "Senior QA"

    def test_delete_user(self, session):
        r = session.delete(f"{BASE_URL}/users/2")
        assert r.status_code == 204
        assert r.text == ""

    def test_pagination(self, session):
        r1 = session.get(f"{BASE_URL}/users", params={"page": 1})
        r2 = session.get(f"{BASE_URL}/users", params={"page": 2})
        assert r1.status_code == 200
        assert r2.status_code == 200
        ids_p1 = [u["id"] for u in r1.json()["data"]]
        ids_p2 = [u["id"] for u in r2.json()["data"]]
        assert not set(ids_p1) & set(ids_p2)


class TestAuth:

    def test_register_successful(self, session):
        payload = {"email": "eve.holt@reqres.in", "password": "pistol"}
        r = session.post(f"{BASE_URL}/register", json=payload)
        assert r.status_code == 200
        assert "token" in r.json()
        assert "id"    in r.json()

    def test_register_missing_password(self, session):
        payload = {"email": "sydney@fife"}
        r = session.post(f"{BASE_URL}/register", json=payload)
        assert r.status_code == 400
        assert "error" in r.json()

    def test_login_successful(self, session):
        payload = {"email": "eve.holt@reqres.in", "password": "cityslicka"}
        r = session.post(f"{BASE_URL}/login", json=payload)
        assert r.status_code == 200
        assert "token" in r.json()

    def test_login_missing_password(self, session):
        payload = {"email": "peter@klaven"}
        r = session.post(f"{BASE_URL}/login", json=payload)
        assert r.status_code == 400
        assert r.json()["error"] == "Missing password"

    def test_response_time(self, session):
        r = session.get(f"{BASE_URL}/users/1")
        assert r.elapsed.total_seconds() < 3.0

    def test_content_type_header(self, session):
        r = session.get(f"{BASE_URL}/users/1")
        assert "application/json" in r.headers.get("Content-Type", "")
