import requests
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

# Define your private key. Make sure its the same as the one used in assets/service.py
key = b'12345678901234567890123456789012'
# Define your Netlify webserver URL
url = 'https://repository.netlify.app/'

def decrypt(encrypted_data, key):
    iv = encrypted_data[:16]
    ciphertext = encrypted_data[16:]
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_data = decryptor.update(ciphertext) + decryptor.finalize()
    return decrypted_data
def read(url, key):
    response = requests.get(url)
    encrypted_data = response.content
    decrypted_data = decrypt(encrypted_data, key)
    return decrypted_data.decode('utf-8')
emailvar = input("Enter email: ")
keyvar = input("Enter key: ")
reqs = url + emailvar + '/check'
try:
    response = requests.get(reqs)
    if response.status_code == 404:
        print("Invalid email or key")
        exit()
    content = read(reqs, key)
except requests.exceptions.RequestException as e:
    print("Invalid Request", e)
    exit()
if not content == keyvar:
    print("Invalid email or key")
else:
    print("Valid email and key")
    # Run your main code here

