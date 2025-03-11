import discord
import json
import os
from dotenv import load_dotenv

# Load environment variables (e.g., BOT_TOKEN) from .env file
load_dotenv()

# Enable message content intent to read the content of the message
intents = discord.Intents.default()
intents.messages = True  # Ensure the bot can read messages
intents.message_content = True  # Enable reading the content of messages

# Create a new client instance with the intents enabled
client = discord.Client(intents=intents)

# Path to the JSON file containing lift status data
lifts_file = 'lifts_status.json'

# Function to read the lift status from the JSON file
def get_lift_status(resort_name):
    try:
        with open(lifts_file, 'r') as file:
            data = json.load(file)

        # Find the resort from the data
        resort_data = next((resort for resort in data if resort['resort'].lower() == resort_name.lower()), None)

        if not resort_data:
            return f"Resort '{resort_name}' not found in the data. Please make sure the resort name is correct."

        lifts_info = resort_data['lifts']
        lift_status_msg = f"**Lift status for {resort_name.capitalize()} Resort:**\n"

        # Build the lift status message
        for lift in lifts_info:
            status_emoji = "❌" if lift['status'] == 'Closed' else ""
            lift_status_msg += f"{lift['name']}: {status_emoji} {lift['status']}\n"

        return lift_status_msg
    except FileNotFoundError:
        return f"Error: The file '{lifts_file}' was not found."
    except json.JSONDecodeError:
        return f"Error: There was an issue parsing the JSON data in '{lifts_file}'."
    except Exception as e:
        print(f"Unexpected error: {e}")
        return 'An unexpected error occurred while processing the lift status file.'

# Event when the bot is ready
@client.event
async def on_ready():
    print('Bot is online!')

# Event when the bot receives a message
@client.event
async def on_message(message):
    # Ignore messages from the bot itself
    if message.author.bot:
        return

    # Handle the !lifts <resort_name> command
    if message.content.lower().startswith('!lifts '):
        resort_name = message.content.split(' ')[1].lower()  # Extract resort name from the command
        lift_status = get_lift_status(resort_name)
        await message.channel.send(lift_status)

# Log in to Discord with your app's token
def run_discord_bot():
    bot_token = os.getenv('BOT_TOKEN')
    if not bot_token:
        print("BOT_TOKEN is not set in the environment variables.")
        return
    client.run(bot_token)

# Run the bot
if __name__ == "__main__":
    run_discord_bot()
