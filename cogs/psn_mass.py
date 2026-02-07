import discord
from discord import app_commands
from discord.ext import commands
from psnawp_api import PSNAWP
import asyncio
import string
import os

NPSO_TOKEN = os.getenv("PSN_NPSSO", "Gtg5bgo6dpZ8jAqKbdFFCdTtbJL6zzXQ7X8viyYkzEaURAIvuMrv8nn5Z7HlMxut")
psnawp = PSNAWP(NPSO_TOKEN)

class PsnMass(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_psnmass = {}

    @app_commands.command(name="psnmass", description="Vérifie toutes les combinaisons possibles d'un PSN de base.")
    @app_commands.describe(base_psn="Le PSN de base à utiliser pour générer les combinaisons.")
    async def psnmass(self, interaction: discord.Interaction, base_psn: str):
        # Vérification de la longueur du PSN de base
        if len(base_psn) > 4:
            await interaction.response.send_message("Le PSN de base doit contenir 4 caractères ou moins.", ephemeral=True)
            return

        # Anti-spam : délai entre les commandes
        now = asyncio.get_event_loop().time()
        last = self._last_psnmass.get(interaction.user.id)
        if last and (now - last) < 10:
            remaining = int(10 - (now - last))
            await interaction.response.send_message(f"Vous devez attendre {remaining}s avant de réutiliser cette commande.", ephemeral=True)
            return
        self._last_psnmass[interaction.user.id] = now

        await interaction.response.defer()

        # Générer toutes les combinaisons possibles
        characters = string.ascii_lowercase + string.digits
        combinations = [base_psn + c for c in characters]

        results = []
        for psn in combinations:
            try:
                user = psnawp.user(online_id=psn)
                profile = user.profile()

                # Récupérer les informations nécessaires
                country = user.get_region().name if user.get_region() else "Inconnu"
                new_online_id = user.online_id

                results.append({
                    "psn": psn,
                    "country": country,
                    "new_online_id": new_online_id
                })
            except Exception:
                continue  # Ignorer les erreurs pour les PSN inexistants

            # Éviter de surcharger les requêtes
            await asyncio.sleep(1)

        # Trier les résultats par pays
        results.sort(key=lambda x: x["country"])

        # Créer les embeds
        embeds = []
        for i in range(0, len(results), 10):  # 10 résultats par embed
            embed = discord.Embed(title="Résultats de la recherche PSN", color=0x0094FF)
            for result in results[i:i+10]:
                embed.add_field(
                    name=result["psn"],
                    value=f"Pays : {result['country']}\nNouveau Online ID : {result['new_online_id']}",
                    inline=False
                )
            embeds.append(embed)

        # Envoyer les embeds
        if not embeds:
            await interaction.followup.send("Aucun résultat trouvé pour les combinaisons générées.")
        else:
            for embed in embeds:
                await interaction.followup.send(embed=embed)

async def setup(bot):
    await bot.add_cog(PsnMass(bot))
