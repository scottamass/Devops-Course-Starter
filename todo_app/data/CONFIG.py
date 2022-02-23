import os
import requests


TOKEN=os.getenv("TOKEN")
API=os.getenv('API')
BOARD=os.getenv('BOARD')
URL="https://api.trello.com/1/"


def get_list_id(name):
    params = {'key': API, 'token': TOKEN}
    trello_lists = requests.get(f'{URL}boards/{BOARD}/lists',params=params).json()
    for l in trello_lists:
        if l['name'] == name:
            id=l['id']          
    return id



TODO_ID=get_list_id('To-do')
DOING_LISTID=get_list_id('Doing')
LISTID_DONE=get_list_id('Done')  