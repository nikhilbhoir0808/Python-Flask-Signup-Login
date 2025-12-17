from flask import Flask, render_template, request, redirect, url_for, session
import re
import json
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

USER_DATA_FILE = 'users.json'

def load_users():
    if not os.path.exists(USER_DATA_FILE):
        return {}
    try:
        with open(USER_DATA_FILE, 'r') as f:
            content = f.read().strip()
            if not content:
                return {}
            return json.loads(content)
    except json.JSONDecodeError:
        return {}

def save_users(users):
    with open(USER_DATA_FILE, 'w') as f:
        json.dump(users, f)

users = load_users()

def valid_password(password):
    if len(password) < 6:
        return False
    if not re.search(r'[A-Z]', password):
        return False
    if not re.search(r'\W', password):
        return False
    if len(re.findall(r'\d', password)) < 2:
        return False
    return True

@app.route('/')
def home():
    # Now always redirects to /signup
    return redirect(url_for('signup'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    global users
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        if email in users:
            return render_template('signup.html', message='Email already registered!')
        if not valid_password(password):
            return render_template(
                'signup.html',
                message='Password must have at least 1 uppercase letter, 1 symbol, and 2 numbers.'
            )
        users[email] = {'username': username, 'password': password}
        save_users(users)
        return redirect(url_for('login'))
    return render_template('signup.html', message='')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = users.get(email)
        if user and user['password'] == password:
            session['username'] = user['username']
            return render_template('success.html', username=user['username'])
        return render_template('login.html', message='Invalid email or password')
    return render_template('login.html', message='')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
