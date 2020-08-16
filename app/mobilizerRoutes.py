from app import app
from flask import render_template, request, redirect, flash
from app.forms import LoginForm
from config import db_config

import firebase_admin
from firebase_admin import credentials, auth, firestore
import pyrebase


service_cred = credentials.Certificate('./app/serviceAccountKey.json')
admin_app = admin.initialize_app(service_cred)

firebase = pyrebase.initialize_app(db_config)
# db = firebase.database()
db = firestore.client()
client_auth = firebase.auth()

@app.route('/courses/<centre_id>', methods=['GET', 'POST'])
def getAllCourses(centre_id):
    if request.method == 'GET':
        docs = db.collection(u'course').where(u'centre_id', u'==', centre_id).stream()

        for doc in docs:
            courseDict = doc.to_dict()
            print(f'{doc.id}, {doc.to_dict()}')

    else:
        centre_id = 234
        name = request.form['name']
        target = request.form['target']
        db.collection(u'course').document().set({
            u'name': name,
            u'centre_id': centre_id
            u'target': target
        })

@app.route('/leads/<mobilizer_id>', methods = ['GET', 'POST'])
def getAllLeads(mobilizer_id):
     if request.method = 'GET':
        docs = db.collection(u'lead').where(u'mobilizer_id', u'==', mobilizer_id).stream()

        for doc in docs:
            leadDict = doc.to_dict()
            print(f'{doc.id}, {leadDict}')

    else:
        name = request.form['name']
        phone = request.form['phone']
        interests = request.form['interests']
        education = request.form['education']
        course = db.collection('course').where(u'name', '==', f'{request.form['course']}').limit(1).stream()
        course_id = course[0].id

        docs = db.collection(u'lead').document().update({
            u'name': name,
            u'phone': phone,
            u'interest': interests,
            u'education': education,
            u'mobilizer_id': mobilizer_id,
            u'course_id': course_id,
            u'status': status
        })

@app.route('/activities/<mobilizer_id>', methods = ['GET', 'POST'])
def getActivities():
    if request.method = 'GET':
        docs = db.collection(u'activity').where(u'mobilizer_id', u'==', mobilizer_id).stream()
        
    else:
        db.collection(u'activity').document().update({
            name 
        })

# getAllCourses(1)