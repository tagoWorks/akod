import AKoDAuth as auth
auth.privatekey('private key from identifier.txt')
auth.publicserverkey('public key from identifier.txt')

usernamevar = input("Enter username: ")
activationkeyvar = input("Enter key: ")

if auth.isValid(usernamevar, activationkeyvar) == False:
    print("Invalid username or key")
    exit
else:
    print("Valid username and key")