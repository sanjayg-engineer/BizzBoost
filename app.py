from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials, auth

# Initialize Flask app
app = Flask(__name__)

# Load Firebase service account key
cred = credentials.Certificate("G:\FP\serviceAccountKey.json")
firebase_admin.initialize_app(cred)

@app.route("/signup", methods=["POST"])
def signup():
    try:
        data = request.json
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return jsonify({"error": "Email and password are required"}), 400

        # Create user in Firebase
        user = auth.create_user(
            email=email,
            password=password
        )

        # Generate email verification link
        verification_link = auth.generate_email_verification_link(email)

        return jsonify({
            "message": "User created successfully. Please verify your email.",
            "uid": user.uid,
            "verification_link": verification_link
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/")
def home():
    return "✅ Flask + Firebase is running!"


if __name__ == "__main__":
    app.run(debug=True)
