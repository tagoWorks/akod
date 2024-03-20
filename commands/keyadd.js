const { SlashCommandBuilder } = require('@discordjs/builders');
const fs = require('fs');
const path = require('path');
const { ownerID } = require('../config.json');

module.exports = {
  data: new SlashCommandBuilder()
    .setName('keyadd')
    .setDescription('Add a new license key (Owner only)')
    .addStringOption(option =>
      option
        .setName('license-key')
        .setDescription('The license key to add')
        .setRequired(true)
    )
    .setDefaultPermission(false), // Hide the command by default
  async execute(interaction) {
    if (interaction.user.id !== ownerID) {
      return interaction.reply({ content: 'You are not allowed to use this command.', ephemeral: true });
    }
    const licenseKeyToAdd = interaction.options.getString('license-key');
    const licenseFilePath = path.join(__dirname, '..', 'assets', 'license.txt');
    fs.appendFile(licenseFilePath, `\n${licenseKeyToAdd}`, (err) => {
      if (err) {
        console.error('Error adding license key:', err);
        return interaction.reply({ content: 'Error adding license key. Please try again later.', ephemeral: true });
      }
      return interaction.reply({ content: `License key ${licenseKeyToAdd} added successfully.`, ephemeral: true });
    });
  },
  permissions: [
    {
      id: ownerID,
      type: 'USER',
      permission: true,
    },
  ],
};
