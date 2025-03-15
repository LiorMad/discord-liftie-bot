import discord
import os
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
from commands.lifts_status import lifts  # Import the /lifts command

# Load environment variables
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

# Set up bot with commands
intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

# Register commands
@client.event
async def on_ready():
    """Sync commands when the bot is ready."""
    await tree.sync()
    print(f"Bot is online as {client.user}")


# Add commands to tree
tree.add_command(lifts)

# Run bot
client.run(TOKEN)
