from firebase_admin import auth

email = " "

link = auth.generate_email_verification_link(email, action_code_settings=None)