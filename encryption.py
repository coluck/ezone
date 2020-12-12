
from cryptography.fernet import Fernet


# Function which generates our key (AES)
def keyGen():
    key = Fernet.generate_key()
    with open("key.enc", "wb") as f:
        f.write(key)


# Function which reads the key
def keyRead():
    try:
        file = open('key.enc', 'rb')
        key = file.read()
        file.close()
        return key
    except FileNotFoundError:
        # If key does not exists a new one is created.
        print("No Key exists, a new one has just been created.")
        keyGen()
        keyRead()


#Function to encrypt files using the key
def encrypt(fileName, Key):
    with open("Files/" + fileName, "rb") as f:
        data = f.read()
    fernet = Fernet(Key)
    encrypted = fernet.encrypt(data)
    with open("EncFiles/" + fileName, "wb") as f:
        f.write(encrypted)


# Function to decrypt files using the key
def decrypt(fileName, Key):
    with open("Downloads/" + fileName, "rb") as f:
        data = f.read()
    fernet = Fernet(Key)
    decrypted = fernet.decrypt(data)
    with open("Downloads/" + fileName, "wb") as f:
        f.write(decrypted)