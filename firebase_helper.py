import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
import os
import json

if not firebase_admin._apps:
    if os.getenv("FIREBASE_KEY"):
        key_dict = json.loads(os.getenv("FIREBASE_KEY"))
        cred = credentials.Certificate(key_dict)
    else:
        cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

def save_to_firebase(message, result):
    try:
        doc = {
            "message": message,
            "result": result,
            "timestamp": datetime.now()
        }
        db.collection("scam_analyses").add(doc)
        print("✅ Saved to Firebase!")
        return True
    except Exception as e:
        print(f"❌ Firebase error: {e}")
        return False