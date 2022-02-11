import requests

from todo_app.data.CONFIG import *

def get_username():
    params = {'key': API, 'token': TOKEN}
    user_name=requests.get(f'{URL}members/me',params=params).json()

    return user_name 

def get_trello_items():
    
    params = {'key': API, 'token': TOKEN}
    all = requests.get(f'{URL}boards/MLtxybJW/cards',params=params).json()
    
    return all

def add_trello_item(title):
    params = {'key': API, 'token': TOKEN,'idList':TODO_ID,'name':title }
    requests.post(f'{URL}cards',params=params )
    