

from flask import Flask ,render_template,  request,redirect, url_for

from todo_app.data.session_items import add_item, delete_item, get_items ,get_item,save_item
from todo_app.data.functions import tasks




from todo_app.flask_config import Config

app = Flask(__name__)
app.config.from_object(Config())


@app.route('/')
def index():
    
    
    items = sorted(get_items(), key=lambda i: i['status'] ,reverse=False)
    compleated = tasks("done")
    outstanding = tasks("Not Started") 
    return render_template('index.html', items=items, user="user", compleated = compleated, outstanding=outstanding)

@app.route('/submit', methods=['POST'] )
def submit():
    if request.method =='POST':
        title=request.form.get('title')
        add_item(title)
        return redirect(url_for('index') )


@app.route("/complete/<id>", methods=['POST'])
def complete(id):
    
        item=get_item(id)
        item['status'] ="done"
        save_item(item)
        
        
        return redirect(url_for('index'))

@app.route("/doing/<id>", methods=['POST'])
def doing(id):
    
        item=get_item(id)
        item['status'] ="In Progress"
        save_item(item)
        
        
        return redirect(url_for('index'))        

@app.route("/delete/<id>", methods=['POST'])
def delete(id):
    
        
        item=get_item(id)
        delete_item(item) 
        
        
        return redirect(url_for('index'))        