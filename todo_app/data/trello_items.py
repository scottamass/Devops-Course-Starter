import requests
from todo_app.data.CONFIG import *


class Item: 
    def __init__(self, id, name, dateLastActivity,due,list,): 
        self.id = id 
        self.name = name
        self.list = list
        self.yearLastActivity = dateLastActivity[0:4]
        self.monthLastActivity = dateLastActivity[5:7]
        self.dayLastActivity = dateLastActivity[8:10]
        self.timeLastActivity = dateLastActivity[11:16]
        self.due= due[8:10]+'-'+due[5:7]+'-'+due[0:4]
        print (self.due)
    @classmethod 
    def from_trello_card(cls, card,list): 
        return cls(card['id'], card['name'], card['dateLastActivity'],card['due'], list['name']) 


def get_username():
    params = {'key': API, 'token': TOKEN}
    user_name=requests.get(f'{URL}members/me',params=params).json()

    return user_name 

def get_trello_items():
    
    params = {'key': API, 'token': TOKEN, 'cards':'open'}
    trello_lists = requests.get(f'{URL}boards/{BOARD}/lists',params=params).json()
    items = []
    for trello_list in trello_lists:
        for trello_card in trello_list['cards']:
            item = Item.from_trello_card(trello_card, trello_list)
            items.append(item)

    return items

def add_trello_item(title,date):
    params = {'key': API, 'token': TOKEN,'idList':TODO_ID,'name':title ,'due':date}
    requests.post(f'{URL}cards',params=params )

def delete_trello_item(card_id):
    
    params = {'key': API, 'token': TOKEN, }
    requests.delete(f'{URL}cards/{card_id}',params=params )

def set_item_to_doing(card_id):
    params = {'key': API, 'token': TOKEN,'idList':DOING_LISTID }
    requests.put(f'{URL}cards/{card_id}',params=params )
def set_item_to_done(card_id):
    params = {'key': API, 'token': TOKEN,'idList':LISTID_DONE }
    requests.put(f'{URL}cards/{card_id}',params=params )       




    