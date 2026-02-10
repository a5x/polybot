import discord
from discord import app_commands
from discord.ext import commands
from psnawp_api import PSNAWP
import asyncio
import string
import os

# Token PS
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
        description="Recherche les PSN existants en ajoutant une lettre."
    )
    @app_commands.describe(
        base_psn="PSN de base (2 ou 3 caractères)",
        mode="Position de la lettre",
        index="Index d'insertion (utilisé seulement si mode = custom)"
    )
    @app_commands.choices(mode=[
        app_commands.Choice(name="Après le PSN (PSNa)", value="after"),
        app_commands.Choice(name="Avant le PSN (aPSN)", value="before"),
        app_commands.Choice(name="Placement personnalisé (PSaN)", value="custom")
    ])
    async def psnmass(
        self,
        interaction: discord.Interaction,
        base_psn: str,
        mode: app_commands.Choice[str],
        index: int | None = None
    ):
        # Validation longueur (2 ou 3 UNIQUEMENT)
        if len(base_psn) not in (2, 3):
            await interaction.response.send_message(
                "❌ Le PSN de base doit contenir **2 ou 3 caractères**.",
                ephemeral=True
            )
            return

        # Anti-spam 10s
        now = asyncio.get_event_loop().time()
        last = self._last_psnmass.get(interaction.user.id)
        if last and (now - last) < 10:
            remaining = int(10 - (now - last))
            await interaction.response.send_message(
                f"⏳ Attendez {remaining}s avant de réutiliser la commande.",
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
                        "⚠️ Vous devez préciser **index** pour le placement personnalisé.",
                        ephemeral=True
                    )
                    return

                if index < 0 or index > len(base_psn):
                    await interaction.followup.send(
                        f"⚠️ L'index doit être entre **0 et {len(base_psn)}**.",
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
                current_online_id = user.online_id

                # Détection changement d'Online ID
                has_new_id = current_online_id.lower() != psn.lower()

                results.append({
                    "psn": psn,
                    "country": country,
                    "new_id": current_online_id if has_new_id else None
                })

            except Exception:
                pass

            await asyncio.sleep(1)

        if not results:
            await interaction.followup.send("❌ Aucun PSN trouvé.")
            return

        embed = discord.Embed(
            title="Résultats PSN",
            description=f"Mode : **{mode.name}**",
            color=0x0094FF
        )

        for r in results[:25]:
            value = f"🌍 Pays : {r['country']}"
            if r["new_id"]:
                value += f"\n🔁 Nouvel Online ID : **{r['new_id']}**"

            embed.add_field(
                name=r["psn"],
                value=value,
                inline=False
            )

        await interaction.followup.send(embed=embed)

async def setup(bot):
    await bot.add_cog(PsnMass(bot))
