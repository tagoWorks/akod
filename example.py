import AKoDAuth as auth
import os
auth.privatekey('private key from identifiers.txt')
auth.publicserverkey('public key from identifiers.txt')

if os.path.exists('licensekey.txt'):
    with open ('licensekey.txt', 'r') as f:
        auth.setActivationKey(f.read())
        f.close()
else:
    activationkey = input("Enter activation key: ")
    auth.setActivationKey(activationkey)
    with open ('licensekey.txt', 'w') as f:
        f.write(activationkey)
        f.close()

username = input("Enter username: ")
password = input("Enter password: ")

if auth.isValid(username, password) == False:
    print("Invalid login credentials.")
    exit
else:
    print("Hello World!")