import os

import requests



def BOARD():
    return os.getenv('BOARD')
URL="https://api.trello.com/1/"



def get_list_id(name):
    params = {'key': os.getenv('API'), 'token': os.getenv("TOKEN")}
#    print('making request')
    response = requests.get(f'{URL}boards/{BOARD()}/lists',params=params)
#    print(response.status_code)
#    print(response.text)
    trello_lists = response.json()
    for l in trello_lists:
        if l['name'] == name:
            id=l['id']          
#    print(id)
    return id


def TODO_ID():
    todo = get_list_id('To Do')
    return todo

def DOING_LISTID():
    doing = get_list_id('Doing')
    return doing
def LISTID_DONE():
    done = get_list_id('Done')
    return done  