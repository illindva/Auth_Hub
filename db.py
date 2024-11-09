import sqlite3
from datetime import datetime, timezone

def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS Authorizations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        application TEXT NOT NULL,
        login_type TEXT NOT NULL,
        username TEXT NOT NULL,
        password TEXT NOT NULL,
        db_host TEXT,
        db_service_name TEXT,
        db_port TEXT,
        created TEXT NOT NULL,
        encryption_flag TEXT NOT NULL
    )''')

    # Initialize Users table
    cursor.execute('''CREATE TABLE IF NOT EXISTS Users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        user_type TEXT NOT NULL,
        user_role TEXT NOT NULL,
        approval_status TEXT NOT NULL DEFAULT 'No'
    )''')

    conn.commit()
    conn.close()

def insert_user(username, password, email, user_type, user_role, approval_status='No'):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO Users (username, password, email, user_type, user_role, approval_status)
                      VALUES (?, ?, ?, ?, ?, ?)''',
                   (username, password, email, user_type, user_role, approval_status))
    conn.commit()
    conn.close()

def get_user_by_username(username):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Users WHERE username = ?', (username,))
    user = cursor.fetchone()
    conn.close()
    return user

def get_users_by_role(role):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Users WHERE user_role = ?', (role,))
    users = cursor.fetchall()
    conn.close()
    return users


def get_user_by_id(user_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user


def update_approval_status(user_id, status):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE Users SET approval_status = ? WHERE id = ?', (status, user_id))
    conn.commit()
    conn.close()

def insert_record(record):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    # Store the created field in UTC
    created_utc = datetime.strptime(record['created'], "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc)

    cursor.execute('''INSERT INTO Authorizations (application, login_type, username, password, db_host, db_service_name, db_port, created, encryption_flag)
                             VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                   (record['application'], record['login_type'], record['username'], record['password'],
                    record['db_host'], record['db_service_name'], record['db_port'], created_utc.isoformat(),
                    record['encryption_flag']))
    conn.commit()
    conn.close()


def get_records():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Authorizations')
    records = cursor.fetchall()
    conn.close()
    return [dict(
        id=row[0],
        application=row[1],
        login_type=row[2],
        username=row[3],
        password=row[4],
        db_host=row[5],
        db_service_name=row[6],
        db_port=row[7],
        created=row[8],
        encryption_flag=row[9]
    ) for row in records]


def get_record_by_id(record_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Authorizations WHERE id=?', (record_id,))
    record = cursor.fetchone()
    conn.close()
    if record:
        return {
            'id': record[0],
            'application': record[1],
            'login_type': record[2],
            'username': record[3],
            'password': record[4],
            'db_host': record[5],
            'db_service_name': record[6],
            'db_port': record[7],
            'created': record[8],
            'encryption_flag': record[9]
        }
    else:
        return None

def delete_record(record_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Authorizations WHERE id=?', (record_id,))
    conn.commit()
    conn.close()