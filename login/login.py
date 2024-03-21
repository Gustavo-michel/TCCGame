from firebase_admin import auth
from firebase_admin import credentials
from flask import Flask, request, jsonify
app = Flask(__name__)

# cred = credentials.Certificate("firebase_key.json")

# firebase_admin.initialize_app(cred)


@app.route('/login', methods=['POST'])
def login():
    email = request.json['email']
    password = request.json['password']

    try:
        user = auth.get_user_by_email(email)
        user = auth.sign_in_with_email_and_password(email, password)
        return jsonify({"success": True, "message": f"Login bem-sucedido! {user.email}"}), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 400
    
    
if __name__ == "__main__":
    app.run()
    