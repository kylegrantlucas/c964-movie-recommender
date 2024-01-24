import pytest
from app import create_app

@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })
    
    yield app

@pytest.fixture
def client(app):
    app.Testing = True
    return app.test_client()

@pytest.fixture()
def runner(app):
    return app.test_cli_runner()

# basic test of post request
def test_post(client):
    # print routes on the client
    print(client.application.url_map)
    response = client.post('/recommendations', json={'userInput': 'The Matrix'})
    assert response.status_code == 200