const { Collection, Intents, Client } = require('discord.js');
const client = new Client({
  intents: [Intents.FLAGS.GUILDS, Intents.FLAGS.GUILD_MESSAGES],
  partials: ['CHANNEL', 'GUILD_MEMBER', 'MESSAGE', 'USER'],
});
const fs = require('fs');
const token = require('./config.json');

client.on('ready', async () => {
  console.log(`Bot is logged in!`);
  client.user.setStatus('online');
  // Set the bot's status. types: WATCHING, PLAYING, LISTENING, STREAMING
  client.user.setActivity('license keys', { type: 'WATCHING' });
});
fs.readdir('./events/', (err, files) => {
  if (err) return console.error(err);
  files.forEach((file) => {
    const event = require(`./events/${file}`);
    let eventName = file.split('.')[0];
    client.on(eventName, event.bind(null, client));
  });
});

client.commands = new Collection();

fs.readdir('./commands/', (err, files) => {
  if (err) return console.error(err);
  files.forEach((file) => {
    if (!file.endsWith('.js')) return;
    let props = require(`./commands/${file}`);
    let commandName = file.split('.')[0];
    client.commands.set(commandName, props);
  });
});

client.login(token.token);
