import discord
from discord import app_commands
from discord.ext import commands
import json
import base64
import requests
import os
from collections import OrderedDict

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO = "a5x/polybot"
FILE_PATH = "data/psn_db.json"
BRANCH = "main"

class PSNDBCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # 💠 Slash Command
    @app_commands.command(name="db", description="Ajoute un PSN dans psn_db.json")
    @app_commands.describe(pseudo="Le pseudo PSN", dateval="Date et emoji (ex: 2006 <:2k6:…>)")
    async def db(self, interaction: discord.Interaction, pseudo: str, dateval: str):
        # 🔐 Vérification : admin uniquement
        if not interaction.user.guild_permissions.administrator:
            return await interaction.response.send_message("Tu dois être **admin** pour utiliser cette commande.", ephemeral=True)

        await interaction.response.defer()

        # 📥 Lire depuis GitHub
        url = f"https://api.github.com/repos/{REPO}/contents/{FILE_PATH}?ref={BRANCH}"
        headers = {"Authorization": f"token {GITHUB_TOKEN}"}
        res = requests.get(url, headers=headers)
        if res.status_code != 200:
            return await interaction.followup.send("Erreur de lecture du fichier JSON sur GitHub.")

        data = res.json()
        sha = data["sha"]
        content = json.loads(base64.b64decode(data["content"]).decode())

        # ➕ Ajouter la nouvelle entrée
        new_content = OrderedDict(content)
        new_content[pseudo] = dateval

        encoded = base64.b64encode(json.dumps(new_content, indent=2, ensure_ascii=False).encode()).decode()

        # 📤 Push sur GitHub
        update = requests.put(url, headers=headers, json={
            "message": f"Ajout de {pseudo} via Discord",
            "content": encoded,
            "sha": sha,
            "branch": BRANCH
        })

        if update.status_code in (200, 201):
            await interaction.followup.send(f"`{pseudo}` → `{dateval}` ajouté avec succès ! au repo github de @a5x")
        else:
            await interaction.followup.send("Échec de la mise à jour GitHub.")

# Charger le cog
async def setup(bot: commands.Bot):
    await bot.add_cog(PSNDBCog(bot))
