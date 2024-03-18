const Jsonfile = require('../config.json');
const fs = require('fs');
const path = require('path');
const cooldowns = {};

exports.run = async (client, message, args) => {
    let config = require('../config.json');
    const allowedChannels = config.onlySendIn;
    if (!allowedChannels.includes(message.channel.id)) {
        const errorMessage = await message.channel.send('This command is not allowed in this channel.');
        setTimeout(() => {
            errorMessage.delete().catch(err => console.error('Error deleting message:', err));
            message.delete().catch(err => console.error('Error deleting message:', err));
        }, 3000);
        return;
    }

    if (args.length < 1) {
        message.delete().catch(err => console.error('Error deleting message:', err));
        const sentMessage = await message.channel.send('To use this command correctly, do `=license validate YOUR-LICENSE-KEY youremail@youremail.com`');
        setTimeout(() => {
            sentMessage.delete().catch(err => console.error('Error deleting message:', err));
        }, 3000);
        return;
    }

    const action = args[0].toLowerCase();

    if (action === 'validate') {
        if (args.length < 1) {
            message.delete().catch(err => console.error('Error deleting message:', err));
            const prefix = Jsonfile.prefix;
            const sentMessage = await message.channel.send(`To use this command correctly, do \`${prefix}license validate YOUR-LICENSE-KEY youremail@youremail.com\``);
            setTimeout(() => {
                sentMessage.delete().catch(err => console.error('Error deleting message:', err));
            }, 3000);
            return;
        }
    
        const licenseKey = args[1];
        const email = args[2];
        const userId = message.author.id;

        const lastUsage = cooldowns[userId];
        // User cooldown: 30 days, always in milliseconds
        if (lastUsage && Date.now() - lastUsage < 30 * 24 * 60 * 60 * 1000) {
            const remainingTime = Math.ceil((30 * 24 * 60 * 60 * 1000 - (Date.now() - lastUsage)) / (1000 * 60 * 60 * 24));
            message.delete().catch(err => console.error('Error deleting message:', err));
            const cooldownMessage = await message.channel.send(`To prevent any type of license key stealing, or spamming there is a implemented cooldown of 30 days. If you mistyped something or made some type of mistake previously please create a ticket in <#1092456996172742788> for support.`);
            setTimeout(() => {
                cooldownMessage.delete().catch(err => console.error('Error deleting message:', err));
            }, 3000);
            return;
        }

        cooldowns[userId] = Date.now();

        // Path to the assets folder from the root
        const assetsFolderPath = path.join(__dirname, '..', 'assets');

        // Path to all valid licenses text file in the assets folder
        const licenseFilePath = path.join(assetsFolderPath, 'license.txt');

        fs.readFile(licenseFilePath, 'utf8', (err, data) => {
            if (err) {
                console.error('Error reading license file:', err);
                return message.channel.send('Error reading license file. Please try again later.');
            }

            let licenses = data.split('\n');

            const index = licenses.findIndex(key => key.trim() === licenseKey);
            if (index !== -1) {
                licenses.splice(index, 1);
                fs.writeFile(licenseFilePath, licenses.join('\n'), async (err) => {
                    if (err) {
                        console.error('Error updating license file:', err);
                        return message.channel.send('Error updating license file. Please try again later.');
                    }
                    const emailFolder = path.join(assetsFolderPath, 'registered', email); 
                    fs.mkdir(emailFolder, { recursive: true }, (err) => {
                        if (err) {
                            console.error('Error creating email folder:', err);
                            return message.channel.send('Error creating email folder. Please try again later.');
                        }
                        const checkFilePath = path.join(emailFolder, 'check');
                        fs.writeFile(checkFilePath, licenseKey, (err) => {
                            if (err) {
                                console.error('Error writing to check file:', err);
                                return message.channel.send('Error writing to check file. Please try again later.');
                            }

                            const remainingLicenses = licenses.length;
                            let config = require('../config.json');
                            const logChannelId = config.logChannel;
                            const targetChannel = client.channels.cache.get(logChannelId);                            
                            if (targetChannel) {
                                targetChannel.send(`License key: ${licenseKey}\nEmail: ${email}\nTime Activated: ${new Date().toLocaleString()}\nLICENSE KEYS LEFT: ${remainingLicenses}`);
                            } else {
                                console.error('Error: Target channel not found.');
                            }

                            message.channel.send(`<@${userId}> Your license was successfully validated! Please wait about 15-20 seconds for the servers to update before use.`)
                                .then(userMessage => {
                                    message.delete().catch(err => console.error('Error deleting message:', err));
                                })
                                .catch(error => {
                                    console.error('Error sending user message:', error);
                                });
                        });
                    });
                });
            } else {
              message.delete().catch(err => console.error('Error deleting message:', err));
              message.channel.send('Invalid license key.')
                  .then(invalidLicenseMessage => {
                      setTimeout(() => {
                          invalidLicenseMessage.delete().catch(err => console.error('Error deleting message:', err));
                      }, 3000);
                  })
                  .catch(error => {
                      console.error('Error sending invalid license message:', error);
                  });
              return;
          }
        });
      } else if (action === 'remove') {
        // Only the owner can use this subcommand
        if (message.author.id !== Jsonfile.owner) {
            message.delete().catch(err => console.error('Error deleting message:', err));
            return;
        }
    
        if (args.length < 2) {
            return message.channel.send('Please provide an email address to remove the license.');
        }
    
        const emailToRemove = args[1];
    
        // Path to the assets folder from the root
        const assetsFolderPath = path.join(__dirname, '..', 'assets', 'registered');
        const emailFolder = path.join(assetsFolderPath, emailToRemove);
    
        fs.rmdir(emailFolder, { recursive: true }, (err) => {
            if (err) {
                console.error('Error removing email folder:', err);
                return message.channel.send('Error removing email folder. Please try again later.');
            }
    
            return message.channel.send(`License removed successfully for email ${emailToRemove}.`);
        });
    }
     else if (action === 'removecooldown') {
        // Only the owner can use this subcommand
        if (message.author.id !== Jsonfile.owner) {
		message.delete().catch(err => console.error('Error deleting message:', err));
		return;
    }

    if (args.length < 2) {
      return message.channel.send('Please provide a user ID to remove cooldown.');
    }

    const targetUserId = args[1];
    if (!cooldowns[targetUserId]) {
      return message.channel.send('There is no cooldown set for the provided user ID.');
    }

    delete cooldowns[targetUserId];

    return message.channel.send(`Cooldown removed successfully for user ID ${targetUserId}.`);
  } else if (action === 'keyadd') {
    // Only the owner can use this subcommand
    if (message.author.id !== Jsonfile.owner) {
		message.delete().catch(err => console.error('Error deleting message:', err));
		return;
    }

    if (args.length < 2) {
      return message.channel.send('Please provide a license key to add.');
    }

    const licenseKeyToAdd = args[1];
    const licenseFilePath = path.join(__dirname, '..', 'assets', 'license.txt');

    fs.appendFile(licenseFilePath, `\n${licenseKeyToAdd}`, (err) => {
      if (err) {
        console.error('Error adding license key:', err);
        return message.channel.send('Error adding license key. Please try again later.');
      }

      return message.channel.send(`License key ${licenseKeyToAdd} added successfully.`);
    });
  } else {
    message.delete().catch(err => console.error('Error deleting message:', err));
    return;
  }
};
