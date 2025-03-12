import discord
import json
import os
from discord import app_commands
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

# Load resorts from JSON
lifts_file = 'lifts_status.json'
with open(lifts_file, 'r') as file:
    resorts_data = json.load(file)
ALL_RESORTS = [resort['resort'] for resort in resorts_data]  # Extract resort names

# Set up bot with commands
intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


# Auto-complete function (filters resorts dynamically)
async def resort_autocomplete(interaction: discord.Interaction, current: str):
    return [
               app_commands.Choice(name=resort, value=resort)
               for resort in ALL_RESORTS if current.lower() in resort.lower()
           ][:25]  # Limit to 25 options


# Slash command for lift status
@tree.command(name="lifts", description="Get lift status for a resort")
@app_commands.autocomplete(resort=resort_autocomplete)
async def lifts(interaction: discord.Interaction, resort: str):
    resort_data = next((r for r in resorts_data if r['resort'].lower() == resort.lower()), None)

    if not resort_data:
        await interaction.response.send_message(f"Resort '{resort}' not found.", ephemeral=True)
        return

    lifts_info = resort_data['lifts']
    response = f"**Lift status for {resort}:**\n" + "\n".join(
        f"{lift['name']}: {'✅' if lift['status'].lower() == 'open' else '❌'} {lift['status']}"
        for lift in lifts_info
    )

    await interaction.response.send_message(response)


# Event when bot is ready
@client.event
async def on_ready():
    await tree.sync()
    print(f"Bot is online as {client.user}")


# Run bot
client.run(TOKEN)
