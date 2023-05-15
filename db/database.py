import sqlite3


def create_tables():
    conn = sqlite3.connect('site.db')
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS users
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                user_role TEXT NOT NULL DEFAULT 'user')''')

    c.execute('''CREATE TABLE IF NOT EXISTS sessions
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                created_at DATETIME NOT NULL,
                ip_address TEXT NOT NULL,
                is_active INTEGER DEFAULT 1,
                FOREIGN KEY (user_id) REFERENCES users (id))''')

    conn.commit()
    conn.close()


def get_user_by_ip(ip_address):
    conn = sqlite3.connect('site.db')
    c = conn.cursor()

    c.execute(
        'SELECT users.* FROM users JOIN sessions ON users.id = sessions.user_id WHERE sessions.ip_address = ? AND sessions.is_active = 1',
        (ip_address,))
    user = c.fetchone()

    conn.close()

    return user


def get_user_by_username(username):
    conn = sqlite3.connect('site.db')
    c = conn.cursor()

    c.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = c.fetchone()

    conn.close()

    return user


def create_user(username, password):
    conn = sqlite3.connect('site.db')
    c = conn.cursor()

    c.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))

    conn.commit()
    conn.close()


def create_session(user_id, ip_address):
    conn = sqlite3.connect('site.db')
    c = conn.cursor()

    c.execute('INSERT INTO sessions (user_id, created_at, ip_address) VALUES (?, datetime("now"), ?)',
              (user_id, ip_address))

    conn.commit()
    conn.close()


def logout_db(ip_address):
    conn = sqlite3.connect('site.db')
    c = conn.cursor()

    c.execute('UPDATE sessions SET is_active = 0 WHERE ip_address = ? AND is_active = 1', (ip_address,))

    conn.commit()
    conn.close()


def get_all_users():
    conn = sqlite3.connect('site.db')
    c = conn.cursor()

    c.execute('SELECT * FROM users')
    users = c.fetchall()

    conn.close()

    return users


def delete_user(user_id):
    conn = sqlite3.connect('site.db')
    c = conn.cursor()

    c.execute('DELETE FROM users WHERE id = ?', (user_id,))

    conn.commit()
    conn.close()
