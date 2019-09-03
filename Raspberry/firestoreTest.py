import firebase_admin
from firebase_admin import credentials
from google.cloud import firestore
import os

project_id = "smart-water-168ca"

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/pi/Desktop/smart-water-168ca-d9f996738e27.json"

cred = credentials.ApplicationDefault()
firebase_admin.initialize_app(cred, {
  'projectId': project_id,
})

db = firestore.Client()
doc_ref = db.collection(u'entidades').document(u'1')
doc_ref.set({u'tete':u'tete'})

print("Deu Certo!")