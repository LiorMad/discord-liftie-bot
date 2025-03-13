import discord
from discord import app_commands
from utils.data_loader import load_resorts

# Load resort data
resorts_data = load_resorts()
ALL_RESORTS = [resort["resort"] for resort in resorts_data]  # Extract resort names


async def resort_autocomplete(interaction: discord.Interaction, current: str):
    """Autocomplete function for resort names (limited to 25 options)."""
    return [
        app_commands.Choice(name=resort, value=resort)
        for resort in ALL_RESORTS if current.lower() in resort.lower()
    ][:25]  # Discord allows a max of 25 choices


@app_commands.command(name="lifts", description="Get lift status for a resort")
@app_commands.autocomplete(resort=resort_autocomplete)
async def lifts(interaction: discord.Interaction, resort: str):
    """Handles the /lifts command to return lift status for a given resort."""
    resort_data = next((r for r in resorts_data if r["resort"].lower() == resort.lower()), None)

    if not resort_data:
        await interaction.response.send_message(f"Resort '{resort}' not found.", ephemeral=True)
        return

    lifts_info = resort_data["lifts"]
    response = f"**Lift status for {resort}:**\n" + "\n".join(
        f"{lift['name']}: {'✅' if lift['status'].lower() == 'open' else '❌'} {lift['status']}"
        for lift in lifts_info
    )

    await interaction.response.send_message(response)
