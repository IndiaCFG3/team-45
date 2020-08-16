from app import app
from flask import render_template, request, redirect, flash
from app.forms import LoginForm
from config import db_config

import firebase_admin
from firebase_admin import credentials, auth, firestore
import pyrebase

service_cred = credentials.Certificate('./app/serviceAccountKey.json')
admin_app = firebase_admin.initialize_app(service_cred)

firebase = pyrebase.initialize_app(db_config)
# db = firebase.database()
db = firestore.client()
client_auth = firebase.auth()

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
            doc_ref = db.collection(u'users').document(f'{user.uid}')
            doc_ref.set({
                u'name': name
            })
        except:
            print('database didnt work')
        return redirect('/')


@app.route('/addmobiliser',methods=['GET','POST'])
def addmobiliser():
    if request.method == 'POST':
        doc_ref = db.collection(u'mobilizer').document(f'{mobilizer.moid}')
        name = request.form['name']
        db.child('mobilizer').push({"name": name})
        phone=request.form['phone']
        db.child('mobilizer').push({"phone": phone})
        cid=request.form['cid']
        db.child('mobilizer').push({"center_id": cid})
        tar=request.form['tar']
        return render_template('addmobiliser.html')
    return render_template('addmobiliser.html')

@app.route('/delmobiliser',methods=['GET','POST'])
def delmobiliser():
    if request.method == 'POST':
        name = request.form['name']
        db.child('mobilizer').pop({"name": name})
        phone=request.form['phone']
        db.child('mobilizer').pop({"phone": phone})
        cid=request.form['cid']
        db.child('mobilizer').pop({"center_id": cid})
        tar=request.form['tar']
        db.child('mobilizer').pop({"full_target": tar})
        db.child('mobilizer').push({"full_target": tar})
        doc_ref.set({
            'name':NULL,
            'phone':NULL,
            'center_id':NULL,
            'full_target':NULL
        })
        return render_template('delmobiliser.html')
    return render_template('delmobiliser.html')

@app.route('/updatemobiliser',methods=['GET','POST'])
def updatemobiliser():
    if request.method == 'POST':
        name = request.form['name']
        db.child('mobilizer').update({"name": name})
        phone=request.form['phone']
        db.child('mobilizer').update({"phone": phone})
        cid=request.form['cid']
        db.child('mobilizer').update({"center_id": cid})
        tar=request.form['tar']
        db.child('mobilizer').update({"full_target": tar})

        return render_template('updatemobiliser.html')
    return render_template('updatemobiliser.html')
@app.route('/docs',methods=['GET','POST'])
def docs():
    return render_template('docs.html')
        
    
    
