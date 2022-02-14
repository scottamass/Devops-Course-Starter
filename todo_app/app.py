

from flask import Flask ,render_template, request,redirect, url_for

from todo_app.data.session_items import add_item, delete_item, get_items ,get_item,save_item
from todo_app.data.functions import tasks
from todo_app.data.CONFIG import *
from todo_app.data.trello_items import get_trello_items, get_username , add_trello_item, delete_trello_item,done_trello_item,doing_trello_item,Item



from todo_app.flask_config import Config


app = Flask(__name__)
app.config.from_object(Config())


@app.route('/')
def index():
   
    
    items = get_trello_items()
    name = get_username()
    return render_template('index.html', items=items, name=name, todo=TODO_ID, doing=DOING_LISTID, done=LISTID_DONE)

@app.route('/submit', methods=['POST'] )
def submit():
    if request.method =='POST':
        title=request.form.get('title')
        add_trello_item(title)
        return redirect(url_for('index') )


@app.route("/complete/<id>", methods=['POST'])
def complete(id):
    
        done_trello_item(id)
        
        
        return redirect(url_for('index'))

@app.route("/doing/<id>", methods=['POST'])
def doing(id):
    
        doing_trello_item(id)
        
        
        return redirect(url_for('index'))        

@app.route("/delete/<id>", methods=['POST'])
def delete(id):
    
        
        
        delete_trello_item(id) 
        
        
        return redirect(url_for('index'))        


