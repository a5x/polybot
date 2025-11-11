import discord
from discord.ext import commands
from discord import app_commands
import aiohttp

class Crew(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def _headers(self, bearer_token: str) -> dict:
        """Génère les headers avec le Bearer Token"""
        return {
            "Authorization": f"Bearer {bearer_token}",
            "X-Requested-With": "XMLHttpRequest",
        }

    @app_commands.command(name="crew", description="Afficher les infos d'un crew GTA Online")
    @app_commands.describe(
        bearer_token="Votre Bearer Token Rockstar",
        crew_name="Nom du crew à rechercher"
    )
    async def crew(self, interaction: discord.Interaction, bearer_token: str, crew_name: str):
        # Réponse invisible aux autres utilisateurs
        await interaction.response.defer(ephemeral=True)

        api_base_url = "https://scapi.rockstargames.com/crew/byname"
        params = {"name": crew_name}

        try:
            async with aiohttp.ClientSession(headers=self._headers(bearer_token)) as session:
                async with session.get(api_base_url, params=params, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                    if resp.status == 401:
                        await interaction.followup.send("❌ Bearer Token invalide ou expiré.")
                        return
                    elif resp.status != 200:
                        await interaction.followup.send(f"❌ Erreur lors de la connexion à l'API (code: {resp.status})")
                        return

                    data = await resp.json()

            # Vérifier si des crews ont été trouvés
            crews = data.get("Crews")
            if not crews:
                await interaction.followup.send(f"❌ Aucun crew trouvé avec le nom '{crew_name}'")
                return

            crew = crews[0]  # Premier résultat

            # Extraire les informations
            crew_name_display = crew.get("name", "N/A")
            crew_tag = crew.get("tag", "N/A")
            crew_motto = crew.get("motto", "Aucune devise")
            member_count = crew.get("memberCount", 0)
            is_private = crew.get("isPrivate", False)
            is_dev = crew.get("isSystemCrew", False)
            crew_color_hex = crew.get("color", "#FFFFFF")
            crew_id = crew.get("crewId", "N/A")

            # Créer l'embed Discord
            embed = discord.Embed(
                title=f"[{crew_tag}] {crew_name_display}",
                description=crew_motto if crew_motto else "Aucune devise",
                url=f"https://socialclub.rockstargames.com/crew/{crew_id}",
                color=int(crew_color_hex.replace("#", ""), 16) if crew_color_hex else discord.Color.blue().value
            )

            embed.add_field(name="👥 Membres", value=f"{member_count:,}", inline=True)
            embed.add_field(name="🔒 Privé", value="✅ Oui" if is_private else "❌ Non", inline=True)
            embed.add_field(name="⭐ Crew Dev", value="✅ Oui" if is_dev else "❌ Non", inline=True)
            embed.add_field(name="🏷️ Tag", value=crew_tag, inline=True)
            embed.add_field(name="🆔 Crew ID", value=crew_id, inline=True)

            embed.set_footer(text="Powered by Rockstar Social Club API")

            await interaction.followup.send(embed=embed)

        except aiohttp.ClientError as e:
            await interaction.followup.send(f"❌ Erreur de connexion: {str(e)}")


async def setup(bot):
    await bot.add_cog(Crew(bot))
