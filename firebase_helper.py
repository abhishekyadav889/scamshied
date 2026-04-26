import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime

# Initialize Firebase
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
        print(f"❌ Firebase save failed: {e}")
        return False