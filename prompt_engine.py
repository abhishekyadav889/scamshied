import google.genai as genai
import os
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def analyze_message(user_message):
    prompt = f"""
    You are a scam detection expert specializing in India.
    A user has received this message and wants to know if it is a scam.
    Analyze it carefully and respond in EXACTLY this format:

    SCAM_SCORE: (a number from 0 to 100. 100 = definitely scam, 0 = definitely safe)
    VERDICT: (write only one word: SCAM or SAFE or SUSPICIOUS)
    REASON: (explain in exactly 2 simple sentences why you gave this verdict)
    WARNING: (write one simple sentence of advice for the user)

    Rules:
    - Look for prize claims, urgent bank requests, OTP requests, lottery wins
    - Look for poor grammar, urgency, threats about account closure
    - Indian scam patterns: KYC expired, TRAI notices, lottery wins, job offers , bank account issues , etc.

    Message to analyze: {user_message}
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return response.text


# ■■ TEST CASES ■■
test_messages = [
    "Dear customer, your TRAI notice is pending. Pay Rs 500 immediately to avoid disconnection.",
    "Congratulations! You won Rs 50,000 lottery. Send bank details now.",
    "Your KYC is expired. Your account will be blocked in 24 hours. Click link.",
    "Hi, meeting tomorrow at 10am in the college canteen. Don't forget.",
    "Dear customer your SBI account is suspended. Call 9876543210 immediately.",
    "Your bank account has been compromised. Verify your details immediately."
    "Congratulations! You have won a free trip to Goa. Click here to claim your prize."
    "URGENT: Your PAN card is expiring. Update now to avoid penalties."
    "Your Amazon order has been delayed. Click here to track your package."  # This one is safe
    "Your phone number has won a lottery. Send your bank details to claim the prize."  # Scam
    "Your account has been suspended due to suspicious activity. Click here to verify your identity."  # Scam
    "Congratulations! You have been selected for a free gift card. Click here to claim."  # Scam
    "Your KYC is expired. Please update your details to avoid account suspension."  # Suspicious
    "Your TRAI notice is pending. Please pay the bill to avoid disconnection."  # Suspicious
    "Your bank account has been compromised. Please verify your details immediately."  # Suspicious
    "Your Amazon order has been delayed. Please click here to track your package."  # Safe
    "Hi, meeting tomorrow at 10am in the college canteen. Don't forget."  # Safe
]

for msg in test_messages:
    print("=" * 50)
    print("MESSAGE:", msg[:60])
    print("ANALYSIS:")
    print(analyze_message(msg))
    print()