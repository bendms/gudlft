from server import showSummary, app
from tests.conftest import client

def test_connection_to_app(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Welcome to the GUDLFT' in response.data

def test_wrong_email_for_connection(client):
    wrong_email = "test@mail.com"
    response = client.post('/showSummary', data={
        "email": wrong_email
    })
    assert b"Sorry, unable to log in to the app. Your email address is incorrect" in response.data
    assert response.status_code == 200

def test_valid_email_for_connection(client):
    valid_email = "admin@irontemple.com"
    response = client.post('/showSummary', data={
        "email": valid_email
    })
    assert response.status_code == 200
    


# def test_should_return_200():
#     response = app.test_client().get('/')
#     assert response.status_code == 200
#     assert b'Welcome to the club' in response.data
    
