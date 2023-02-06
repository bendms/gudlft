import pytest
import server
from server import clubs, competitions, saveClubs, saveCompetitions, loadClubs, loadCompetitions
from tests.conftest import client
import os

def test_json_contains_clubs_exists():
    assert os.path.exists("clubs.json")
    
def test_json_contains_competitions_exists():
    assert os.path.exists("competitions.json")
        
def test_clubs_list_not_empty():
    assert len(clubs)>0
    
def test_competitions_list_not_empty():
    assert len(competitions)>0
    
def test_clubs_json_contains_simply_lift():
    for club in clubs:
        if club["name"]=="Simply Lift":
            simply_lift = club
    assert simply_lift
    
def test_competitions_json_contains_simply_lift():
    for competition in competitions:
        if competition["name"]=="Spring Festival":
            spring_festival = competition
    assert spring_festival

def test_save_clubs_in_json():
    clubs = server.clubs
    print("CLUBS", clubs)
    server.saveClubs(clubs=clubs)
    clubs_saved_in_json = server.loadClubs()
    print("CLUBS_SAVED_IN_JSON", clubs_saved_in_json)
    assert clubs == clubs_saved_in_json
    
def test_save_competitions_in_json():
    competitions = server.competitions
    print("COMPETITIONS", competitions)
    server.saveCompetitions(competitions=competitions)
    competitions_saved_in_json = server.loadCompetitions()
    print("COMPETITIONS_SAVED_IN_JSON", competitions_saved_in_json)
    assert competitions == competitions_saved_in_json
    
    
# def test_mock_clubs_from_json_file(monkeypatch):
#     test_clubs = [{
#             "name": "Club 1",
#             "email": "club_1@mail.com",
#             "points": "20",
#             "places": []
#         },
#         {
#             "name": "Club 2",
#             "email": "club_2@mail.com",
#             "points": "20",
#             "places": [
#                 {
#                     "name": "Competition for end of 2023",
#                     "date": "2023-10-22 13:30:00",
#                     "number": 10
#                 },
#                 {
#                     "name": "Competition for end of 2024",
#                     "date": "2024-10-22 13:30:00",
#                     "number": 10
#                 }
#             ]
#         },
#         {
#             "name": "Club 3",
#             "email": "club_3@mail.com",
#             "points": "15"
#         }]
#     # def mockreturn():
#     #     return test_clubs
    
#     monkeypatch.setattr(server, 'loadClubs', test_clubs)
    
#     expected_value = test_clubs
#     assert loadClubs() == expected_value

# def test_mock_clubs_from_json_file(mocker):
#     test_clubs = [{
#             "name": "Club 1",
#             "email": "club_1@mail.com",
#             "points": "20",
#             "places": []
#         },
#         {
#             "name": "Club 2",
#             "email": "club_2@mail.com",
#             "points": "20",
#             "places": [
#                 {
#                     "name": "Competition for end of 2023",
#                     "date": "2023-10-22 13:30:00",
#                     "number": 10
#                 },
#                 {
#                     "name": "Competition for end of 2024",
#                     "date": "2024-10-22 13:30:00",
#                     "number": 10
#                 }
#             ]
#         },
#         {
#             "name": "Club 3",
#             "email": "club_3@mail.com",
#             "points": "15"
#         }]
    
#     mocker.patch('server.loadClubs', return_value=test_clubs)
    
#     expected_value = test_clubs
#     assert loadClubs() == expected_value
    
# def test_try_to_save_clubs_in_json_file(monkeypatch):
#     test_clubs = [{
#         "name": "Club 1",
#         "email": "test@email.com",
#         "points": "10"
#     },
#     {
#         "name": "Club 2",
#         "email": "test@email.com",
#         "points": "20"
#     },
#     {
#         "name": "Club 3",
#         "email": "test@email.com",
#         "points": "30"
#     }]
#     with patch.dict(server.clubs, test_clubs):
#         saveClubs()
#         assert server.clubs == test_clubs

    # saveClubs(test_clubs)
    # loadClubs()
    # content of test_tmp_path.py

# def test_load_fake_data_in_json(mocker):
#     mocker.patch("server.loadJson", return_value=[{
#         "name": "Club 1",
#         "email": "test@email.com",
#         "points": "10"
#     },
#     {
#         "name": "Club 2",
#         "email": "test@email.com",
#         "points": "20"
#     },
#     {
#         "name": "Club 3",
#         "email": "test@email.com",
#         "points": "30"
#     }])