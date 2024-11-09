from cryptography.fernet import Fernet

fernet_key = Fernet.generate_key().decode()  # Generate a key and decode it to string
print(f"Insert this key in your .env file as FERNET_KEY={fernet_key}")
