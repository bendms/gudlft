import datetime
from server import clubs, competitions

def test_purchasing_should_return_200(client):
    club = clubs[0]
    competition = competitions[0]
    response = client.post('/purchasePlaces', data={
        "club": club['name'],
        "competition": competition['name'],
        "places": 1
    })
    assert response.status_code == 200

def test_purchase_more_than_12_places_for_event_in_the_futur_should_return_error(client):
    for competition in competitions:
        date_of_competition = competition["date"]
        if datetime.datetime.strptime(date_of_competition, '%Y-%m-%d %H:%M:%S')>datetime.datetime.today():
            next_competition = competition
            club = clubs[0]
            response = client.post("/purchasePlaces", data={
                "club": club['name'],
                "competition": next_competition['name'],
                "places": 13
            })
            assert response.status_code == 200
            assert b"Achat impossible car vous ne pouvez pas acheter plus de 12 places" in response.data
            
def test_purchase_negative_number_of_places_for_event_in_the_futur_should_return_error(client):
    for competition in competitions:
        date_of_competition = competition["date"]
        if datetime.datetime.strptime(date_of_competition, '%Y-%m-%d %H:%M:%S')>datetime.datetime.today():
            next_competition = competition
            club = clubs[0]
            response = client.post("/purchasePlaces", data={
                "club": club['name'],
                "competition": next_competition['name'],
                "places": -1
            })
            assert response.status_code == 200
            assert b"Achat impossible car vous ne pouvez pas acheter moins de 1 place" in response.data   
            
def test_purchase_places_without_put_number_for_event_in_the_futur_should_return_error(client):
    for competition in competitions:
        date_of_competition = competition["date"]
        if datetime.datetime.strptime(date_of_competition, '%Y-%m-%d %H:%M:%S')>datetime.datetime.today():
            next_competition = competition
            club = clubs[0]
            response = client.post("/purchasePlaces", data={
                "club": club['name'],
                "competition": next_competition['name'],
                "places": ValueError
            })
            assert response.status_code == 200
            assert b"Achat impossible car vous devez indiquer le nombre de place" in response.data   

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
            response = client.post("/purchasePlaces", data={
                "club": club['name'],
                "competition": next_competition['name'],
                "places": 3
            })
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
            response = client.post("/purchasePlaces", data={
                "club": club['name'],
                "competition": next_competition['name'],
                "places": 2
            })
            assert response.status_code == 200
            assert b"Great-booking complete!" in response.data 
            
def test_purchase_places_with_correct_input_without_saving_in_json(client, mocker):
    for competition in competitions:
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
            response = client.post("/purchasePlaces", data={
                "club": club['name'],
                "competition": next_competition['name'],
                "places": 1
            })
            assert response.status_code == 200
            assert b"Great-booking complete!" in response.data 
