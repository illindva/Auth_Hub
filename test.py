from cryptography.fernet import Fernet
from dotenv import load_dotenv
from encryption_util import encrypt_password, decrypt_password

# Load environment variables from .env file
load_dotenv()

password = input("Enter password to Encrypt : ")

encrypted_password = encrypt_password(password)

print(f"Encrypted Password: {encrypted_password}")