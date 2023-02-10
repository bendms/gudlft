from server import clubs, competitions
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
