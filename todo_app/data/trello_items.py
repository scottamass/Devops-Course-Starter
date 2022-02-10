import requests

from todo_app.data.CONFIG import *
def get_items():
    
    params = {'key': API, 'token': TOKEN}
    all = requests.get(f'{URL}',params=params).json()
    
    return all