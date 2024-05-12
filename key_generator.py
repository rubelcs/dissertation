# key_generator.py

import os
from cryptography.fernet import Fernet

def generate_key():
    # Check if the key file already exists
    if not os.path.exists("encryption_key.txt"):
        # If not, generate a new key and store it
        key = Fernet.generate_key()
        with open("encryption_key.txt", "wb") as key_file:
            key_file.write(key)
    else:
        print("Key already exists.")

if __name__ == "__main__":
    generate_key()
