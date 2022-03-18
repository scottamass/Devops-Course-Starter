import requests
from todo_app.data.CONFIG import *
from todo_app.data.item import Item




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




    