import VLoDVP
VLoDVP.privatekey('private key from identifier.txt')
VLoDVP.publicserverkey('public key from identifier.txt')

uservar = input("Enter username: ")
licensekeyvar = input("Enter key: ")

if VLoDVP.isValid(uservar, licensekeyvar) == False:
    print("Invalid username or key")
else:
    print("Valid username and key")