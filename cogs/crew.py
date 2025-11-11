import discord
from discord.ext import commands
from discord import app_commands
import aiohttp

class Crew(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="crew", description="Afficher les infos d'un crew GTA Online")
    @app_commands.describe(crew_name="Nom du crew à rechercher")
    async def crew(self, interaction: discord.Interaction, crew_name: str):
        await interaction.response.defer()

        api_base_url = "https://socialclub.rockstargames.com/crewsapi/SearchCrews"
        
        # Headers pour l'API Rockstar
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        
        # Paramètres pour la recherche
        params = {
            "searchTerm": crew_name,
            "crewType": "",
            "openCrewFilter": -1,
            "systemCrewFilter": -1
        }

        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(api_base_url, params=params) as resp:
                if resp.status != 200:
                    await interaction.followup.send(
                        f"❌ Erreur lors de la connexion à l'API (code: {resp.status})"
                    )
                    return

                data = await resp.json()

        # Vérifier si des crews ont été trouvés
        if not data.get("Crews") or len(data["Crews"]) == 0:
            await interaction.followup.send(
                f"❌ Aucun crew trouvé avec le nom '{crew_name}'"
            )
            return

        # Prendre le premier résultat
        crew = data["Crews"][0]

        # Extraire les informations
        crew_name_display = crew.get("CrewName", "N/A")
        crew_tag = crew.get("CrewTag", "N/A")
        crew_motto = crew.get("CrewMotto", "N/A")
        member_count = crew.get("MemberCount", 0)
        is_private = crew.get("IsPrivate", False)
        is_dev = crew.get("Dev", False)
        crew_color_hex = crew.get("CrewColour", "#FFFFFF")
        crew_url = crew.get("CrewUrl", "")

        # Créer l'embed
        embed = discord.Embed(
            title=f"[{crew_tag}] {crew_name_display}",
            description=crew_motto if crew_motto else "Aucune devise",
            url=f"https://socialclub.rockstargames.com{crew_url}" if crew_url else None,
            color=int(crew_color_hex.replace("#", ""), 16)
        )

        # Ajouter les champs
        embed.add_field(
            name="👥 Nombre de membres",
            value=f"{member_count:,}",
            inline=True
        )

        embed.add_field(
            name="🔒 Privé",
            value="✅ Oui" if is_private else "❌ Non",
            inline=True
        )

        embed.add_field(
            name="⭐ Crew Dev",
            value="✅ Oui" if is_dev else "❌ Non",
            inline=True
        )

        embed.add_field(
            name="🏷️ Tag",
            value=crew_tag,
            inline=True
        )

        # Ajouter d'autres infos utiles
        crew_type = crew.get("CrewType", "N/A")
        embed.add_field(
            name="📂 Type",
            value=crew_type if crew_type else "N/A",
            inline=True
        )

        is_open = crew.get("IsOpen", False)
        embed.add_field(
            name="📖 Ouvert",
            value="✅ Oui" if is_open else "❌ Non",
            inline=True
        )

        embed.set_footer(text="Powered by Rockstar Social Club API")

        await interaction.followup.send(embed=embed)
async def setup(bot):
    await bot.add_cog(Crew(bot))
