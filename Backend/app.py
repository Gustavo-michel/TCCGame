from firebase_admin import auth
from flask import Flask, request, render_template, redirect, url_for, session
import config

config.connection

app = Flask(__name__, template_folder='../')

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        try:
            user = auth.create_user(
                uid=name,
                email=email,
                password=password,
            )
            print('Usuário criado com sucesso:', user.uid)
            return redirect(url_for('login'))
        except Exception as e:
            print('Erro ao criar usuário:', e)
            return render_template("register/register.html", error='Erro ao criar usuário. Tente novamente.')
        
    return render_template("register/register.html", error=None)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            user = auth.get_user_by_email(email)
            auth_user = auth.sign_in_with_email_and_password(email, password)
            session['user'] = auth_user
            print('Usuário logado com sucesso:', user.uid)
            return redirect(url_for('account'))
        except Exception as e:
            print('Erro ao fazer login:', e)
            return render_template("login.html", error='Erro ao fazer login. Verifique suas credenciais.')
        
    return render_template('login/login.html', error=None)

@app.route('/account')
def account():
    if 'user' in session:
        return render_template('account/account.html')
    else:
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)