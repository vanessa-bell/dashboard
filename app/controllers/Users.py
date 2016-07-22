from system.core.controller import *

class Users(Controller):
    def __init__(self, action):
        super(Users, self).__init__(action)
        self.load_model('User')
        self.load_model('Message')
        self.db = self._app.db

    def index(self):
        """
        A loaded model is accessible through the models attribute 
        self.models['WelcomeModel'].get_users()
        
        self.models['WelcomeModel'].add_message()
        # messages = self.models['WelcomeModel'].grab_messages()
        # user = self.models['WelcomeModel'].get_user()
        # to pass information on to a view it's the same as it was with Flask
        
        # return self.load_view('index.html', messages=messages, user=user)
        """
        return self.load_view('index.html')

    def signin(self):
        return self.load_view('signin.html')

    def register(self):
        return self.load_view('register.html')

    def dashboard(self):
        users = self.models['User'].get_users()
        return self.load_view('dashboard.html',users=users)

    def show(self,id):
        user = self.models['User'].get_user(id)
        first_name = user[0]['first_name']
        return self.load_view('show.html',user=user[0],first_name=first_name)


    def create(self,methods=['POST']):
        user_info = request.form
        create_status = self.models['User'].create_new(user_info)
        print create_status['status']
        if create_status['status'] == True:
            session['id'] = create_status['user']['id']
            session['first_name'] = create_status['user']['first_name']
            return redirect('/dashboard')
        else:
            for message in create_status['errors']:
                flash(message, 'error')
            return redirect('/register')

    def login(self,methods=['POST']):
        info = request.form
        print "this is request info", info
        if self.models['User'].login_user(info) == False:
            flash("Invalid login!",'error')
            print "there is no user"
            return redirect('/signin')
        else:
            user = self.models['User'].login_user(info)
            session['id'] = user['id']
            session['first_name'] = user['first_name']
            print "successful login", session['id']
            return redirect('/dashboard')
    
    def logoff(self):
        session.pop('id')
        flash("You are now logged out",'error')
        return redirect('/')