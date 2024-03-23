const { SlashCommandBuilder } = require('@discordjs/builders');
const fs = require('fs');
const path = require('path');
const { ownerID, guildID } = require('../config.json');

module.exports = {
  data: new SlashCommandBuilder()
    .setName('keyadd')
    .setDescription('Add a new key (Owner only)')
    .addStringOption(option =>
      option
        .setName('key')
        .setDescription('The activation key to add')
        .setRequired(true)
    ),
  async execute(interaction) {
    if (interaction.user.id !== ownerID) {
      return interaction.reply({ content: 'You are not allowed to use this command.', ephemeral: true });
    }
    const licenseKeyToAdd = interaction.options.getString('key');
    const licenseFilePath = path.join(__dirname, '..', 'assets', 'validkeys.txt');
    fs.readFile(licenseFilePath, 'utf8', (err, data) => {
      if (err) {
        console.error('Error reading key file:', err);
        return interaction.reply({ content: 'Error adding key. Please try again later.', ephemeral: true });
      }
      const existingKeys = data.trim().split('\n');
      if (existingKeys.includes(licenseKeyToAdd)) {
        return interaction.reply({ content: 'This key already exists.', ephemeral: true });
      }
      fs.appendFile(licenseFilePath, `\n${licenseKeyToAdd}`, (err) => {
        if (err) {
          console.error('Error adding key:', err);
          return interaction.reply({ content: 'Error adding key. Please try again later.', ephemeral: true });
        }
        return interaction.reply({ content: `Activation key ${licenseKeyToAdd} added successfully.`, ephemeral: true });
      });
    });
  },
  defaultPermission: false,
  permissions: [
    {
      id: guildID,
      type: 'ROLE',
      permission: false,
    },
    {
      id: ownerID,
      type: 'USER',
      permission: true,
    },
  ],
};