import VLoDVP
VLoDVP.setkey(b'12345678901234567890123456789012')
VLoDVP.setlink('https://yourlink.netlify.app/')

uservar = input("Enter username: ")
licensekeyvar = input("Enter key: ")

if VLoDVP.validate(uservar, licensekeyvar) == False:
    print("Invalid username or key")
else:
    print("Valid username and key")