import VLoDVP
VLoDVP.setkey(b'12345678901234567890123456789012')
VLoDVP.setlink('https://yourlink.netlify.app/')

emailvar = input("Enter email: ")
licensekeyvar = input("Enter key: ")

if VLoDVP.validate(emailvar, licensekeyvar) == False:
    print("Invalid email or key")
else:
    print("Valid email and key")