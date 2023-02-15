from unittest import mock
from unittest.mock import patch
from locust import HttpUser, between, task


class ProjectPerfTest(HttpUser):
    await_time = between(5, 10)
    
    @task
    def index(self):
        self.client.get("/")
    @task    
    def login(self):
        self.client.post("/showSummary", data={
            "email": "admin@irontemple.com"
        })
    
    @task
    def bookPlaces(self):
        self.client.get("/book/Competition%20for%20end%20of%202023/Iron%20Temple")
    
    @task 
    def purchasePlaces(self):
        self.client.post("/purchasePlaces", data={
            "club": "Iron Temple",
            "competition": "Competition for end of 2023",
            "places": 1
        })
        
    @task
    def logout(self):
        self.client.get("/logout")
