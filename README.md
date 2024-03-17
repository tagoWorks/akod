
![Banner](./header.png)

# Validating Licenses on Discord

![GitHub last commit](https://img.shields.io/github/last-commit/t-a-g-o/vlon)
![GitHub issues](https://img.shields.io/github/issues-raw/t-a-g-o/VLON)
![GitHub](https://img.shields.io/github/license/t-a-g-o/VLON)

*there is definitely an easier way to make a licensing service but idc*
The VLON bot is a user license validation tool coded in javascript and python, and uses GitHub and Netlify as licensing servers. **Completely free forever. And Encrypted.** The VLON bot allows
users to validate their license that they purchased from your site, using a simple command. I created this because I was going to make licensed code later in the future and all licensing services costed money eventually.
VLON works by creating a new directory with the validated users email and in it it creates the check file with the license code, VLON then copies this files over to your local git repo (encrypting the contents of the check file) and commits the
changes. Your GitHub repository will be hosted on Netlify in order to have the files accessable from anywhere. Then in your software code just add the decypt.py contents before the main code runs, and then obfuscate your final code in order
to hide the private key. I recommend [Hyperion](https://github.com/billythegoat356/Hyperion) as it is the most effective and hardest to decypt.


# Getting Started with VLON & Netlify 🚀

## Setup webserver
1. Create a new private GitHub repo
   
2. Add a `index.html` file with any content (just so the site can deploy)
   
3. Head to https://netlify.com/ and Login or Create an account
   
4. Create your site via GitHub

5. Wait for site to deply. You should have a link like "repositoryname.netlify.app"

## Prepare VLON
1. Clone the repo
   ```sh
   git clone https://github.com/t-a-g-o/VLON
   ```
   
2. CD into the directory
   ```sh
   cd VLON
   ```
3. Download required modules by running the provied `GetReqs.bat` file
   
4. Open the `config.json` file with notepad or another text editor, and input all the values
   * token: Your discord bot token
   * prefix: The bots prefix for commands
   * owner: The owner's user ID (will be allowed to add licenses, remove cooldowns, and delete validated accounts)
   * onlySendIn: The channel ID's where the bot will be allowed to resond
   * logChannel: The channel ID where the bot will send license validation logs
    
5. Open the `assets` folder and edit `service.py` with the required fields
   * Input your local repository path for "repo="
   * Define your static private key. This key is used to decypt and validate licenses on the user end
    
6. Input your licenses in the `license.txt` file

# Client 

Next, you have to explain how to use your project. You can create subsections under here to explain more clearly.

# License

You can also mention what license the project uses. I usually add it like this:

[MIT license](./LICENSE)
