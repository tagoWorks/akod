const { SlashCommandBuilder } = require('@discordjs/builders');
const fs = require('fs');
const path = require('path');
const { ownerID, guildID } = require('../config.json');

module.exports = {
  data: new SlashCommandBuilder()
    .setName('remove')
    .setDescription('Remove a registered account (Owner only)')
    .addStringOption(option =>
      option
        .setName('account-name')
        .setDescription('The account name to remove')
        .setRequired(true)
    ),
  
  async execute(interaction) {
    const { ownerID } = require('../config.json');
    const { guildID } = require('../config.json');
    if (!ownerID) {
      return interaction.reply({ content: 'Owner information not found in config.', ephemeral: true });
    }
    if (interaction.user.id !== ownerID) {
      return interaction.reply({ content: 'You do not have permission to use this command.', ephemeral: true });
    }
    const accToRemove = interaction.options.getString('account-name');
    const assetsFolderPath = path.join(__dirname, '..', 'assets', 'registered');
    const accFolder = path.join(assetsFolderPath, accToRemove);
    fs.rmdir(accFolder, { recursive: true }, (err) => {
      if (err) {
        console.error('Error removing account folder:', err);
        return interaction.reply({ content: 'Error removing account folder. Please try again later.', ephemeral: true });
      }
      return interaction.reply({ content: `License removed successfully for ${accToRemove}.`, ephemeral: true });
    });
  },
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