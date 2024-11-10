import os
from cryptography.fernet import Fernet
from dotenv import load_dotenv
from encryption_util import encrypt_password, decrypt_password

# Load environment variables from .env file
load_dotenv()
applications_list = os.getenv('APPLICATIONS', '').split(',')

print(f"applications_list: {applications_list}")
for app in applications_list:
    print(app)