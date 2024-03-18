![Banner](./image.png)
<div align="center">
    </a>
    <br />
    
   [tagoWorks](https://tago.works/) - [Discord](https://tago.works/discord)
   
   ![GitHub last commit](https://img.shields.io/github/last-commit/t-a-g-o/vlod)
   ![GitHub issues](https://img.shields.io/github/issues-raw/t-a-g-o/vlod)
   ![GitHub](https://img.shields.io/github/license/t-a-g-o/vlod)

   *there is definitely an easier way to make a licensing service but idc*
   
   Validating Licenses on Discord bot is a user license validation tool coded in javascript and python, and uses GitHub and Netlify as licensing servers. **Completely free forever. And Encrypted.** The VLoD bot allows
   users to validate their license that they purchased from your site, using a simple command. I created this because I was going to make licensed code later in the future and all licensing services costed money eventually.
   VLoD works by creating a new directory with the validated users email and in it it creates the check file with the license code, VLoD then copies this files over to your local git repo (encrypting the contents of the check file) and commits the
   changes. Your GitHub repository will be hosted on Netlify in order to have the files accessable from anywhere. Then in your software code just add the decypt.py contents before the main code runs, and then obfuscate your final code in order
   to hide the private key. I recommend [Hyperion](https://github.com/billythegoat356/Hyperion) as it is the most effective and hardest to decypt. VLoD is open source and I encourge you to make your own changes!

</div>


# Getting Started with VLoD & Netlify 🚀

## Setup webserver
1. Create a new private GitHub repo
   
2. Add a `index.html` file with any content (just so the site can deploy)
   
3. Head to https://netlify.com/ and Login or Create an account
   
4. Create your site via GitHub

5. Wait for site to deploy. You should have a link like "repositoryname.netlify.app"

## Prepare VLoD
1. Clone the repo
   ```sh
   git clone https://github.com/t-a-g-o/VLoD
   ```
   
2. CD into the directory
   ```sh
   cd VLoD
   ```
3. Download required modules by running the provied `GetReqs.bat` file
   
4. Open the `config.json` file with notepad or another text editor, and input all the values
   * token: Your discord bot token
   * prefix: The bots prefix for commands
   * owner: The owner's user ID (will be allowed to add licenses, remove cooldowns, and delete validated accounts)
   * onlySendIn: The channel ID's where the bot will be allowed to resond
   * logChannel: The channel ID where the bot will send license validation logs
    
5. Open the `assets` folder and edit `service.py` with the required fields
   * Fill in the fields for username, repo name, and personal access token
   * Generate or type your private read key and save it for later

6. Input your licenses in the `license.txt` file

# Implement VLoD in your code 💻
For now VLoD can only be used for Python scripts. If you want to contribute and attempt to expand please feel free.
1. Import the Validating Licenses on Discord Validating Packing package
   ```sh
   import VLoDVP
   ```
2. Define your private key and your new netlify webserver
   ```sh
   VLoDVP.setkey('12345678901234567890123456789012')
   VLoDVP.setlink('https://yourlink.netlify.app/')
   ```
3. Code a way for the user to input their email and license
   *email var and licensekeyvar can be named anything*
   ```sh
   emailvar = input("Enter email: ")
   licensekeyvar = input("Enter key: ")
   ```
4. Check if the account exists and the license is active
   ```sh
   if VLoDVP.validate(emailvar, licensekeyvar) == False:
      print("Invalid email or key")
   else:
      # Run your main code here
   ```
If your having issues check out the example.py or join the [discord server](https://tago.works/discord)
# Discord Bot Usage 🤖
## Member usage
Users in your Discord server can validate their licenses by running the command "!license validate LICENSEKEY EMAIL" where the ! is your set prefix in the `config.js` file.
Any member of you discord server by default will be set to a 30 day cooldown in order to prevent any type of license fruad. To change this cooldown you can edit the "'const remainingTime = Math.ceil((30 * 24 * 60 * 60 * 1000 - (Date.now() - lastUsage)) / (1000 * 60 * 60 * 24));" line in `commands/license.js` to a set amount of milliseconds.

## Owner usage
As the owner, you can remove users cooldowns, add license keys, and deactive emails that are registered to a license key
*the following examples uses the prefix ! but you set your custom prefix in `config.js`*
* !license removecooldown USERID
* !license remove EMAILREGISTERED
* !license keyadd LICENSEKEY

**Note:**
To remove added license keys, or to add license keys in bulk you need to manually edit the `assets/license.txt` file, making sure that the last license key ends with pressing the ENTER key to go down a line.

# Roadmap 🛣️
- [x] Create decypt.py
- [x] Rename project (Nova -> VLoD)
- [ ] Expand on languages to license
- [ ] Auto save login in decypt.py
- [ ] Add checks for invalid emails
- [ ] Add catches for when an invalid folder is created

# License & Information 📃
This project is published under the [MIT license](./LICENSE)

If you are interested in working together, or want to get in contact with me please email me at santiagobuisnessmail@gmail.com
