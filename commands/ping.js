const { SlashCommandBuilder } = require('@discordjs/builders');

module.exports = {
  data: new SlashCommandBuilder()
    .setName('ping')
    .setDescription('What could this mysterious command do?'),
  async execute(interaction) {
    await interaction.reply('Pong!');
  },
};