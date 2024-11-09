import os
import pytz
from pytz import timezone
from dotenv import load_dotenv
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash
from db import init_db, insert_record, get_records, get_record_by_id, delete_record
from encryption_util import encrypt_password, decrypt_password

# Load environment variables from .env file
load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv('APP_SECRET_KEY', '0123456789')

#Database Initialization
def setup():
    init_db()
setup()

@app.route('/', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        application = request.form['application']
        login_type = request.form['login_type']
        username = request.form['username']
        password = request.form['password']
        db_host = request.form.get('db_host')
        db_service_name = request.form.get('db_service_name')
        db_port = request.form.get('db_port')
        created = request.form['created']
        encryption_flag = request.form['encryption_flag']

        if encryption_flag == 'Yes':
            encrypted_password = encrypt_password(password)
        else:
            encrypted_password = password

        record = {
            'application': application,
            'login_type': login_type,
            'username': username,
            'password': encrypted_password,
            'db_host': db_host,
            'db_service_name': db_service_name,
            'db_port': db_port,
            'created': created,
            'encryption_flag': encryption_flag
        }

        insert_record(record)
        flash("Record has been added successfully!")
        return redirect(url_for('show_records'))

    return render_template('form.html')


@app.route('/records', methods=['GET'])
def show_records():
    records = get_records()
    # Convert the created timestamp from UTC to local time
    local_tz = pytz.timezone('America/New_York')  # Replace with the desired time zone
    for record in records:
        created_utc = datetime.fromisoformat(record['created']).replace(tzinfo=pytz.UTC)
        record['created'] = created_utc.astimezone(local_tz).strftime("%Y-%m-%d %H:%M:%S %Z%z")
    return render_template('view_records.html', records=records)


@app.route('/decrypt/<int:id>', methods=['GET'])
def decrypt(id):
    record = get_record_by_id(id)
    if record is None:
        flash("Record not found!")
        return redirect(url_for('show_records'))

    decrypted_password = decrypt_password(record['password']) if record['encryption_flag'] == 'Yes' else record['password']
    flash(f"Decrypted Password: {decrypted_password}")
    return redirect(url_for('show_records'))

@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    record = get_record_by_id(id)
    if record is None:
        flash("Record not found!")
        return redirect(url_for('show_records'))

    delete_record(id)
    flash("Record has been deleted successfully!")
    return redirect(url_for('show_records'))

if __name__ == '__main__':
    app.run(debug=True)
