import os
from urllib import response
import pytest
import requests
from todo_app.app import create_app
from todo_app.data.mongo_items import add_items,get_items
from dotenv import load_dotenv, find_dotenv

import mongomock

@pytest.fixture
def client():
    
    load_dotenv('.env.test', override=True)
    with mongomock.patch(servers=(('fakemongo.com', 27017),)):
        test_app = create_app()
        with test_app.test_client() as client:
            yield client

def test_index_page(client):

    response = client.get('/')
    
    assert response.status_code == 200
    
   # assert 'Test card' in response.data.decode()

def test_add_items(client):
    
    

    add_items('test item','')
    response = client.get('/')
    
    response_html = response.data.decode()
    
    assert 'test item' in response_html

