from app import app
from flask import render_template, request, redirect, flash
from app.forms import LoginForm
from config import db_config
# from firebase import Firebase
import firebase_admin as admin
from firebase_admin import credentials, auth
import pyrebase

firebase = pyrebase.initialize_app(db_config)
db = firebase.database()
client_auth = firebase.auth()

service_cred = credentials.Certificate('/home/bhavya_sheth/Desktop/jpmc45/app/serviceAccountKey.json')
admin_app = admin.initialize_app(service_cred)

@app.route('/')
@app.route('/index')
def index():
    # return render_template('login.html')
    return render_template('home.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    
    else:
        email = request.values.get('email')
        password = request.values.get('password')

        try:
            cred = client_auth.sign_in_with_email_and_password(email, password)
            print('Successfully logged in')
            flash('Login successful!')
            return redirect('/')
        except:
            flash('Incorrect email or password. Please try again!')
            print('Error during login')
            return redirect('/login')

        print(f"email is: {request.values.get('email')}")


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    form=LoginForm()
    print(request)
    if request.method == 'GET':
        return render_template('signup.html')
    
    else:
        email = request.form['email']
        password = request.form['password']
        print(request.form)
        try:
            admin = request.form['admin']
        except:
            admin = 'off'
        name = request.form['fname'] + ' ' + request.form['lname']
        print(f'name is {name}')

        # Sign up user 
        try:
            creds = client_auth.create_user_with_email_and_password(email, password)
            print(creds)
            print('sign up successful') 
        except:
            flash('Sign up failed. Please try again!')
            print('error during sign up')
            return redirect('/signup')

        #give user admin role
        try:
            user = auth.get_user_by_email(email)
            if admin == 'on':  
                auth.set_custom_user_claims(user.uid, {'admin': True})
            else:
                auth.set_custom_user_claims(user.uid, {'admin': False})

            print(f'successfully made custom claims on {user.uid}')
            # print(custom_token)
        except:
            flash('Admin role not given. Please try again!')
            # print(custom_token)
            print('error during custom claim')
            return redirect('/index')

        #add name in user db
        try:
            db.child('users').child(user.uid).push({"name": name})
        except:
            print('database didnt work')
        return redirect('/')

        
    