![Banner](https://media.discordapp.net/attachments/1092315227057561630/1221138931916214422/akodheader.png?ex=662d2cc1&is=661ab7c1&hm=bb787a7cb77e43e5258d9d82ac9526a261da7fd24265c8a79ca57f7f489c5e8c&=&format=webp&quality=lossless&width=1440&height=242)
<div align="center">
    </a>
    <br />

   ![GitHub last commit](https://img.shields.io/github/last-commit/tagoworks/akod)
   ![GitHub issues](https://img.shields.io/github/issues-raw/tagoworks/akod)
   ![GitHub](https://img.shields.io/github/license/tagoworks/akod)
   
![Example](https://media.discordapp.net/attachments/1092315227057561630/1229117980449837098/Group_2.png?ex=662e8452&is=661c0f52&hm=0f28751f0b32612ed588d1a6463aab57f29f58fc1bc0dd0205b9ac63afdfc967&=&format=webp&quality=lossless)

</div>

> Activating Keys on Discord is a free and multi-layered encrypted user key authentication tool for your code. Built with JavaScript and Python, it utilizes GitHub and Netlify as licensing servers. AKoD allows your users to validate their purchased activation keys from your site using a simple Discord bot command. It creates a directory with the validated account name, generates an encrypted key file, and commits the changes to a GitHub repository hosted on Netlify for accessibility. To integrate AKoD into your software, create a free flask api, and obfuscate your final code using a tool like Hyperion to hide the private key. AKoD is open-source, and you're encouraged to make your own modifications to suit your needs.


# Get Started with AKoD 🚀
For better detailed intructions visit the revisioned [wiki page](https://github.com/tagoworks/akod/wiki/getting-started)
or watch the [YouTube video!](https://youtu.be/Wtpl7a_08jE)


## Setup webserver
1. Create a new private GitHub repo
   
2. Add a `index.html` file with any content (just so the site can deploy)
   
3. Head to https://app.netlify.com/ and Login or Create an account
   
4. Create your site via GitHub

5. Wait for site to deploy. You should have a link like "repositoryname.netlify.app"

## Prepare AKoD
1. Create a new folder & clone the repo
   ```sh
   git clone https://github.com/tagoworks/akod
   ```
   
2. Open the new `akod` folder
   
4. Download required modules by running the provided `GetReqs.bat` file
   
5. Open the `config.json` file with notepad or another text editor, and input all the values
   * token: Your discord bot token
   * ownerID: The owner's user ID (will be allowed to add custom keys, remove cooldowns, and delete validated accounts)
   * guildID: The server ID which the bot will be in (for permission sets)
   * onlySendIn: The channel ID's where the bot will be allowed to respond
   * logChannel: The channel ID where the bot will send key activation logs
   * GITUSERNAME: Your GitHub account username
   * GITSTORAGEREPO: The repository where the accounts and active accounts/keys will be stored
   * GITPAT: Your GitHub personal access token (PAT), which is used to push the new accounts to the webserver repository (give repo scopes)
   * netlifyURL: Your Netlify repo link (https://repository.netlify.app/)
6. Open the `assets` directory and run the `StartWatching.bat` file in order to generate your `identifiers.txt` file
   * It is very important to save these keys, if you publish your projects and use this key and later on change it you will not be able to validate any keys
   * After a few minutes check your Netlify link and verify AKoD can read and write
7. Input your custom keys in the `validkeys.txt` file
   * Remember to make a new line for each new activation key
8. Modify the `blacklist.txt` file to add any additional blocked usernames, like your username or other developers.

# Setting up your own free API 🛜

1. Go to [pythonanywhere.com](https://pythonanywhere.com/) and create a free account to host the auth api
2. Create a new web app
   * Select "Flask" web framework
   * Select "Python 3.10"
5. Rename the py file to something like "auth"
6. Create the webapp
7. Scroll down until you see "Source code", and click "Go to directory"
8. Click on the 'auth.py' file you created
9. Copy the contents of the the python file in the "flaskapi" folder, and paste it into the file for pythonanywhere
10. Save the changes on the top right
11. Reload your webapp

# Implement AKoDAuth into your code 💻
View the 'example.py' file to see how to set all the needed variables to your api and check for a valid login!

1. Set and post your private and public key
   ```py
   private_key = "private key from identifiers.txt"
   publicserverkey = "public key from identifiers.txt"
   requests.post('http://yourusername.pythonanywhere.com/privatekey', data={'privatekey': private_key})
   requests.post('http://yourusername.pythonanywhere.com/publickey', data={'link': publicserverkey})
   ```
2. Create a way to input activation key, username, and login
   ```py
   activationkey =input ("Enter activation key: ")
   username = input("Enter username: ")
   password = input("Enter password: ")
3. Creata a post request to your API to check for the account credentials
   ```py
   requests.post('http://yourusername.pythonanywhere.com/setactivationkey', data={'key': activationkey})
   response = requests.post('http://yourusername.pythonanywhere.com/validate', data={'username': username, 'password': password})
   ```
4. If the response is "VALID", start your code!
   ```py
   if response.text == "VALID":
     print("Hello, World!")
    ```

If your still having issues join the [discord server](https://tago.works/discord)!

# Discord Bot Usage 🤖

## Member usage
Users in your Discord server can validate their keys by running the command "/validate ACTIVATION-KEY LOGIN PASSWORD".
Any member of you discord server by default will be set to a 30 day cooldown in order to prevent any type of fraud. To change this cooldown you can edit the "'const remainingTime = Math.ceil((30 * 24 * 60 * 60 * 1000 - (Date.now() - lastUsage)) / (1000 * 60 * 60 * 24));" line in `commands/validate.js` to a set amount of milliseconds.

## Owner usage
As the owner, you can remove users cooldowns, add keys, and REMOVE accounts that are registered to a key
* /removecooldown USERID
* /remove ACCOUNT-NAME
* /keyadd KEY

**Note:**
To remove added keys, or to add keys in bulk you need to manually edit the `assets/validkeys.txt` file, making sure that the last key ends with pressing the ENTER key to go down a line.

# Roadmap 🛣️
- [x] Rename project (VLoD -> AKoD)
- [x] Convert bot commands to discord slash applications
- [x] Add checks for invalid account names
- [x] Add catches for when an invalid folder is created
- [x] Add public key functionality
- [X] Add password function
- [X] Add custom API
- [ ] Expand on languages to use AKoDAuth
- [ ] Add expiring method

# License & Information 📃
This project is published under the [MIT license](./LICENSE)

If you are interested in working together, or want to get in contact with me please email me at santiagobuisnessmail@gmail.com
