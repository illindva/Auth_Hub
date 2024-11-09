import os
import pytz
import sqlite3
import smtplib  # For sending email notifications
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, request, redirect, url_for, flash, session
from db import init_db, insert_record, get_records, get_record_by_id, delete_record, insert_user, get_user_by_username, \
    get_users_by_role, update_approval_status, get_user_by_id
from encryption_util import encrypt_password, decrypt_password
from functools import wraps

# Load environment variables from .env file
load_dotenv()
ADMIN_EMAIL = os.getenv('ADMIN_EMAIL')
ADMIN_EMAIL_PWD = decrypt_password(os.getenv('ADMIN_EMAIL_PWD'))
app = Flask(__name__)
app.secret_key = os.getenv('APP_SECRET_KEY', '0123456789')

#Database Initialization
def setup():
    init_db()
setup()

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            flash("You need to be logged in to view this page.")
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)

    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            flash("You need to be logged in to view this page.")
            return redirect(url_for('login', next=request.url))
        user = get_user_by_username(session['username'])
        if user[5] != 'Admin':
            flash("You do not have permission to view this page.")
            return redirect(url_for('form'))
        return f(*args, **kwargs)

    return decorated_function

def send_approval_request(user):
    sender_email = ADMIN_EMAIL
    sender_password = ADMIN_EMAIL_PWD
    subject = f"Approval Required for New User: {user[1]}"
    body = f"User {user[1]} has registered and requires approval. Please log in to the admin panel to approve or deny the request."

    # Retrieve list of admin users
    admins = get_users_by_role('Admin')

    # Send email to each admin
    for admin in admins:
        receiver_email = admin[3]
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        try:
            server = smtplib.SMTP('smtp.example.com', 587)
            server.starttls()
            server.login(sender_email, sender_password)
            text = msg.as_string()
            server.sendmail(sender_email, receiver_email, text)
            server.quit()
            print(f"Approval request email sent to {receiver_email}")
        except Exception as e:
            print(f"Failed to send email: {e}")

@app.route('/home')
def home():
    return render_template('home.html')
@app.route('/')
def root():
    return redirect(url_for('home'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        email = request.form['email']
        user_type = request.form['user_type']
        user_role = request.form['user_role']

        if password != confirm_password:
            flash("Passwords do not match!")
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        approval_status = 'No' if user_role != 'Admin' else 'Yes'

        try:
            insert_user(username, hashed_password, email, user_type, user_role, approval_status)
            flash("Registration successful! Please log in.")

            if user_role != 'Admin':
                user = get_user_by_username(username)
                send_approval_request(user)
                flash("Your account is pending approval by an admin. You will be notified once approved.")

            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash("Username or email already taken!")
            return redirect(url_for('register'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = get_user_by_username(username)

        if user and check_password_hash(user[2], password):
            if user[6] == 'No':
                flash("Your account is pending approval by an admin.")
                return redirect(url_for('login'))
            session['username'] = username
            flash("Logged in successfully!")
            next_page = request.args.get('next')
            return redirect(next_page or url_for('form'))
        else:
            flash("Invalid username or password!")
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash("Logged out successfully!")
    return redirect(url_for('login'))

@app.route('/', methods=['GET', 'POST'])
@login_required
def form():
    user = get_user_by_username(session['username'])
    if user[6] == 'No':
        flash("Your account is pending approval by an admin.")
        return redirect(url_for('login'))

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
@login_required
def show_records():
    user = get_user_by_username(session['username'])
    if user[6] == 'No':
        flash("Your account is pending approval by an admin.")
        return redirect(url_for('login'))

    records = get_records()
    # Convert the created timestamp from UTC to local time
    local_tz = pytz.timezone('America/New_York')  # Replace with the desired time zone
    for record in records:
        created_utc = datetime.fromisoformat(record['created']).replace(tzinfo=pytz.UTC)
        record['created'] = created_utc.astimezone(local_tz).strftime("%Y-%m-%d %H:%M:%S %Z%z")
    return render_template('view_records.html', records=records)


@app.route('/decrypt/<int:id>', methods=['GET'])
@login_required
def decrypt(id):
    user = get_user_by_username(session['username'])
    if user[6] == 'No':
        flash("Your account is pending approval by an admin.")
        return redirect(url_for('login'))

    record = get_record_by_id(id)
    if record is None:
        flash("Record not found!")
        return redirect(url_for('show_records'))

    decrypted_password = decrypt_password(record['password']) if record['encryption_flag'] == 'Yes' else record['password']
    flash(f"Decrypted Password: {decrypted_password}")
    return redirect(url_for('show_records'))

@app.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete(id):
    user = get_user_by_username(session['username'])
    if user[6] == 'No':
        flash("Your account is pending approval by an admin.")
        return redirect(url_for('login'))

    record = get_record_by_id(id)
    if record is None:
        flash("Record not found!")
        return redirect(url_for('show_records'))

    delete_record(id)
    flash("Record has been deleted successfully!")
    return redirect(url_for('show_records'))

@app.route('/approve/<int:id>', methods=['GET', 'POST'])
@admin_required
def approve_user(id):
    user = get_user_by_id(id)
    if user is None:
        flash("User not found.")
        return redirect(url_for('approval_list'))

    if request.method == 'POST':
        approval_status = request.form['approval_status']
        update_approval_status(id, approval_status)
        flash(f"User '{user[1]}' has been {'approved' if approval_status == 'Yes' else 'disapproved'}.")
        return redirect(url_for('approval_list'))

    return render_template('approve_user.html', user=user)


if __name__ == '__main__':
    app.run(debug=True)
