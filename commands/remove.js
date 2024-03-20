const { SlashCommandBuilder } = require('@discordjs/builders');
const fs = require('fs');
const path = require('path');

// Path to config.json file in the parent directory
const configPath = path.resolve(__dirname, '..', 'config.json');
const { ownerID } = require(configPath);

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
    if (!ownerID) {
      return interaction.reply({ content: 'Owner information not found in config.', ephemeral: true });
    }
    // Only the owner can use this subcommand
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
  }
};
