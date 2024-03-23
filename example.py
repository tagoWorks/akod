import AKoDAuth as auth
auth.privatekey('private key from identifier.txt')
auth.publicserverkey('public key from identifier.txt')

uservar = input("Enter username: ")
licensekeyvar = input("Enter key: ")

if auth.isValid(uservar, licensekeyvar) == False:
    print("Invalid username or key")
else:
    print("Valid username and key")