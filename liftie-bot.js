const { Client, GatewayIntentBits } = require('discord.js');
const fs = require('fs');
require('dotenv').config();


// Create a new client instance
const client = new Client({ intents: [GatewayIntentBits.Guilds, GatewayIntentBits.GuildMessages, GatewayIntentBits.MessageContent] });

// Path to the JSON file containing lift status data
const liftsFile = 'lifts_status.json';

// Function to read the lift status from the JSON file
function getLiftStatus(resortName) {
  try {
    const data = JSON.parse(fs.readFileSync(liftsFile, 'utf8'));

    // Find the resort from the data
    const resortData = data.find(resort => resort.resort.toLowerCase() === resortName.toLowerCase());

    if (!resortData) {
      return `Resort ${resortName} not found in the data.`;
    }

    const liftsInfo = resortData.lifts;
    let liftStatusMsg = `**Lift status for ${resortName.charAt(0).toUpperCase() + resortName.slice(1)} Resort:**\n`;

    liftsInfo.forEach(lift => {
      liftStatusMsg += `${lift.name}: ${lift.status}\n`;
    });

    return liftStatusMsg;
  } catch (error) {
    console.error(error);
    return 'Error reading the lift status file.';
  }
}

// Event when the bot is ready
client.once('ready', () => {
  console.log('Bot is online!');
});

// Event when the bot receives a message
client.on('messageCreate', (message) => {
  // Ignore messages from the bot itself
  if (message.author.bot) return;

  // Handle the !lifts <resort_name> command
  if (message.content.toLowerCase().startsWith('!lifts ')) {
    const resortName = message.content.split(' ')[1].toLowerCase(); // Extract resort name from the command
    const liftStatus = getLiftStatus(resortName);
    message.channel.send(liftStatus);
  }
});

// Log in to Discord with your app's token
client.login(process.env.BOT_TOKEN);