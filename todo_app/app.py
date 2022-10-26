


from flask import Flask ,render_template, request,redirect, url_for
from todo_app.data.CONFIG import *
from todo_app.data.trello_items import get_trello_items, get_username , add_trello_item, delete_trello_item,set_item_to_done,set_item_to_doing
from todo_app.data.views import ViewModel
from todo_app.data.mongo_items import add_items, get_items,mongo_start,mongo_done,mongo_delete
from flask_login import LoginManager, UserMixin, current_user,login_required, login_user,AnonymousUserMixin,logout_user





from todo_app.flask_config import Config
class User(UserMixin):
	def __init__(self,id):
		self.id = id
		self.is_reader = True
		#78789252
		if id=="78789252":
			self.roles=['reader','writer']
		else:
			self.roles=['reader']

WRITER ='writer'
READER= 'reader'
class Anonymous(AnonymousUserMixin):
	def __init__(self):
		self.id = 1
		self.roles=['reader','writer']

def create_app():
		app = Flask(__name__)
		app.config.from_object(Config())
		if os.getenv('LOGIN_DISABLED') is None:
			app.config['LOGIN_DISABLED'] = False
		else:
			app.config['LOGIN_DISABLED'] = True

		login_manager = LoginManager()
		
		@login_manager.unauthorized_handler
		def unauthenticated():
			red_url=f"https://github.com/login/oauth/authorize?client_id={os.getenv('GITHUB_CLIENT_ID')}"
			return redirect(red_url)

		@login_manager.user_loader
		def load_user(user_id):
			return User(user_id)

		login_manager.init_app(app)	
		login_manager.anonymous_user = Anonymous	

		LOGIN_DISABLED = app.config['LOGIN_DISABLED']
		@app.route('/')
		@login_required
		def index():
			if (LOGIN_DISABLED or 'reader' in current_user.roles):	
				#items = get_trello_items()
				items = get_items()
				item_view_model=ViewModel(items)
				DEV=os.getenv("DEV")
				print(current_user.id)
				return render_template('index.html', view_items=item_view_model,  env=DEV, user=current_user)
		
		@app.route('/login/callback')
		def callback():
			auth_code = request.args['code']
			print(auth_code)
			access_toker_url="https://github.com/login/oauth/access_token"
			q_params={"client_id":os.getenv('GITHUB_CLIENT_ID'),"client_secret":os.getenv('GITHUB_SECRET_ID'),"code":auth_code}
			headers={"Accept":"application/json"}
			response= requests.post(access_toker_url, params=q_params,headers=headers)
			access_token = response.json()['access_token']
			user_info_url = "https://api.github.com/user"
			auth_header = {'Authorization':f'Bearer {access_token}'}
			user_info_response = requests.get(user_info_url,headers=auth_header)
			user_id=user_info_response.json()['id']
			user =User(user_id)
			login_user(user)
			return redirect('/')
		@app.route('/logout')
		def logout():
			logout_user()
			return "loged out"	
		@app.route('/submit', methods=['POST'] )
		@login_required
		def submit():
			if (LOGIN_DISABLED or 'writer' in current_user.roles):
				if request.method =='POST':
					if current_user.is_writer:
						title=request.form.get('title')
						
						
						preprocessed_date =request.form.get('due_date')
								
							
						
						add_items(title,preprocessed_date)
						return redirect(url_for('index') )
					else:
						return  "not authorised"



		@app.route("/complete/<id>", methods=['POST'])
		@login_required
		def complete(id):
			if (LOGIN_DISABLED or 'writer' in current_user.roles):
				mongo_done(id)
				#set_item_to_done(id)
				return redirect(url_for('index'))
			else:
				return  "not authorised"

		@app.route("/doing/<id>", methods=['POST'])
		@login_required
		def doing(id):
			if (LOGIN_DISABLED or 'writer' in current_user.roles):
				#set_item_to_doing(id)
				mongo_start(id)
				return redirect(url_for('index'))        
			else:
				return  "not authorised"
		@app.route("/delete/<id>", methods=['POST'])
		@login_required
		def delete(id): 
			if (LOGIN_DISABLED or 'writer' in current_user.roles):
				#delete_trello_item(id) 
				mongo_delete(id)
				return redirect(url_for('index')) 
			else:
				return  "not authorised"	       
		return app

