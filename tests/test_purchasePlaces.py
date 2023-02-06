import unittest
from unittest import mock
import datetime
import server
from server import clubs, competitions, book
from tests.conftest import client, saveClubs_mocked, saveCompetitions_mocked
from flask import url_for



def test_purchase_more_than_12_places_for_event_in_the_futur_should_return_error(client):
    for competition in competitions:
        print("COMPETITION['DATE']", competition["date"])
        date_of_competition = competition["date"]
        if datetime.datetime.strptime(date_of_competition, '%Y-%m-%d %H:%M:%S')>datetime.datetime.today():
            next_competition = competition
            club = clubs[0]
            print("COMPETITION USE IN TEST", next_competition)
            print("CLUB USE IN TEST", club)
            response = client.post("/purchasePlaces", data={
                "club": club['name'],
                "competition": next_competition['name'],
                "places": 13
            })
            print("response", response)
            print("response.status_code", response.status_code)
            print("response.data", response.data)
            assert response.status_code == 200
            assert b"Achat impossible car vous ne pouvez pas acheter plus de 12 places" in response.data
            
def test_purchase_negative_number_of_places_for_event_in_the_futur_should_return_error(client):
    for competition in competitions:
        print("COMPETITION['DATE']", competition["date"])
        date_of_competition = competition["date"]
        if datetime.datetime.strptime(date_of_competition, '%Y-%m-%d %H:%M:%S')>datetime.datetime.today():
            next_competition = competition
            club = clubs[0]
            print("COMPETITION USE IN TEST", next_competition)
            print("CLUB USE IN TEST", club)
            response = client.post("/purchasePlaces", data={
                "club": club['name'],
                "competition": next_competition['name'],
                "places": -1
            })
            print("response", response)
            print("response.status_code", response.status_code)
            print("response.data", response.data)
            assert response.status_code == 200
            assert b"Achat impossible car vous ne pouvez pas acheter moins de 1 place" in response.data   
            
def test_purchase_places_without_put_number_for_event_in_the_futur_should_return_error(client):
    for competition in competitions:
        print("COMPETITION['DATE']", competition["date"])
        date_of_competition = competition["date"]
        if datetime.datetime.strptime(date_of_competition, '%Y-%m-%d %H:%M:%S')>datetime.datetime.today():
            next_competition = competition
            club = clubs[0]
            print("COMPETITION USE IN TEST", next_competition)
            print("CLUB USE IN TEST", club)
            response = client.post("/purchasePlaces", data={
                "club": club['name'],
                "competition": next_competition['name'],
                "places": ValueError
            })
            print("response", response)
            print("response.status_code", response.status_code)
            print("response.data", response.data)
            assert response.status_code == 200
            assert b"Achat impossible car vous devez indiquer le nombre de place" in response.data   




# def saveClubs_mocked(clubs):
#     print("CLUBS", clubs)
#     clubs_to_save_to_json = {"clubs" : []}
#     [clubs_to_save_to_json["clubs"].append(i) for i in clubs]
#     print("clubs_to_save_to_json_in_mock_function", clubs_to_save_to_json)
    
# def saveCompetitions_mocked(competitions):
#     print("COMPETITIONS", competitions)
#     competitions_to_save_to_json = {"competitions" : []}
#     [competitions_to_save_to_json["competitions"].append(i) for i in competitions]
#     print("competitions_to_save_to_json_in_mock_function", competitions_to_save_to_json)

# class TestRandom(unittest.TestCase):
#     @mock.patch('__main__.urandom', side_effect=simple_urandom)
#     def test_urandom(self, urandom_function):
#         assert urandom(5) == 'fffff'
        

# @mock.patch('server.purchasePlaces', side_effect=saveClubs)
# @mock.patch('server.purchasePlaces', side_effect=saveCompetitions)
# def test_purchase_places_with_correct_input_without_saving_in_json(self, saveClubs, saveCompetitions):
#     for competition in competitions:
#         print("COMPETITION['DATE']", competition["date"])
#         date_of_competition = competition["date"]
#         if datetime.datetime.strptime(date_of_competition, '%Y-%m-%d %H:%M:%S')>datetime.datetime.today():
#             next_competition = competition
#             club = clubs[0]
#             print("COMPETITION USE IN TEST", next_competition)
#             print("CLUB USE IN TEST", club)
#             response = client.post("/purchasePlaces", data={
#                 "club": club['name'],
#                 "competition": next_competition['name'],
#                 "places": 1
#             })
#             print("response", response)
#             print("response.status_code", response.status_code)
#             print("response.data", response.data)
#             assert response.status_code == 200
#             assert b"Great-booking complete!" in response.data 

