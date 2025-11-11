import discord
from discord.ext import commands
from discord import app_commands
import aiohttp
from datetime import datetime

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
        for k in keys:
            if k in data and data[k] is not None:
                return data[k]
        return default

    @app_commands.command(name="crew", description="Afficher les infos d'un crew GTA Online")
    @app_commands.describe(
        bearer_token="Votre Bearer Token Rockstar",
        search_by="Rechercher par 'name' ou 'id'",
        query="Nom ou ID du crew selon le type de recherche"
    )
    async def crew(self, interaction: discord.Interaction, bearer_token: str, search_by: str, query: str):
        await interaction.response.defer(ephemeral=True)

        search_by = search_by.lower()
        if search_by not in ("name", "id"):
            await interaction.followup.send("❌ Paramètre `search_by` invalide, utilisez 'name' ou 'id'.")
            return

        if search_by == "name":
            api_url = "https://scapi.rockstargames.com/crew/byname"
            params = {"name": query}
        else:  # search_by == "id"
            api_url = f"https://scapi.rockstargames.com/crew/{query}"
            params = None

        try:
            async with aiohttp.ClientSession(headers=self._headers(bearer_token)) as session:
                async with session.get(api_url, params=params, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                    if resp.status == 401:
                        await interaction.followup.send("❌ Bearer Token invalide ou expiré.")
                        return
                    elif resp.status != 200:
                        await interaction.followup.send(f"❌ Erreur API (code: {resp.status})")
                        return

                    data = await resp.json()

            # Récupérer le crew
            crew = None
            if isinstance(data, dict) and "Crews" in data and isinstance(data["Crews"], (list, tuple)) and data["Crews"]:
                crew = data["Crews"][0]
            elif isinstance(data, dict) and any(k in data for k in ("CrewId", "crewId", "CrewName", "name", "CrewTag", "tag")):
                crew = data
            else:
                for subkey in ("result", "data", "crew", "Crew", "Response"):
                    if isinstance(data, dict) and subkey in data and isinstance(data[subkey], dict):
                        crew = data[subkey]
                        break

            if not crew:
                await interaction.followup.send(f"❌ Aucun crew trouvé avec le {search_by} '{query}'")
                return

            # Champs du crew
            crew_name_display = self._first_present(crew, "CrewName", "name", "crewName", default="N/A")
            crew_tag = self._first_present(crew, "CrewTag", "tag", "crewTag", default="N/A")
            crew_motto = self._first_present(crew, "CrewMotto", "motto", default="Aucune devise")
            member_count = self._first_present(crew, "MemberCount", "memberCount", default=0)
            is_private = self._first_present(crew, "IsPrivate", "isPrivate", default=False)
            is_dev = self._first_present(crew, "Dev", "isSystemCrew", "DevFlag", default=False)
            is_founder = self._first_present(crew, "IsFounderCrew", "isFounderCrew", default=False)
            crew_color_hex = self._first_present(crew, "CrewColour", "CrewColor", "color", default="#FFFFFF")
            crew_id = self._first_present(crew, "CrewId", "crewId", "crewID", default="N/A")

            # Date création
            created_at_raw = self._first_present(crew, "Created", "CreatedAt", "DateCreated", default=None)
            created_at_display = "N/A"
            if created_at_raw:
                try:
                    dt = datetime.fromisoformat(created_at_raw.replace("Z", "+00:00"))
                    created_at_display = dt.strftime("%d/%m/%Y %H:%M:%S")
                except Exception:
                    created_at_display = created_at_raw

            # Normaliser member_count
            try:
                member_count_int = int(str(member_count).replace(",", ""))
            except Exception:
                member_count_int = 0

            # Couleur embed
            try:
                color_value = int(str(crew_color_hex).replace("#", ""), 16)
            except Exception:
                color_value = discord.Color.blue().value

            # Embed
            embed = discord.Embed(
                title=f"[{crew_tag}] {crew_name_display}",
                description=crew_motto,
                url=f"https://socialclub.rockstargames.com/crew/{crew_id}",
                color=color_value
            )

            embed.add_field(name="👥 Membres", value=f"{member_count_int:,}", inline=True)
            embed.add_field(name="🔒 Privé", value="✅ Oui" if is_private else "❌ Non", inline=True)
            embed.add_field(name="⭐ Crew Dev", value="✅ Oui" if is_dev else "❌ Non", inline=True)
            embed.add_field(name="👑 Fondateur", value="✅ Oui" if is_founder else "❌ Non", inline=True)
            embed.add_field(name="📅 Créé le", value=created_at_display, inline=True)
            embed.add_field(name="🏷️ Tag", value=crew_tag, inline=True)
            embed.add_field(name="🆔 Crew ID", value=crew_id, inline=True)

            # Thumbnail logo
            embed.set_thumbnail(url=f"https://prod.cloud.rockstargames.com/crews/sc/0/{crew_id}/publish/emblem/emblem_128.png")
            embed.set_footer(text="Powered by Rockstar Social Club API")

            await interaction.followup.send(embed=embed)

        except aiohttp.ClientError as e:
            await interaction.followup.send(f"❌ Erreur de connexion: {str(e)}")


async def setup(bot):
    await bot.add_cog(Crew(bot))
