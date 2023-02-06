import datetime
from server import clubs, competitions, book
from tests.conftest import client
from flask import url_for


def test_connection_to_booking_page_for_past_event_should_return_error(client):
    for competition in competitions:
        print("COMPETITION['DATE']", competition["date"])
        date_of_competition = competition["date"]
        if datetime.datetime.strptime(date_of_competition, '%Y-%m-%d %H:%M:%S')<datetime.datetime.today():
            old_competition = competition.copy()
            club = clubs[0].copy()
            print("COMPETITION USE IN TEST", old_competition)
            print("CLUB USE IN TEST", club)
            response = client.get("/book/"+old_competition['name']+"/"+club['name'])
            # response = client.post(url_for('book', competition=old_competition['name'], club=club['name']))
            # response = url_for(book, competition=old_competition['name'], club=club['name'])
            # response = book(competition=old_competition['name'], club=club['name'])
            print("response", response)
            print("response.status_code", response.status_code)
            print("response.data", response.data)
            print("Old competitions was found ! :)")
            assert response.status_code == 200
            assert b"<li>Sorry, this competition is in the past</li>" in response.data
    
def test_connection_to_booking_page_for_event_in_the_futur_should_return_how_many_places(client):
    for competition in competitions:
        print("COMPETITION['DATE']", competition["date"])
        date_of_competition = competition["date"]
        if datetime.datetime.strptime(date_of_competition, '%Y-%m-%d %H:%M:%S')>datetime.datetime.today():
            next_competition = competition.copy()
            club = clubs[0].copy()
            print("COMPETITION USE IN TEST", next_competition)
            print("CLUB USE IN TEST", club)
            response = client.get("/book/"+next_competition['name']+"/"+club['name'])
            print("response", response)
            print("response.status_code", response.status_code)
            print("response.data", response.data)
            print("Next competitions was found ! :)")
            assert response.status_code == 200
            assert b"How many places?" in response.data
            
def test_connection_to_booking_page_for_event_in_the_futur_but_club_does_not_have_enough_points_should_return_error(client, mocker):
    for competition in competitions:
        print("COMPETITION['DATE']", competition["date"])
        date_of_competition = competition["date"]
        if datetime.datetime.strptime(date_of_competition, '%Y-%m-%d %H:%M:%S')>datetime.datetime.today():
            next_competition = competition
            connected_club = clubs[0]
            mocker.patch.dict(connected_club, {"points": "0"})
            print("COMPETITION USE IN TEST", next_competition)
            print("CLUB USE IN TEST", connected_club)
            response = client.get("/book/"+next_competition['name']+"/"+connected_club['name'])
            print("response", response)
            print("response.status_code", response.status_code)
            print("response.data", response.data)
            print("Next competitions was found ! :)")
            assert response.status_code == 200
            assert b"Sorry, you don&#39;t have enough points to book a place" in response.data
            
def test_connection_to_booking_page_for_event_in_the_futur_but_there_is_no_place_left_in_competition(client, mocker):
    for competition in competitions:
        print("COMPETITION['DATE']", competition["date"])
        date_of_competition = competition["date"]
        if datetime.datetime.strptime(date_of_competition, '%Y-%m-%d %H:%M:%S')>datetime.datetime.today():
            next_competition = competition.copy()
            club = clubs[0].copy()
            mocker.patch.dict(competition, {'numberOfPlaces': '0'})
            print("COMPETITION USE IN TEST", next_competition)
            print("CLUB USE IN TEST", club)
            response = client.get("/book/"+next_competition['name']+"/"+club['name'])
            print("response", response)
            print("response.status_code", response.status_code)
            print("response.data", response.data)
            print("Next competitions was found ! :)")
            assert response.status_code == 200
            assert b"Sorry, there are no places left for this competition" in response.data
            
def test_connection_to_booking_page_for_event_in_the_futur_but_foundClub_does_not_exists(client, mocker):
    for competition in competitions:
        print("COMPETITION['DATE']", competition["date"])
        date_of_competition = competition["date"]
        if datetime.datetime.strptime(date_of_competition, '%Y-%m-%d %H:%M:%S')>datetime.datetime.today():
            next_competition = competition.copy()
            club = clubs[0].copy()
            mocker.patch.dict(competition, {'name': 'Fake Name'})
            print("COMPETITION USE IN TEST", next_competition)
            print("CLUB USE IN TEST", club)
            response = client.get("/book/"+next_competition['name']+"/"+club['name'])
            print("response", response)
            print("response.status_code", response.status_code)
            print("response.data", response.data)
            print("Next competitions was found ! :)")
            assert response.status_code == 200
            assert b"Sorry, this competition or club does not exist" in response.data
