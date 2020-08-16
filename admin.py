import firebase_admin
from firebase_admin import credentials, auth, firestore
from config import db_config

import pyrebase

creds = credentials.Certificate('app/serviceAccountKey.json')
default_app = firebase_admin.initialize_app(creds)

firebase = pyrebase.initialize_app(db_config)
db = firestore.client()
client_auth = firebase.auth()

user = auth.get_user_by_email('bhavya@gmail.com')
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
doc_ref = db.collection(u'users').document(f'{user.uid}')
doc_ref.set({
    u'name': 'bhavya sheth'
})

# users = db.child("users").get()
# print(users.val())