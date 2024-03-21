import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth
from flask import Flask, request, jsonify
app = Flask(__name__)

cred = credentials.Certificate("firebase_key.json")

firebase_admin.initialize_app(cred)

# displayName = input('Enter your name ')
# email = input('Enter your email adress ')
# password = input('Please enter your password ')


@app.route('/account', methods=['POST'])
def signup():
    displayName = request.json['name']
    email = request.json['email']
    password = request.json['password']

    try:
        user = auth.create_user(
            email=email,
            password=password,
            uid=displayName
        )
        return jsonify({"success": True, "message": f"Usuário criado com sucesso! {user.uid}"}), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 400

if __name__ == "__main__":
    app.run()