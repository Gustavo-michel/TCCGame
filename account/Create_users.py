import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth

cred = credentials.Certificate("firebase_key.json")

firebase_admin.initialize_app(cred)


displayName = input('Enter your name ')
email = input('Enter your email adress ')
password = input('Please enter your password ')


user = auth.create_user( email = email, password = password, uid = displayName)

print(f"User created sucessfully: {user.uid}")


# @app.route('/signup', methods=['POST'])
# def signup():
#     email = request.json['email']
#     password = request.json['password']

#     try:
#         user = auth.create_user(
#             email=email,
#             password=password
#         )
#         return jsonify({"success": True, "message": "Usuário criado com sucesso!"}), 200
#     except Exception as e:
#         return jsonify({"success": False, "message": str(e)}), 400