

from flask import Flask ,render_template, request,redirect, url_for
from todo_app.data.CONFIG import *
from todo_app.data.trello_items import get_trello_items, get_username , add_trello_item, delete_trello_item,set_item_to_done,set_item_to_doing,Item



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
        if request.form.get('due_date') != 'None':
                preprocessed_date=request.form.get('due_date')
                print (preprocessed_date)
                due_month=preprocessed_date[3:5]
                due_day=preprocessed_date[0:2]
                due_year= preprocessed_date[5:10]
                total=(f'{due_month}/{due_day}{due_year}')
                due_date=total
        add_trello_item(title,due_date)
        return redirect(url_for('index') )


@app.route("/complete/<id>", methods=['POST'])
def complete(id):
        set_item_to_done(id)
        return redirect(url_for('index'))

@app.route("/doing/<id>", methods=['POST'])
def doing(id):
        set_item_to_doing(id)
        return redirect(url_for('index'))        

@app.route("/delete/<id>", methods=['POST'])
def delete(id): 
        delete_trello_item(id) 
        return redirect(url_for('index'))        


