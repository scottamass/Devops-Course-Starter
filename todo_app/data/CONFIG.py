import os
import requests



def BOARD():
    return os.getenv('BOARD')
URL="https://api.trello.com/1/"



def get_list_id(name):
    params = {'key': os.getenv('API'), 'token': os.getenv("TOKEN")}
    trello_lists = requests.get(f'{URL}boards/{BOARD}/lists',params=params).json()
    for l in trello_lists:
        if l['name'] == name:
            id=l['id']          
    return id


def TODO_ID():
    return get_list_id('To-do')

def DOING_LISTID():
    return get_list_id('Doing')
def LISTID_DONE():
    return get_list_id('Done')  