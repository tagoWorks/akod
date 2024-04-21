import requests
import os

private_key = "private key from identifiers.txt"
publicserverkey = "public key from identifiers.txt"
requests.post('http://yourusername.pythonanywhere.com/privatekey', data={'privatekey': private_key})
requests.post('http://yourusername.pythonanywhere.com/publickey', data={'link': publicserverkey})


if os.path.exists('licensekey.txt'):
    with open ('licensekey.txt', 'r') as f:
        activationkey = f.read()
        f.close()
else:
    activationkey = input("Enter activation key: ")
    with open ('licensekey.txt', 'w') as f:
        f.write(activationkey)
        f.close()

username = input("Enter username: ")
password = input("Enter password: ")
requests.post('http://yourusername.pythonanywhere.com/setactivationkey', data={'key': activationkey})
response = requests.post('http://yourusername.pythonanywhere.com/validate', data={'username': username, 'password': password})

if response.text == "VALID":
    print("Hello, World!")