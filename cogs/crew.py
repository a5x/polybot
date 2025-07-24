# cogs/crew.py
import discord
from discord.ext import commands
from discord import app_commands
import aiohttp
from bs4 import BeautifulSoup

class CrewCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="crew",
        description="Vérifie si un crew existe sur Rockstar Social Club et affiche ses infos"
    )
    @app_commands.describe(
        name="Le nom du crew Social Club (ex : kaid_gvng)"
    )
    async def crew(
        self,
        interaction: discord.Interaction,
        name: str,
    ):
        await interaction.response.defer(thinking=True)
        tag = name.lower().replace(" ", "_")
        url = f"https://socialclub.rockstargames.com/crew/{tag}/hierarchy"

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status != 200:
                    return await interaction.followup.send(
                        f"⚠️ Impossible de vérifier `{tag}` (HTTP {resp.status})."
                    )
                html = await resp.text()

        # Parse HTML
        soup = BeautifulSoup(html, "html.parser")

        # Détection de non-existence
        if soup.find(string=lambda t: "disbanded" in t.lower()) or "Not Found" in html:
            return await interaction.followup.send(
                f"❌ Le crew `{tag}` n’existe pas ou a été dissous."
            )

        # Récupération du nom complet du crew
        title_el = soup.select_one("h1.sc-heading--alpha")
        crew_name = title_el.get_text(strip=True) if title_el else tag

        # Récupération de la plaque/tag
        tag_el = soup.select_one(".crew-tag")
        crew_tag = tag_el.get_text(strip=True) if tag_el else "—"

        # Récupération du nombre de membres
        members_el = soup.select_one("li[data-view='hierarchy-members'] .stat-value")
        members = members_el.get_text(strip=True) if members_el else "—"

        # Construction de l'embed
        embed = discord.Embed(
            title=crew_name,
            url=url,
            color=discord.Color.blue()
        )
        embed.set_thumbnail(url="https://socialclub.rockstargames.com/images/crew-icon.png")
        embed.add_field(name="Tag", value=crew_tag, inline=True)
        embed.add_field(name="Membres", value=members, inline=True)
        embed.set_footer(text=f"Requête pour /crew {tag}")

        await interaction.followup.send(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(CrewCog(bot))
