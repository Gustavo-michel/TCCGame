from firebase_admin import auth
from firebase_admin import credentials
import requests

cred = credentials.Certificate("firebase_key.json")

firebase_admin.initialize_app(cred)

email = requests.post("")

user = auth.get_user_by_email(email)

print(f"User id is: {user}")

# from flask import Flask, request, jsonify
# app = Flask(__name__)


# @app.route('/login', methods=['POST'])
# def login():
#     email = request.json['email']
#     password = request.json['password']

#     try:
#         user = auth.get_user_by_email(email)
#         user = auth.sign_in_with_email_and_password(email, password)
#         return jsonify({"success": True, "message": "Login bem-sucedido!"}), 200
#     except Exception as e:
#         return jsonify({"success": False, "message": str(e)}), 400