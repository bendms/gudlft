import pytest
from server import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def saveClubs_mocked(clubs):
    print("CLUBS", clubs)
    clubs_to_save_to_json = {"clubs" : []}
    [clubs_to_save_to_json["clubs"].append(i) for i in clubs]
    print("clubs_to_save_to_json_in_mock_function", clubs_to_save_to_json)
    return clubs_to_save_to_json

@pytest.fixture
def saveCompetitions_mocked(competitions):
    print("COMPETITIONS", competitions)
    competitions_to_save_to_json = {"competitions" : []}
    [competitions_to_save_to_json["competitions"].append(i) for i in competitions]
    print("competitions_to_save_to_json_in_mock_function", competitions_to_save_to_json)
    return competitions_to_save_to_json
