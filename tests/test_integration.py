import unittest
from unittest import mock
import datetime
import server
from server import clubs, competitions, book
from tests.conftest import client, saveClubs_mocked, saveCompetitions_mocked
from flask import url_for



def test_full_customer_usage_login_book_places_and_purchase_places_and_logout(client, mocker):
    # Access to website
    response = client.get('/')
    assert response.status_code == 200
    assert b'Welcome to the GUDLFT' in response.data
    assert b'Nom du club' in response.data
    assert b'Nombre de points' in response.data
    # Login
    valid_email = "admin@irontemple.com"
    response = client.post('/showSummary', data={
        "email": valid_email
    })
    assert response.status_code == 200
    assert b'Nom du club' in response.data
    assert b'Nombre de points' in response.data
    # Access to booking page
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
    # Purchase places
        print("COMPETITION['DATE']", competition["date"])
        date_of_competition = competition["date"]
        if datetime.datetime.strptime(date_of_competition, '%Y-%m-%d %H:%M:%S')>datetime.datetime.today():
            next_competition = competition
            club = clubs[0]
            print("COMPETITION USE IN TEST", next_competition)
            print("CLUB USE IN TEST", club)
            mocker.patch('server.saveClubs', return_value=saveClubs_mocked)
            mocker.patch('server.saveCompetitions', return_value=saveCompetitions_mocked)
            response = client.post("/purchasePlaces", data={
                "club": club['name'],
                "competition": next_competition['name'],
                "places": 1
            })
            print("response", response)
            print("response.status_code", response.status_code)
            print("response.data", response.data)
            assert response.status_code == 200
            assert b"Great-booking complete!" in response.data 
    # Logout
    response = client.get('/logout')
    print('======================= last response in full test =======================', response.data)
    assert response.status_code == 302
    assert b'Redirecting...' in response.data
        
        
