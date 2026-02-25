import pytest
from django.test import Client


@pytest.mark.django_db
def test_home_page_returns_200():
    client = Client()
    response = client.get("/")
    assert response.status_code == 200


@pytest.mark.django_db
def test_health_check_returns_200():
    client = Client()
    response = client.get("/health/")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


@pytest.mark.django_db
def test_admin_redirects_to_login():
    client = Client()
    response = client.get("/admin/")
    assert response.status_code == 302
    assert "/admin/login/" in response.url
