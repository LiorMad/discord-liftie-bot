const { Client, Intents, SlashCommandBuilder } = require('discord.js');
const fs = require('fs');
const path = require('path');
require('dotenv').config();

const client = new Client({
  intents: [
    Intents.FLAGS.GUILDS,
    Intents.FLAGS.GUILD_MESSAGES,
    Intents.FLAGS.DIRECT_MESSAGES,
  ],
});

const liftsFile = 'lifts_status.json'; // Path to your lifts status JSON file

// Function to read the lift status from the JSON file
function getLiftStatus(resortName) {
  try {
    const data = JSON.parse(fs.readFileSync(liftsFile, 'utf8'));
    const resortData = data.find(
      (resort) => resort.resort.toLowerCase() === resortName.toLowerCase()
    );

    if (!resortData) {
      return `Resort '${resortName}' not found in the data. Please make sure the resort name is correct.`;
    }

    const liftsInfo = resortData.lifts;
    let liftStatusMsg = `**Lift status for ${resortName.charAt(0).toUpperCase() + resortName.slice(1)} Resort:**\n`;

    liftsInfo.forEach((lift) => {
      const statusEmoji = lift.status === 'Closed' ? '❌' : '';
      liftStatusMsg += `${lift.name}: ${statusEmoji} ${lift.status}\n`;
    });

    return liftStatusMsg;
  } catch (error) {
    console.error(error);
    return 'Error reading the lift status file.';
  }
}

// Function to get available resort names
function getAvailableResorts() {
  try {
    const data = JSON.parse(fs.readFileSync(liftsFile, 'utf8'));
    const resortNames = data.map((resort) => resort.resort);
    return resortNames;
  } catch (error) {
    console.error(error);
    return 'Error fetching resort names.';
  }
}

// Slash commands registration
client.once('ready', async () => {
  const guildId = 'YOUR_GUILD_ID'; // Replace with your server's Guild ID
  const guild = await client.guilds.fetch(guildId);
  const commands = guild.commands;

  // Register slash commands
  await commands.set([
    new SlashCommandBuilder()
      .setName('lifts')
      .setDescription('Get the lift status for a resort')
      .addStringOption((option) =>
        option
          .setName('resort')
          .setDescription('The name of the resort')
          .setRequired(true)
          .setAutocomplete(true)
      ),
    new SlashCommandBuilder()
      .setName('lifts_resorts')
      .setDescription('List all available resorts'),
  ]);

  console.log('Bot is online!');
});

// Auto-completion for the resort name argument
client.on('interactionCreate', async (interaction) => {
  if (!interaction.isCommand()) return;

  const { commandName, options } = interaction;

  if (commandName === 'lifts') {
    const resortName = options.getString('resort');
    const liftStatus = getLiftStatus(resortName);
    await interaction.reply(liftStatus);
  } else if (commandName === 'lifts_resorts') {
    const resorts = getAvailableResorts();
    await interaction.reply(resorts.join(', '));
  }
});

// Auto-completion logic
client.on('interactionCreate', async (interaction) => {
  if (interaction.isAutocomplete()) {
    const focusedOption = interaction.options.getFocused();
    const availableResorts = getAvailableResorts();
    const filteredResorts = availableResorts.filter((resort) =>
      resort.toLowerCase().startsWith(focusedOption.toLowerCase())
    );

    await interaction.respond(
      filteredResorts.map((resort) => ({ name: resort, value: resort }))
    );
  }
});

// Log in to Discord with your app's token
client.login(process.env.BOT_TOKEN);
