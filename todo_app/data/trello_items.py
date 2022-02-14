import requests
from todo_app.data.CONFIG import *


class Item: 
    def __init__(self, id, name, idList , dateLastActivity): 
        self.id = id 
        self.name = name 
        self.idList = idList 
        self.yearLastActivity = dateLastActivity[0:4]
        self.monthLastActivity = dateLastActivity[5:7]
        self.dayLastActivity = dateLastActivity[8:10]
        self.timeLastActivity = dateLastActivity[11:16]
    @classmethod 
    def from_trello_card(cls, card): 
        return cls(card['id'], card['name'], card['idList'],card['dateLastActivity'] ) 

def get_username():
    params = {'key': API, 'token': TOKEN}
    user_name=requests.get(f'{URL}members/me',params=params).json()

    return user_name 

def get_trello_items():
    
    params = {'key': API, 'token': TOKEN}
    all = requests.get(f'{URL}boards/MLtxybJW/cards',params=params).json()
    items = []
    for card in all:
      item = Item.from_trello_card(card)
      items.append(item)
    return items
def add_trello_item(title):
    params = {'key': API, 'token': TOKEN,'idList':TODO_ID,'name':title }
    requests.post(f'{URL}cards',params=params )

def delete_trello_item(card_id):
    
    params = {'key': API, 'token': TOKEN, }
    requests.delete(f'{URL}cards/{card_id}',params=params )

def doing_trello_item(card_id):
    params = {'key': API, 'token': TOKEN,'idList':DOING_LISTID }
    requests.put(f'{URL}cards/{card_id}',params=params )
def done_trello_item(card_id):
    params = {'key': API, 'token': TOKEN,'idList':LISTID_DONE }
    requests.put(f'{URL}cards/{card_id}',params=params )       