import datetime
from server import clubs, competitions

def test_book_should_return_200(client):
    club = clubs[0]
    competition = competitions[0]
    response = client.get('/book/'+competition['name']+'/'+club['name'])
    assert response.status_code == 200
    
def test_connection_to_booking_page_for_past_event_should_return_error(client):
    for competition in competitions:
        date_of_competition = competition["date"]
        if datetime.datetime.strptime(date_of_competition, '%Y-%m-%d %H:%M:%S')<datetime.datetime.today():
            old_competition = competition.copy()
            club = clubs[0].copy()
            response = client.get("/book/"+old_competition['name']+"/"+club['name'])
            assert response.status_code == 200
            assert b"<li>Sorry, this competition is in the past</li>" in response.data
    
def test_connection_to_booking_page_for_event_in_the_futur_should_return_how_many_places(client):
    for competition in competitions:
        date_of_competition = competition["date"]
        if datetime.datetime.strptime(date_of_competition, '%Y-%m-%d %H:%M:%S')>datetime.datetime.today():
            next_competition = competition.copy()
            club = clubs[0].copy()
            response = client.get("/book/"+next_competition['name']+"/"+club['name'])
            assert response.status_code == 200
            assert b"How many places?" in response.data
            
def test_connection_to_booking_page_for_event_in_the_futur_but_club_does_not_have_enough_points_should_return_error(client, mocker):
    for competition in competitions:
        date_of_competition = competition["date"]
        if datetime.datetime.strptime(date_of_competition, '%Y-%m-%d %H:%M:%S')>datetime.datetime.today():
            next_competition = competition
            connected_club = clubs[0]
            mocker.patch.dict(connected_club, {"points": "0"})
            response = client.get("/book/"+next_competition['name']+"/"+connected_club['name'])
            assert response.status_code == 200
            assert b"Sorry, you don&#39;t have enough points to book a place" in response.data
            
def test_connection_to_booking_page_for_event_in_the_futur_but_there_is_no_place_left_in_competition(client, mocker):
    for competition in competitions:
        date_of_competition = competition["date"]
        if datetime.datetime.strptime(date_of_competition, '%Y-%m-%d %H:%M:%S')>datetime.datetime.today():
            next_competition = competition.copy()
            club = clubs[0].copy()
            mocker.patch.dict(competition, {'numberOfPlaces': '0'})
            response = client.get("/book/"+next_competition['name']+"/"+club['name'])
            assert response.status_code == 200
            assert b"Sorry, there are no places left for this competition" in response.data
            
def test_connection_to_booking_page_for_event_in_the_futur_but_foundClub_does_not_exists(client, mocker):
    for competition in competitions:
        date_of_competition = competition["date"]
        if datetime.datetime.strptime(date_of_competition, '%Y-%m-%d %H:%M:%S')>datetime.datetime.today():
            next_competition = competition.copy()
            club = clubs[0].copy()
            mocker.patch.dict(competition, {'name': 'Fake Name'})
            response = client.get("/book/"+next_competition['name']+"/"+club['name'])
            assert response.status_code == 200
            assert b"Sorry, this competition or club does not exist" in response.data
