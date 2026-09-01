"""Unit tests for the sample Flask application in app.py."""

import importlib
import json

import pytest

import app as app_module


@pytest.fixture
def client():
    """Flask test client with app config switched to testing mode."""
    app_module.app.config["TESTING"] = True
    with app_module.app.test_client() as test_client:
        yield test_client


def test_home_returns_html_page(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.content_type

    body = response.get_data(as_text=True)
    assert "Hello, This deployment is from GithubActions" in body
    assert "Served by gunicorn as a non-root user" in body


def test_home_shows_runtime_details(client):
    body = client.get("/").get_data(as_text=True)
    assert "Container host:" in body
    assert "Running as UID:" in body
    assert "Python:" in body


def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "healthy"}


def test_info_endpoint_returns_expected_keys(client):
    response = client.get("/api/info")
    assert response.status_code == 200

    payload = response.get_json()
    assert set(payload) == {"app", "hostname", "uid", "python"}
    assert payload["app"] == app_module.APP_NAME
    assert isinstance(payload["uid"], int)
    assert payload["python"].startswith("3.")


def test_info_endpoint_is_valid_json(client):
    response = client.get("/api/info")
    assert json.loads(response.get_data(as_text=True))["hostname"]


def test_unknown_route_returns_404(client):
    assert client.get("/does-not-exist").status_code == 404


def test_app_name_can_be_overridden(monkeypatch):
    """APP_NAME is read at import time, so reload after setting it."""
    monkeypatch.setenv("APP_NAME", "Custom App Name")
    reloaded = importlib.reload(app_module)
    try:
        assert reloaded.APP_NAME == "Custom App Name"
        with reloaded.app.test_client() as test_client:
            body = test_client.get("/").get_data(as_text=True)
            assert "Custom App Name" in body
    finally:
        monkeypatch.delenv("APP_NAME", raising=False)
        importlib.reload(app_module)
