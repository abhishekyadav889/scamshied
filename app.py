from flask import Flask, request, jsonify
from flask_cors import CORS
import google.genai as genai
import os
from dotenv import load_dotenv
from firebase_helper import save_to_firebase

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

app = Flask(__name__)
CORS(app)


def analyze_message(user_message):
    prompt = f"""
    You are a scam detection expert for India.
    Analyze this message and respond in EXACTLY this format:

    SCAM_SCORE: (0 to 100)
    VERDICT: (SCAM or SAFE or SUSPICIOUS)
    REASON: (2 simple sentences explaining why)
    WARNING: (one sentence of advice for the user)

    Message: {user_message}
    """
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return response.text
    except Exception as e:
        print(f"❌ Gemini error: {e}")
        return None


@app.route("/")
def home():
    return "ScamShield Backend is Running!"


@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        data = request.get_json()

        # Check if request body exists
        if not data:
            return jsonify({"error": "No data received"}), 400

        # Check if message field exists
        if "message" not in data:
            return jsonify({"error": "Please send a message"}), 400

        message = data["message"].strip()

        # Check for empty message
        if not message:
            return jsonify({"error": "Message cannot be empty"}), 400

        # Check for too short message
        if len(message) < 5:
            return jsonify({"error": "Message too short"}), 400

        # Check for too long message
        if len(message) > 5000:
            return jsonify({"error": "Message too long. Max 5000 characters"}), 400

        # Analyze with Gemini
        result = analyze_message(message)

        # Check if Gemini failed
        if result is None:
            return jsonify({"error": "Analysis failed. Please try again"}), 500

        # Save to Firebase
        try:
            save_to_firebase(message, result)
        except Exception as e:
            print(f"❌ Firebase error: {e}")
            # Don't crash — just continue even if Firebase fails

        return jsonify({
            "success": True,
            "result": result
        })

    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return jsonify({"error": "Something went wrong. Please try again"}), 500


if __name__ == "__main__":
    print("ScamShield Backend Starting...")
app.run(debug=True, port=5000, host="0.0.0.0")