# src/cogs/scid.py
import discord
from discord.ext import commands
from discord import app_commands
import aiohttp
from bs4 import BeautifulSoup

class SocialClub(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="scid", description="Afficher le Rockstar Social Club ID (SCID) d’un joueur")
    @app_commands.describe(pseudo="Nom du profil Social Club du joueur")
    async def scid(self, interaction: discord.Interaction, pseudo: str):
        await interaction.response.defer()
        url = f"https://socialclub.rockstargames.com/member/{pseudo}/games"
        headers = {
            "User-Agent": "Mozilla/5.0 (DiscordBot)"
        }

        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(url) as resp:
                if resp.status == 404:
                    return await interaction.followup.send(f"❌ Profil **{pseudo}** introuvable.")
                html = await resp.text()

        # Parse HTML
        soup = BeautifulSoup(html, "html.parser")

        # Essai via meta tag
        scid = None
        meta = soup.find("meta", {"name": "scid"})
        if meta and meta.has_attr("content"):
            scid = meta["content"]

        # Sinon, recherche dans les <script>
        if not scid:
            for script in soup.find_all("script"):
                text = script.string
                if text and "scid" in text:
                    import re
                    m = re.search(r"""['"]scid['"]\s*[:=]\s*['"]?(\d+)['"]?""", text)
                    if m:
                        scid = m.group(1)
                        break

        if not scid:
            return await interaction.followup.send(
                f"❌ Impossible de trouver le SCID pour **{pseudo}**. Vérifiez que le profil est public."
            )

        # Construction de l’embed
        embed = discord.Embed(
            title=pseudo,
            url=url,
            description=f"**Rockstar SCID** : `{scid}`",
            color=discord.Color.red()
        )
        embed.set_footer(text="Données récupérées depuis Social Club")

        await interaction.followup.send(embed=embed)

async def setup(bot):
    await bot.add_cog(SocialClub(bot))
