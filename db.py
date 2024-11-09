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