const { SlashCommandBuilder } = require('@discordjs/builders');
const fs = require('fs');
const path = require('path');
const { cooldowns } = require('../events/shared.js');

module.exports = {
  data: new SlashCommandBuilder()
    .setName('validate')
    .setDescription('Validate your purchased key!')
    .addStringOption(option =>
      option
        .setName('activation-key')
        .setDescription('Your purchased key')
        .setRequired(true)
    )
    .addStringOption(option =>
      option
        .setName('account-name')
        .setDescription('Create an account name login')
        .setRequired(true)
    ),
  async execute(interaction) {
    const licenseKey = interaction.options.getString('activation-key');
    const accname = interaction.options.getString('account-name');
    const userId = interaction.user.id;
    const lastUsage = cooldowns[userId];
    // User cooldown: 30 days, always in milliseconds
    if (lastUsage && cooldowns[userId] - lastUsage < 30 * 24 * 60 * 60 * 1000) {
      const remainingTime = Math.ceil((30 * 24 * 60 * 60 * 1000 - (Date.now() - lastUsage)) / (1000 * 60 * 60 * 24));
      await interaction.reply({
        content: `To prevent any type of key stealing, or spamming there is a implemented cooldown. Please contact staff for more help.`,
        ephemeral: true,
      });
      return;
    }
    cooldowns[userId] = Date.now();
    if (!/^[a-zA-Z0-9]+$/.test(accname) || /\s/.test(accname)) {
      await interaction.reply({
        content: `Invalid account name. Account name should only contain letters and numbers and should not contain any spaces.`,
        ephemeral: true,
      });
      delete cooldowns[userId];
      return;
    }

    // Path to the assets folder from the root
    const assetsFolderPath = path.join(__dirname, '..', 'assets');

    // Path to all valid licenses text file in the assets folder
    const licenseFilePath = path.join(assetsFolderPath, 'validkeys.txt');

    fs.readFile(licenseFilePath, 'utf8', (err, data) => {
      if (err) {
        console.error('Error reading key file:', err);
        return interaction.reply({ content: 'Error reading key file. Please try again later.', ephemeral: true });
      }
      let licenses = data.split('\n');
      const index = licenses.findIndex(key => key.trim() === licenseKey);
      if (index !== -1) {
        const accFolder = path.join(assetsFolderPath, 'registered', accname);
        fs.access(accFolder, fs.constants.F_OK, async (err) => {
          if (!err) {
            await interaction.reply({
              content: `Sorry but "${accname}" is in use. Please rerun the validate command with a different account name.`,
              ephemeral: true,
            });
            delete cooldowns[userId];
            return;
          }
          licenses.splice(index, 1);
          fs.writeFile(licenseFilePath, licenses.join('\n'), async (err) => {
            if (err) {
              console.error('Error updating license file:', err);
              return interaction.reply({ content: 'Error updating key file. Please try again later.', ephemeral: true });
            }
            fs.mkdir(accFolder, { recursive: true }, (err) => {
              if (err) {
                console.error('Error creating account folder:', err);
                return interaction.reply({ content: 'Error creating account folder. Please try again later.', ephemeral: true });
              }
              const checkFilePath = path.join(accFolder, 'check');
              fs.writeFile(checkFilePath, licenseKey, (err) => {
                if (err) {
                  console.error('Error writing to check file:', err);
                  return interaction.reply({ content: 'Error writing to check file. Please try again later.', ephemeral: true });
                }
                const remainingLicenses = licenses.length;
                let config = require('../config.json');
                const logChannelId = config.logChannel;
                const targetChannel = interaction.client.channels.cache.get(logChannelId);
                if (targetChannel) {
                  targetChannel.send(`Activation key: ${licenseKey}\nUsername: ${accname}\nTime Activated: ${new Date().toLocaleString()}\nVALID KEYS LEFT: ${remainingLicenses}`);
                } else {
                  console.error('Error: Target channel not found.');
                }
                interaction.reply({ content: `Your key was successfully activated with your username! Please wait about 15-20 seconds for the servers to update before use.`, ephemeral: true });
              });
            });
          });
        });
      } else {
        interaction.reply({ content: 'Invalid key. Please try again later.', ephemeral: true });
      }
    });
  }
};