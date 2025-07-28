# src/cogs/scid.py
import discord
from discord.ext import commands
from discord import app_commands
import aiohttp
from bs4 import BeautifulSoup
import re

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

        # 1) Récupération du HTML
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(url) as resp:
                if resp.status == 404:
                    return await interaction.followup.send(f"❌ Profil **{pseudo}** introuvable.")
                html = await resp.text()

        # 2) Parsing et extraction du SCID
        soup = BeautifulSoup(html, "html.parser")
        scid = None

        # a) data-rid sur le header
        header = soup.find("div", class_="profile-header")
        if header and header.get("data-rid"):
            scid = header["data-rid"]

        # b) data-profile-id sur n'importe quel élément
        if not scid:
            elem = soup.find(attrs={"data-profile-id": True})
            if elem:
                scid = elem["data-profile-id"]

        # c) balise meta[name="scid"]
        if not scid:
            meta = soup.find("meta", {"name": "scid"})
            if meta and meta.get("content"):
                scid = meta["content"]

        # d) regex dans les <script>
        if not scid:
            for script in soup.find_all("script"):
                text = script.string or ""
                m = re.search(r'"rid"\s*:\s*"(\d+)"', text)
                if m:
                    scid = m.group(1)
                    break
                m = re.search(r'"profileId"\s*:\s*(\d+)', text)
                if m:
                    scid = m.group(1)
                    break

        # 3) Vérification et embed
        if not scid:
            return await interaction.followup.send(
                f"❌ Impossible de trouver le SCID pour **{pseudo}**. Vérifiez que le profil est public ou que le pseudo est correct."
            )

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
