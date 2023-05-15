from flask import Flask, render_template, request, session, jsonify

from db import database as db
from db.database import create_tables, get_user_by_username, create_user, create_session, logout_db, get_all_users

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

create_tables()


@app.route('/')
def index():
    user = session.get('user')
    if user:
        return render_template('index.html', username=user[1])
    else:
        return render_template('index.html', username=None)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        existing_user = get_user_by_username(username)
        if existing_user:
            return jsonify({'message': 'Username already exists'})

        create_user(username, password)

        return jsonify({'message': 'User created successfully'})
    else:
        return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = get_user_by_username(username)
        if user and user[2] == password:
            create_session(user[0], request.remote_addr)
            session['user'] = user
            return jsonify({'message': 'Logged in successfully'})
        else:
            return jsonify({'message': 'Invalid username or password'})
    else:
        return render_template('login.html')


@app.route('/logout')
def logout():
    if 'user' in session:
        logout_db(request.remote_addr)
        session.pop('user', None)
        return jsonify({'message': 'Logged out successfully'})
    else:
        return jsonify({'message': 'Not logged in'})


@app.route('/admin')
def admin_panel():
    user = session.get('user')
    if user and user[3] == 'admin':
        users = get_all_users()
        return render_template('admin.html', users=users)
    else:
        return "You are not authorized to access this page."


@app.route('/admin/delete-user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    user = session.get('user')
    if user and user[3] == 'admin':
        db.delete_user(user_id)
        return jsonify({'message': 'User deleted successfully'})
    else:
        return jsonify({'message': 'Not authorized'})


if __name__ == '__main__':
    app.run(debug=True)
