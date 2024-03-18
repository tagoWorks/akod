import requests
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
key = b''
netlify_app_link = ''
def setkey(encrypted_key):
    global key
    key = encrypted_key
def setlink(link):
    global netlify_app_link
    netlify_app_link = link
def decrypt(encrypted_data):
    iv = encrypted_data[:16]
    ciphertext = encrypted_data[16:]
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_data = decryptor.update(ciphertext) + decryptor.finalize()
    return decrypted_data
def read(url):
    response = requests.get(url)
    encrypted_data = response.content
    decrypted_data = decrypt(encrypted_data)
    return decrypted_data.decode('utf-8')
def validate(email, license):
    global netlify_app_link
    url = netlify_app_link + email + '/check'
    try:
        response = requests.get(url)
        if response.status_code == 404:
            return False
        content = read(url)
    except requests.exceptions.RequestException as e:
        print("VLoDVP Request Error", e)
        return False
    return content == license