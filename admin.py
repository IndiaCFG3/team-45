import firebase_admin
from firebase_admin import credentials, auth, firestore
from config import db_config

import pyrebase

creds = credentials.Certificate('app/serviceAccountKey.json')
default_app = firebase_admin.initialize_app(creds)

firebase = pyrebase.initialize_app(db_config)
db = firestore.client()
client_auth = firebase.auth()

# bhavya@gmail.com
# bhavya

user = auth.get_user_by_email(f'bhavya@gmail.com')
# final = auth.set_custom_user_claims(user.uid, {
#     "admin": True
# })

# print(user.uid, user.displayName)
# user = auth.get_user_by_email('harsh@gmail.com')
# print(user.custom_claims.get('admin'))
# print(user)
# print(final)

# resp = db.child('users').child(user.uid).push({"name": "bhavya sheth"})
# print(resp)
# doc_ref = db.collection(u'users').document(f'{user.uid}')
# doc_ref.set({
#     u'name': 'bhavya sheth'
# })

def getAllCourses(centre_id):
    # docs = db.collection(u'center').stream()

    # for doc in docs:
        # print(f'{doc.id}, {doc.to_dict()}')
    centre_id = 234
    name = 'Tally'
    target = 10
    doc_ref = db.collection(u'course').document(f'{name}')

    doc_ref.set({
        u"name": name,
        u"centre_id": centre_id,
        u"target": target
    })

getAllCourses(1)

# users = db.child("users").get()
# print(users.val())