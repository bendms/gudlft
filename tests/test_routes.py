# from server import clubs, competitions, book
# from tests.conftest import client
# from flask import url_for

# def test_index_should_return_200(client):
#     response = client.get('/')
#     assert response.status_code == 200
    
# def test_show_summary_should_return_200(client):
#     response = client.post('/showSummary', data={
#         "email": "admin@irontemple.com"
#     })
#     assert response.status_code == 200
    
# def test_book_should_return_200(client):
#     club = clubs[0]
#     competition = competitions[0]
#     response = client.post('/book/'+competition['name']+'/'+club['name'])
#     assert response.status_code == 200

# def test_purchasing_should_return_200(client):
#     club = clubs[0]
#     competition = competitions[0]
#     response = client.post('/purchasePlaces')
#     assert response.status_code == 200
    
# def test_logout_should_return_200(client):
#     response = client.get('/logout')
#     assert response.status_code == 302