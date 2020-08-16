from app import app
from flask import render_template, request, redirect, flash
from app.forms import LoginForm
from config import db_config

import firebase_admin
from firebase_admin import credentials, auth, firestore
import pyrebase


service_cred = credentials.Certificate('/home/bhavya_sheth/Desktop/jpmc45/app/serviceAccountKey.json')
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
        name = 'Tally'
        target = 10
        doc_ref = db.collection(u'course').document().set({
            u'name': name,
            u'centre_id': centre_id
            u'target': target
        })



# getAllCourses(1)