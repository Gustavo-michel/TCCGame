from firebase_admin import auth

email = " "

link = auth.generate_password_reset_link(email, action_code_settings=None)