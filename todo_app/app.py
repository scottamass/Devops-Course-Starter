


from flask import Flask ,render_template, request,redirect, url_for
from todo_app.data.CONFIG import *
from todo_app.data.trello_items import get_trello_items, get_username , add_trello_item, delete_trello_item,set_item_to_done,set_item_to_doing
from todo_app.data.views import ViewModel
from todo_app.data.mongo_items import add_items, get_items,mongo_start,mongo_done,mongo_delete





from todo_app.flask_config import Config

def create_app():
        app = Flask(__name__)
        app.config.from_object(Config())



        @app.route('/')
        def index():
                
                #items = get_trello_items()
                items = get_items()
                item_view_model=ViewModel(items)
                DEV=os.getenv("DEV")
				
                return render_template('index.html', view_items=item_view_model,  env=DEV)

        @app.route('/submit', methods=['POST'] )
        def submit():
            if request.method =='POST':
                title=request.form.get('title')
                
                
                preprocessed_date =request.form.get('due_date')
                        
                       
                
                add_items(title,preprocessed_date)
                return redirect(url_for('index') )


        @app.route("/complete/<id>", methods=['POST'])
        def complete(id):
                mongo_done(id)
                #set_item_to_done(id)
                return redirect(url_for('index'))

        @app.route("/doing/<id>", methods=['POST'])
        def doing(id):
                #set_item_to_doing(id)
                mongo_start(id)
                return redirect(url_for('index'))        

        @app.route("/delete/<id>", methods=['POST'])
        def delete(id): 
                #delete_trello_item(id) 
                mongo_delete(id)
                return redirect(url_for('index'))        
        return app

