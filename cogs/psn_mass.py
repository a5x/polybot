import discord
from discord import app_commands
from discord.ext import commands
from psnawp_api import PSNAWP
import asyncio
import string
import os

# Token PSN
NPSO_TOKEN = os.getenv(
    "PSN_NPSSO",
    "Gtg5bgo6dpZ8jAqKbdFFCdTtbJL6zzXQ7X8viyYkzEaURAIvuMrv8nn5Z7HlMxut"
)
psnawp = PSNAWP(NPSO_TOKEN)

class PsnMass(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_psnmass = {}

    @app_commands.command(
        name="psnmass",
        description="Vérifie toutes les combinaisons possibles d'un PSN de base."
    )
    @app_commands.describe(
        base_psn="PSN de base (4 caractères max)",
        mode="Position de la lettre",
        index="Position d'insertion (uniquement pour placement personnalisé)"
    )
    @app_commands.choices(mode=[
        app_commands.Choice(name="Après le PSN (PSNa)", value="after"),
        app_commands.Choice(name="Avant le PSN (aPSN)", value="before"),
        app_commands.Choice(name="Placement personnalisé", value="custom")
    ])
    async def psnmass(
        self,
        interaction: discord.Interaction,
        base_psn: str,
        mode: app_commands.Choice[str],
        index: int | None = None
    ):
        # Vérification longueur
        if len(base_psn) > 2:
            await interaction.response.send_message(
                "❌ Le PSN de base doit contenir 4 caractères ou moins.",
                ephemeral=True
            )
            return

        # Anti-spam (10s)
        now = asyncio.get_event_loop().time()
        last = self._last_psnmass.get(interaction.user.id)
        if last and (now - last) < 10:
            remaining = int(10 - (now - last))
            await interaction.response.send_message(
                f"⏳ Attendez encore {remaining}s avant de réutiliser cette commande.",
                ephemeral=True
            )
            return

        self._last_psnmass[interaction.user.id] = now
        await interaction.response.defer()

        characters = string.ascii_lowercase + string.digits
        combinations = []

        # Génération des PSN
        for c in characters:
            if mode.value == "after":
                psn = base_psn + c

            elif mode.value == "before":
                psn = c + base_psn

            elif mode.value == "custom":
                if index is None:
                    await interaction.followup.send(
                        "⚠️ Vous devez fournir un index pour le placement personnalisé.",
                        ephemeral=True
                    )
                    return

                if index < 0 or index > len(base_psn):
                    await interaction.followup.send(
                        f"⚠️ L'index doit être compris entre 0 et {len(base_psn)}.",
                        ephemeral=True
                    )
                    return

                psn = base_psn[:index] + c + base_psn[index:]

            combinations.append(psn)

        results = []

        # Recherche PSN
        for psn in combinations:
            try:
                user = psnawp.user(online_id=psn)
                profile = user.profile()

                country = user.get_region().name if user.get_region() else "Inconnu"
                new_online_id = user.online_id

                results.append({
                    "psn": psn,
                    "country": country,
                    "new_online_id": new_online_id
                })

            except Exception:
                pass

            await asyncio.sleep(1)  # anti rate-limit

        # Tri par pays
        results.sort(key=lambda x: x["country"])

        # Création des embeds
        embeds = []
        for i in range(0, len(results), 10):
            embed = discord.Embed(
                title="Résultats de la recherche PSN",
                color=0x0094FF
            )
            for result in results[i:i + 10]:
                embed.add_field(
                    name=result["psn"],
                    value=(
                        f"🌍 Pays : {result['country']}\n"
                        f"🆔 Online ID : {result['new_online_id']}"
                    ),
                    inline=False
                )
            embeds.append(embed)

        # Envoi
        if not embeds:
            await interaction.followup.send("❌ Aucun PSN valide trouvé.")
        else:
            for embed in embeds:
                await interaction.followup.send(embed=embed)

async def setup(bot):
    await bot.add_cog(PsnMass(bot))
