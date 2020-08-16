from app import app
from flask import render_template, request, redirect, flash
from app.forms import LoginForm
from config import db_config
from app import mobilizerRoutes

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
    if request.method == 'GET':
        doc_ref = db.collection(u'mobilizer').document(f'{mobilizer.moid}')
        # name = request.form['name']
        # db.child('mobilizer').push({"name": name})
        # phone=request.form['phone']
        # db.child('mobilizer').push({"phone": phone})
        # cid=request.form['cid']
        # db.child('mobilizer').push({"center_id": cid})
        # tar=request.form['tar']

        # client_auth.current_user
        return render_template('addmobiliser.html',docs=doc_ref)

    else:
        mobilizer_id=request.form['mobilizer_id']
        name = request.form['name']
        phone=request.form['phone']
        cid=request.form['cid']
        tar=request.form['tar']
        doc_ref = db.collection(u'mobilizer').document().set({
            'mobilizer_id':mobilizer_id,
            'name':name,
            'phone':phone,
            'center_id':cid,
            'full_target':tar
        })
        print(doc_ref.collection(u'mobilizer').document(mobilizer_id))

        return render_template('addmobiliser.html')



@app.route('/mobilizers/<mobilizer_id>', methods=['GET', 'POST'])
def getAllmobilizers(mobilizer_id):
    if request.method == 'GET':
        docs = db.collection(u'mobilizer').stream()

        for doc in docs:
            courseDict = doc.to_dict()
            print(f'{doc.id}, {doc.to_dict()}')

    else:
        name = request.form['name']
        phone=request.form['phone']
        cid=request.form['cid']
        tar=request.form['tar']
        doc_ref = db.collection(u'mobilizer').document().set({
            'mobilizer_id':mobilizer_id,
            'name':name,
            'phone':phone,
            'center_id':cid,
            'full_target':tar
        })
    return render_template("home.html")


@app.route('/deletemobilizers', methods=['GET', 'POST'])
def deletemobilizers():
    name = request.form['name']
    phone=request.form['phone']
    cid=request.form['cid']
    tar=request.form['tar']
    if request.method == 'GET':
        docs = db.collection(u'mobilizer').where(u'mobilizer_id', u'!=', mobilizer_id).stream()

        for doc in docs:
            courseDict = doc.to_dict()
            print(f'{doc.id}, {doc.to_dict()}')

    else:
        doc_ref = db.collection(u'mobilizer').document(u'mobilizer_id')
        doc_ref.update({
        'mobilizer_id':firestore.DELETE_FIELD,
        'name':firestore.DELETE_FIELD,
        'phone':firestore.DELETE_FIELD,
        'center_id':firestore.DELETE_FIELD,
        'full_target':firestore.DELETE_FIELD,
        })

@app.route('/updatemobiliser/<mobilizer_id>', methods = ['GET', 'POST'])
def updatemobiliser(mobilizer_id):
     if request.method == 'POST':
         name = request.form['name']
         phone=request.form['phone']
         cid=request.form['cid']
         tar=request.form['tar']
         doc_ref = db.collection(u'objects').document(u'mobilizer_id')
         doc_ref.update({
         'name':name,
         'phone':phone,
         'center_id':cid,
         'full_target':tar

         })

@app.route('/leads')
def leads():
    return render_template('leads.html')
@app.route('/docs')
def docs():
    a=db.collection.get()
    print(type(a))
