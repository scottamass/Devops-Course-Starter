import pymongo 
import os
from todo_app.data.item import Item
from datetime import date, datetime
from bson.objectid import ObjectId


def get_items():
    
    db = pymongo.MongoClient(os.getenv("MONGO_CONNECTION_STRING"))
    map=db[os.getenv("MONGO_DATABASE_NAME")]
    todos=map.todo_items
    results =todos.find()
    items = []
    for r in results:
        item = Item.from_trello_card(r)
        items.append(item)
    return items
def add_items(title:str,dates):    
    item={'name':title, 'status':'To Do','dateLastActivity':date.today().strftime('%d-%m-%Y'),  'due':dates}
    db = pymongo.MongoClient(os.getenv("MONGO_CONNECTION_STRING"))
    map=db[os.getenv("MONGO_DATABASE_NAME")]
    todos=map.todo_items
    todos.insert_one(item)

def mongo_done(id):
    db = pymongo.MongoClient(os.getenv("MONGO_CONNECTION_STRING"))
    map=db[os.getenv("MONGO_DATABASE_NAME")]
    todos=map.todo_items

    query_params={'$set':{'status':'Done'}}
    todos.update_one({'_id':ObjectId(id)},query_params)

def mongo_start(id):
    db = pymongo.MongoClient(os.getenv("MONGO_CONNECTION_STRING"))
    map=db[os.getenv("MONGO_DATABASE_NAME")]
    todos=map.todo_items

    query_params={'$set':{'status':'Doing'}}
    todos.update_one({'_id':ObjectId(id)},query_params)

def mongo_delete(id):
    db = pymongo.MongoClient(os.getenv("MONGO_CONNECTION_STRING"))
    map=db[os.getenv("MONGO_DATABASE_NAME")]
    todos=map.todo_items

    
    todos.delete_one({'_id':ObjectId(id)})