import datetime
from server import clubs, competitions, book
from tests.conftest import client
from flask import url_for




def test_valid_email_for_connection(client):
    valid_email = "admin@irontemple.com"
    response = client.post('/showSummary', data={
        "email": valid_email
    })
    assert response.status_code == 200
    
def test_connection_to_application_should_return_200(client):
    response = client.get('/')
    assert response.status_code == 200
    
# def test_connection_to_booking_page_should_return_200(client):
#     club = clubs[0]
#     competition = competitions[0]
#     response = client.post('/book/'+competition['name']+'/'+club['name'])
#     print("RESPONSE", response)

    
            

