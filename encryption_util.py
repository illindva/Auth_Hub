import os
from dotenv import load_dotenv
from cryptography.fernet import Fernet

# Load environment variables from .env file
load_dotenv()

# Normally, you would store this key securely
key = os.getenv('FERNET_KEY')
if key is None:
    raise ValueError("No Fernet key found in environment variables")
cipher_suite = Fernet(key)


def encrypt_password(password):
    return cipher_suite.encrypt(password.encode()).decode()


def decrypt_password(encrypted_password):
    return cipher_suite.decrypt(encrypted_password.encode()).decode()