# class TestPurchase(unittest.TestCase):
#     @mock.patch('server.saveClubs', side_effect=saveClubs_mocked)
#     @mock.patch('server.saveCompetitions', side_effect=saveCompetitions_mocked)
#     def test_purchase_places_with_correct_input_without_saving_in_json(self, saveCompetitions, saveClub):
#         for competition in competitions:
#             print("COMPETITION['DATE']", competition["date"])
#             date_of_competition = competition["date"]
#             if datetime.datetime.strptime(date_of_competition, '%Y-%m-%d %H:%M:%S')>datetime.datetime.today():
#                 next_competition = competition.copy()
#                 club = clubs[0].copy()
#                 print("COMPETITION USE IN TEST", next_competition)
#                 print("CLUB USE IN TEST", club)
#                 # server.purchasePlaces()
#                 response = client.post("/purchasePlaces", data={
#                     "club": club['name'],
#                     "competition": next_competition['name'],
#                     "places": 1
#                 })
#                 print("response", response)
#                 print("response.status_code", response.status_code)
#                 print("response.data", response.data)
#                 # assert response.status_code == 200
#                 assert b"Great-booking complete!" in response.data 



def test_sum_of_places_already_bought_and_places_required_exceed_12_should_return_error(client, mocker):
    for competition in competitions:
        print("COMPETITION['DATE']", competition["date"])
        date_of_competition = competition["date"]
        if datetime.datetime.strptime(date_of_competition, '%Y-%m-%d %H:%M:%S')>datetime.datetime.today():
            next_competition = competition
            club = clubs[0]
            mocker.patch.dict(club, {"points": 10})
            mocker.patch.dict(club, {"places": [
                {
                    "name": next_competition["name"],
                    "date": next_competition["date"],
                    "number": 10
                }]})
            print("COMPETITION USE IN TEST", next_competition)
            print("CLUB USE IN TEST", club)
            response = client.post("/purchasePlaces", data={
                "club": club['name'],
                "competition": next_competition['name'],
                "places": 3
            })
            print("response", response)
            print("response.status_code", response.status_code)
            print("response.data", response.data)
            assert response.status_code == 200
            assert b"Achat impossible car vous ne pouvez pas acheter plus de 12 places" in response.data 
            
def test_purchase_places_with_correct_input_and_ticket_already_exist_in_json_without_saving_in_json(client, mocker):
    for competition in competitions:
        print("COMPETITION['DATE']", competition["date"])
        date_of_competition = competition["date"]
        if datetime.datetime.strptime(date_of_competition, '%Y-%m-%d %H:%M:%S')>datetime.datetime.today():
            next_competition = competition
            club = clubs[0]
            mocker.patch.dict(club, {"places": [
                {
                    "name": next_competition["name"],
                    "date": next_competition["date"],
                    "number": 10
                }]})
            print("COMPETITION USE IN TEST", next_competition)
            print("CLUB USE IN TEST", club)
            
            mocker.patch('server.saveClubs', return_value=saveClubs_mocked)
            mocker.patch('server.saveCompetitions', return_value=saveCompetitions_mocked)
            response = client.post("/purchasePlaces", data={
                "club": club['name'],
                "competition": next_competition['name'],
                "places": 2
            })
            print("response", response)
            print("response.status_code", response.status_code)
            print("response.data", response.data)
            assert response.status_code == 200
            assert b"Great-booking complete!" in response.data 
            
def test_purchase_places_with_correct_input_without_saving_in_json(client, mocker):
    for competition in competitions:
        print("COMPETITION['DATE']", competition["date"])
        date_of_competition = competition["date"]
        if datetime.datetime.strptime(date_of_competition, '%Y-%m-%d %H:%M:%S')>datetime.datetime.today():
            next_competition = competition
            club = clubs[0]
            mocker.patch.dict(club, {"places": [
                {
                    "name": next_competition["name"],
                    "date": next_competition["date"],
                    "number": 10
                }]})
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