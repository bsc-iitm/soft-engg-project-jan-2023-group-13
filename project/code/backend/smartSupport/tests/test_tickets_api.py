import requests

# from flask import request
from main import app

JWT = ''


def test_login():
    global JWT
    response = app.test_client().post('/api/user/login', json={
        "username": "jdoe",
        "password": "pass123"
    })
    JWT = response.get_json()['access_token']
    # print(JWT)
    assert response.status_code == 200


def test_get_tickets():
    test_login()
    response =  app.test_client().get('/api/tickets?page=0&per_page=10',
                                       headers={'Authorization': 'Bearer ' + JWT})
    assert response.status_code == 200