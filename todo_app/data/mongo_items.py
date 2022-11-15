import pymongo 
import os

from requests import delete
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

def add_user_to_db(user):

    db_user={'name':user.name, 'id':user.id, 'roles':user.roles}
    db_admin={'name':user.name, 'id':user.id, 'roles':['admin','writer','reader']}
    
    db = pymongo.MongoClient(os.getenv("MONGO_CONNECTION_STRING"))
    map=db[os.getenv("MONGO_DATABASE_NAME")]
    users=map.users
    if users.find_one({'id':user.id}):
        print('user in db')
        
        return None
    else:
        print('user not in db')   
        print (users)
        db_users=user_list_create()
        if len(db_users) ==0:
            users.insert_one(db_admin)
        else: users.insert_one(db_user)    
            
        

def load_user_from_db(user):
    
    db = pymongo.MongoClient(os.getenv("MONGO_CONNECTION_STRING"))
    map=db[os.getenv("MONGO_DATABASE_NAME")]
    users_from_db=map.users
    loged_user= users_from_db.find_one({'id':int(user)})
    
    return loged_user


def user_list_create():
    user_list=[]
    db = pymongo.MongoClient(os.getenv("MONGO_CONNECTION_STRING"))
    map=db[os.getenv("MONGO_DATABASE_NAME")]
    users=map.users
    for user in users.find():
        user_list.append(user)
    return user_list    



def make_admin(id):

    db = pymongo.MongoClient(os.getenv("MONGO_CONNECTION_STRING"))
    map=db[os.getenv("MONGO_DATABASE_NAME")]
    users_from_db=map.users
    request_user =users_from_db.find_one({'id':int(id)})
    if "admin" in request_user['roles']:
        print('you are admin')
        query_params={'$pull':{'roles':'admin'}}
        users_from_db.update_one({'id':int(id)},query_params)
    else:    
        query_params={'$push':{'roles':'admin'}}
        users_from_db.update_one({'id':int(id)},query_params)

def make_writer(id):

    db = pymongo.MongoClient(os.getenv("MONGO_CONNECTION_STRING"))
    map=db[os.getenv("MONGO_DATABASE_NAME")]
    users_from_db=map.users
    request_user =users_from_db.find_one({'id':int(id)})
    if "writer" in request_user['roles']:
        print('you are admin')
        query_params={'$pull':{'roles':'writer'}}
        users_from_db.update_one({'id':int(id)},query_params)
    else:    
        query_params={'$push':{'roles':'writer'}}
        users_from_db.update_one({'id':int(id)},query_params)

def ban_user(id):
    
    db = pymongo.MongoClient(os.getenv("MONGO_CONNECTION_STRING"))
    map=db[os.getenv("MONGO_DATABASE_NAME")]
    users_from_db=map.users
    blacklist = map.blacklist
    request_user =users_from_db.find_one({'id':int(id)})
    if "banned" in request_user['roles']:
        print('you are banned')
        query_params={'$pull':{'roles':'banned'}}
        users_from_db.update_one({'id':int(id)},query_params)
        map.blacklist.delete_one({'id':int(id)}
        )
    else:    
        query_params={'$push':{'roles':'banned'}}
        users_from_db.update_one({'id':int(id)},query_params)
        map.blacklist.insert_one({'id':int(id)})


