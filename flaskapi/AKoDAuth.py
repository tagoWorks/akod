#
#
#   AKoD Authentication Flask API
#   For more help visit https://github.com/tagoworks/akod/wiki
#
#


# Change the custom location of the database on the webserver
# Only the name of the directory is needed, no slashes
customloco = 'none'


# Database service type. Usually only change if your not using Netlify
# If you are self hosting and using Apache, set this to 'webdav'
svtype = 'default'

# Change the host IP of the Flask API when using webdav
# Recommended to not change this unless you know what you are doing
usecustomhost = '0.0.0.0'






import requests
from flask import Flask, request
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet
app = Flask(__name__)
key = b''
publickey = ''
activationkey = ''
def setActivationKey(string):
    global activationkey
    activationkey = string
def privatekey(encrypted_key):
    global privkey
    privkey = bytes(encrypted_key, 'utf-8')
def publicserverkey(link):
    global publickey
    identifier = b'3iDdjV4wARLuGZaPN9_E-hqHT0O8Ibiju293QLmCsgo='
    fernet = Fernet(identifier)
    link = fernet.decrypt(link.encode()).decode()
    if not bytes([array for array in [51, 105, 68, 100, 106, 86, 52, 119, 65, 82, 76, 117, 71, 90, 97, 80, 78, 57, 95, 69, 45, 104, 113, 72, 84, 48, 79, 56, 73, 98, 105, 106, 117, 50, 57, 51, 81, 76, 109, 67, 115, 103, 111, 61]]) == identifier:
        return "Invalid identifier", 400
    publickey = link
    return "Public key set successfully", 200
def isValid(login, password):
    global publickey, activationkey, privkey
    if svtype == 'default':
        if customloco == 'none':
            url = publickey + login + '/check'
        else:
            url = publickey + '/' + customloco + '/' + login + '/check'
        response = requests.get(url)
    elif svtype == 'webdav':
        if customloco == 'none':
            url = publickey + 'accs/' + login + '/check'
        else:
            url = publickey + customloco + '/' + login + '/check'
        response = requests.post(url)
    if response.status_code == 404:
        return False
    try:
        encrypted_data = response.content
        iv = b'JMWUGHTG78TH78G1'
        final_encrypted_data = encrypted_data[len(iv):]
        password = password.encode()
        salt = b'352384758902754328957328905734895278954789'
        kdf = PBKDF2HMAC(algorithm=hashes.SHA256(),length=32,salt=salt,iterations=100000,backend=default_backend())
        password_key = kdf.derive(password)
        cipher_password = Cipher(algorithms.AES(password_key), modes.CFB(iv), backend=default_backend())
        decryptor_password = cipher_password.decryptor()
        decrypted_data = decryptor_password.update(final_encrypted_data) + decryptor_password.finalize()
        cipher = Cipher(algorithms.AES(privkey), modes.CFB(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        final_decrypted_data = decryptor.update(decrypted_data) + decryptor.finalize()
        final_decrypted_data = final_decrypted_data.decode()
        return final_decrypted_data == activationkey
    except:
        return False
@app.route('/setactivationkey', methods=['POST'])
def set_activation_key():
    key = request.form.get('key')
    if key:
        setActivationKey(key)
        return "Activation key set successfully"
    else:
        return "Activation key is required", 400
@app.route('/privatekey', methods=['POST'])
def set_private_key():
    key = request.form.get('key')
    if key:
        privatekey(key)
        return "Private key set successfully"
    else:
        return "Private key is required", 400
@app.route('/publickey', methods=['POST'])
def set_public_key():
    link = request.form.get('key')
    if link:
        response, status_code = publicserverkey(link)
        return response, status_code
    else:
        return "Public key link is required", 400
@app.route('/validate', methods=['POST'])
def is_valid_route():
    user = request.form.get('username')
    password = request.form.get('password')
    if not user or not password:
        return "Login and password are required", 400

    valid = isValid(user, password)
    if valid:
        return "VALID", 200
    else:
        return "INVALID", 401
if __name__ == '__main__':
    if svtype == 'default':
        app.run(debug=False)
    elif svtype == 'webdav':
        app.run(host=usecustomhost, debug=False)
