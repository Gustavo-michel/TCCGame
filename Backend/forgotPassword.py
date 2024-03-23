from firebase_admin import auth
from flask import Flask, request

app = Flask(__name__)

email = request.form['email']

link = auth.generate_password_reset_link(email, action_code_settings=None)

if __name__ == "__main__":
    app.run()