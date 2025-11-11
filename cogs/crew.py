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

    def _first_present(self, data: dict, *keys, default=None):
        """
        Retourne la première valeur non-None trouvée dans data pour la liste de keys donnée.
        Keys peuvent être 'CrewName', 'name', etc.
        """
        for k in keys:
            if k in data and data[k] is not None:
                return data[k]
        return default

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

            # Cas 1: réponse avec liste "Crews": prendre le premier élément si présent
            crew = None
            if isinstance(data, dict) and "Crews" in data and isinstance(data["Crews"], (list, tuple)) and data["Crews"]:
                crew = data["Crews"][0]
            elif isinstance(data, dict) and any(k in data for k in ("CrewId", "crewId", "CrewName", "name", "CrewTag", "tag")):
                # Cas 2: la réponse contient directement les champs du crew (pas de "Crews")
                crew = data
            else:
                # Sinon essayer d'extraire d'autres formes (par sécurité)
                # Parfois l'API peut retourner un dict avec une sous-clé (ex: "result" ou "data")
                for subkey in ("result", "data", "crew", "Crew", "Response"):
                    if isinstance(data, dict) and subkey in data and isinstance(data[subkey], dict):
                        crew = data[subkey]
                        break

            if not crew:
                await interaction.followup.send(f"❌ Aucun crew trouvé avec le nom '{crew_name}'")
                return

            # Récupération robuste des champs (plusieurs noms de clés testés)
            crew_name_display = self._first_present(crew, "CrewName", "name", "crewName", default="N/A")
            crew_tag = self._first_present(crew, "CrewTag", "tag", "crewTag", default="N/A")
            crew_motto = self._first_present(crew, "CrewMotto", "motto", "CrewMotto", default="Aucune devise")
            member_count = self._first_present(crew, "MemberCount", "memberCount", "Membercount", default=0)
            is_private = self._first_present(crew, "IsPrivate", "isPrivate", default=False)
            # Dev flag peut être "Dev", "isSystemCrew" ou "Dev"
            is_dev = self._first_present(crew, "Dev", "isSystemCrew", "DevFlag", default=False)
            crew_color_hex = self._first_present(crew, "CrewColour", "CrewColor", "color", "CrewColour", default="#FFFFFF")
            crew_id = self._first_present(crew, "CrewId", "crewId", "crewID", default="N/A")

            # Normaliser le member_count s'il est en string
            try:
                member_count_int = int(str(member_count).replace(",", ""))
            except Exception:
                member_count_int = 0

            # Construire l'embed
            # convert hex to int safely
            color_value = None
            try:
                color_value = int(str(crew_color_hex).replace("#", ""), 16)
            except Exception:
                color_value = discord.Color.blue().value

            embed = discord.Embed(
                title=f"[{crew_tag}] {crew_name_display}",
                description=crew_motto if crew_motto else "Aucune devise",
                url=f"https://socialclub.rockstargames.com/crew/{crew_id}",
                color=color_value
            )

            embed.add_field(name="👥 Membres", value=f"{member_count_int:,}", inline=True)
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
