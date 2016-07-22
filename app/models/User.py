from system.core.model import Model
import re
from time import strftime 

class User(Model):
    def __init__(self):
        super(User, self).__init__()

    def create_new(self, info):
        EMAIL_REGEX = re.compile(r'^[a-za-z0-9\.\+_-]+@[a-za-z0-9\._-]+\.[a-za-z]*$')
        NAME_REGEX = re.compile(r'^[a-zA-Z ]+$')
        errors = []
        if not info['first_name']:
            errors.append('First name cannot be blank')
        elif len(info['first_name']) < 2:
            errors.append('First name must be at least 2 characters long')
        elif not NAME_REGEX.match(info['first_name']):
            errors.append('First name must be letters only')
        if not info['last_name']:
            errors.append('Last name cannot be blank')
        elif len(info['last_name']) < 2:
            errors.append('Last name must be at least 2 characters long')
        elif not NAME_REGEX.match(info['last_name']):
            errors.append('Last name must be letters only')
        if not info['email']:
            errors.append('Email cannot be blank')
        elif not EMAIL_REGEX.match(info['email']):
            errors.append('Email format must be valid!')
        
        if not info['password']:
            errors.append('Password cannot be blank')
        elif len(info['password']) < 8:
            errors.append('Password must be at least 8 characters long')
        elif info['password'] != info['confirm_pw']:
            errors.append('Password and confirmation must match!')
        if errors:
            return {'status': False, 'errors':errors}
        else:    
            password = info['password']
            print "expected password", password 
            hashed_pw = self.bcrypt.generate_password_hash(password)
            create_query = "INSERT INTO users (first_name, last_name, email, pw_hash, created_at, updated_at) VALUES (:first_name, :last_name, :email, :pw_hash, NOW(), NOW())"            
            create_data = {'first_name': info['first_name'], 'last_name': info['last_name'], 'email': info['email'], 'pw_hash': hashed_pw}
            self.db.query_db(create_query, create_data)
            get_user_query = "SELECT * FROM users ORDER BY id DESC LIMIT 1"
            users = self.db.query_db(get_user_query)
            return {'status':True, 'user': users[0]}


    def login_user(self,info,methods='POST'):
        password = info['password']
        print "password", password
        user_query = "SELECT * FROM users WHERE email = :email LIMIT 1"
        user_data = {'email': info['email']}
        user = self.db.get_one(user_query, user_data)
        if user:
            if self.bcrypt.check_password_hash(user.pw_hash, password):
                return user
        return False

    def get_users(self):
        query = 'SELECT * FROM users'
        return self.db.query_db(query)

    def get_user(self, id):
        query = "SELECT * from users where id = :id"
        data = {'id': id}
        return self.db.query_db(query, data)



        