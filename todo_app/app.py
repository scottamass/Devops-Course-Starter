


import functools
from flask import Flask ,render_template, request,redirect, url_for,flash
from todo_app.data.CONFIG import *
from todo_app.data.trello_items import get_trello_items, get_username , add_trello_item, delete_trello_item,set_item_to_done,set_item_to_doing
from todo_app.data.views import ViewModel
from todo_app.data.mongo_items import add_items, get_items, make_admin, make_writer,mongo_start,mongo_done,mongo_delete,add_user_to_db,load_user_from_db, user_list_create,make_admin,ban_user
from flask_login import LoginManager, UserMixin, current_user,login_required, login_user,AnonymousUserMixin,logout_user





from todo_app.flask_config import Config
class User(UserMixin):
	def __init__(self,name,id,roles):
		self.name =name
		self.id = id
		self.roles = roles
# commented out but left in for evidence of module 11 parts 1 to 3 
""" 		if id==78789252:
			self.roles=['writer','reader']
		else:
			self.roles=['reader'] """

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

		def writer_required(func):
			@functools.wraps(func)
			def forbidden_if_not_writer_func(*args, **kwargs):
				if LOGIN_DISABLED or "writer" not in current_user.roles:
					flash('you do not have the correct permission')
					return redirect(url_for('index'))
				else:
					return func(*args, **kwargs)
			return forbidden_if_not_writer_func	


		def admin_required(func):
			@functools.wraps(func)
			def forbidden_if_not_admin_func(*args, **kwargs):
				if LOGIN_DISABLED or "admin" not in current_user.roles:
					flash('you do not have the correct permission')
					return redirect(url_for('index'))
				else:
					return func(*args, **kwargs)
			return forbidden_if_not_admin_func	

		def banned(func):
			@functools.wraps(func)
			def forbidden_if_banned_func(*args, **kwargs):
				if  "banned" in current_user.roles:
					
					return redirect(url_for('ban_page'))
				else:
					return func(*args, **kwargs)
			return forbidden_if_banned_func		
		login_manager = LoginManager()
		
		@login_manager.unauthorized_handler
		def unauthenticated():
			red_url=f"https://github.com/login/oauth/authorize?client_id={os.getenv('GITHUB_CLIENT_ID')}"
			return redirect(red_url)

		@login_manager.user_loader
		def load_user(user_id):
			u =load_user_from_db(user_id)
			
			#return User(user_id)
			#return load_user_from_db(user_id)
			return User(name=u['name'], id=u['id'], roles=u['roles'])
		login_manager.init_app(app)	
		login_manager.anonymous_user = Anonymous	

		LOGIN_DISABLED = app.config['LOGIN_DISABLED']
		@app.route('/')
		@login_required
		@banned
		def index():
			
			if (LOGIN_DISABLED or 'reader' in current_user.roles):	
				#items = get_trello_items()
				items = get_items()
				item_view_model=ViewModel(items)
				DEV=os.getenv("DEV")
				return render_template('index.html', view_items=item_view_model,  env=DEV, user=current_user)
		
		@app.route('/login/callback')
		def callback():
			auth_code = request.args['code']
			#print(auth_code)
			access_toker_url="https://github.com/login/oauth/access_token"
			q_params={"client_id":os.getenv('GITHUB_CLIENT_ID'),"client_secret":os.getenv('GITHUB_SECRET_ID'),"code":auth_code}
			headers={"Accept":"application/json"}
			response= requests.post(access_toker_url, params=q_params,headers=headers)
			access_token = response.json()['access_token']
			user_info_url = "https://api.github.com/user"
			auth_header = {'Authorization':f'Bearer {access_token}'}
			user_info_response = requests.get(user_info_url,headers=auth_header)
			user_name=user_info_response.json()['login']
			print(user_name)
			user_id=user_info_response.json()['id']
			user =User(user_name,user_id,'reader')
			login_user(user)
			add_user_to_db(current_user)
			
			
			return redirect('/')
		@app.route('/logout')
		def logout():
			logout_user()
			return "loged out"

		@app.route('/getd')
		def data():
			print(current_user.id)
			print(current_user.name)
			print(current_user.roles)	
			return redirect(url_for('index'))

		@app.route('/submit', methods=['POST'] )
		@login_required
		@writer_required
		def submit():
			#if (LOGIN_DISABLED or 'writer' in current_user.roles):
				if request.method =='POST':
					
						title=request.form.get('title')
						
						
						preprocessed_date =request.form.get('due_date')
								
							
						
						add_items(title,preprocessed_date)
						return redirect(url_for('index') )
			#	else:
			#		return  "not authorised"



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


		@app.route("/admin")
		@login_required
		@admin_required
		def admin(): 
			
				
				
				users = user_list_create()
				return render_template('admin-page.html', users=users) 
	       
		
		
		@app.route("/make_admin/<id>", methods=['POST'])
		@login_required
		@admin_required
		def user_admin(id):
			
				make_admin(id)
				
				return redirect(url_for('admin'))


		@app.route("/make_writer/<id>", methods=['POST'])
		@login_required
		@admin_required
		def user_writer(id):
			
				make_writer(id)
				
				return redirect(url_for('admin'))
			
		
		@app.route("/disable_account/<id>", methods=['POST'])
		@login_required
		@admin_required
		def ban_hammer(id):
			
				ban_user(id)
				
				return redirect(url_for('admin'))


		@app.route('/banned')
		def ban_page():
			return render_template('banned.html')		
			
		return app


		
