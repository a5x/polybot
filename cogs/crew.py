# cogs/crew.py
import discord
from discord.ext import commands
from discord import app_commands
import aiohttp

class CrewCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="crew",
        description="Vérifie si un crew existe sur Rockstar Social Club",
    )
    @app_commands.describe(
        name="Le nom du crew Social Club (ex : kaid_gvng)"
    )
    async def crew(
        self,
        interaction: discord.Interaction,
        name: str,
    ):
        # Ack et affichage d’un loader
        await interaction.response.defer(thinking=True)

        # Normalisation du nom (minuscules, espaces → underscores)
        tag = name.lower().replace(" ", "_")
        url = f"https://socialclub.rockstargames.com/crew/{tag}/hierarchy"

        # Requête HTTP asynchrone
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status == 200:
                    html = await resp.text()
                    # Repère un message d’erreur ou de disband
                    if "This Crew has been disbanded" in html or "Not Found" in html:
                        await interaction.followup.send(
                            f"❌ Le crew `{tag}` n’existe pas ou a été dissous."
                        )
                    else:
                        await interaction.followup.send(
                            f"✅ Le crew `{tag}` existe ! → {url}"
                        )
                else:
                    await interaction.followup.send(
                        f"⚠️ Impossible de vérifier `{tag}` (HTTP {resp.status})."
                    )

async def setup(bot: commands.Bot):
    await bot.add_cog(CrewCog(bot))
