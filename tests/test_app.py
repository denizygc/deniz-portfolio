import pytest
from flask import url_for
from app import create_app
from app.extensions import db

@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })

    yield app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()

def test_app_creation(app):
    assert app is not None
    assert app.name == 'app'  # Make sure correct app name

def test_healthcheck_route(client):
    # Example route you should have in your app (or create it)
    response = client.get("/healthcheck")
    assert response.status_code == 200
    assert response.json == {"status": "ok"}

def test_blueprints_registered(app):
    # Check if your blueprint is registered correctly
    url_map = [str(rule) for rule in app.url_map.iter_rules()]
    assert "/projects" in " ".join(url_map)  # Adjust if your blueprint URL prefix differs

def test_db_extension_initialized(app):
    # Make sure db is initialized
    assert db.engine is not None
