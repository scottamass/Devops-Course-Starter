from sys import ps1
from flask import Flask ,render_template, sessions, request
from todo_app.data.session_items import add_item, get_items


from todo_app.flask_config import Config

app = Flask(__name__)
app.config.from_object(Config())


@app.route('/')
def index():
    


    return render_template('index.html',items = get_items())

@app.route('/submit', methords =['POST'])
def submit():
    if request.methord =='POST':
        pass


