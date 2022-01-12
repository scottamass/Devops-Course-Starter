
from flask import Flask ,render_template, sessions, request,redirect, url_for

from todo_app.data.session_items import add_item, get_items ,get_item


from todo_app.flask_config import Config

app = Flask(__name__)
app.config.from_object(Config())


@app.route('/')
def index():
    


    return render_template('index.html',items = get_items())

@app.route('/submit', methods=['POST'] )
def submit():
    if request.method =='POST':
        title=request.form.get('title')
        add_item(title)
        return redirect(url_for('index'))
#

@app.route("/complete<id>", methods=['PUT'])
def complete(id):
    
        get_item(id).status = "done"
        
        
        return redirect(url_for('index'))