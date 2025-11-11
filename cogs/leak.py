import discord
from discord import app_commands
from discord.ext import commands
import json
import base64
import requests
import os

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO = "a5x/polybot"
FILE_PATH = "data/leak.json"
BRANCH = "main"

class LeakCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # 💠 Slash Command
    @app_commands.command(name="leak", description="Ajoute un PSN dans leak.json (admin uniquement)")
    @app_commands.describe(pseudo="Le pseudo PSN à marquer comme leak")
    async def leak(self, interaction: discord.Interaction, pseudo: str):
        # 🔐 Vérification : admin uniquement
        if not interaction.user.guild_permissions.administrator:
            return await interaction.response.send_message("Tu dois être **admin** pour utiliser cette commande.", ephemeral=True)

        await interaction.response.defer()

        # 📥 Lire depuis GitHub
        url = f"https://api.github.com/repos/{REPO}/contents/{FILE_PATH}?ref={BRANCH}"
        headers = {"Authorization": f"token {GITHUB_TOKEN}"}
        res = requests.get(url, headers=headers)
        
        if res.status_code == 200:
            # Fichier existe déjà
            data = res.json()
            sha = data["sha"]
            try:
                content = json.loads(base64.b64decode(data["content"]).decode())
            except Exception:
                content = []
        elif res.status_code == 404:
            # Fichier n'existe pas, créer un nouveau
            sha = None
            content = []
        else:
            return await interaction.followup.send("Erreur de lecture du fichier JSON sur GitHub.")

        # ➕ Ajouter le pseudo s'il n'existe pas déjà
            pseudo_lower = pseudo.lower()
            if pseudo_lower not in content:
                content.append(pseudo_lower)
        
        # Trier la liste
        content.sort()

        encoded = base64.b64encode(json.dumps(content, indent=2, ensure_ascii=False).encode()).decode()

        # 📤 Push sur GitHub
        payload = {
            "message": f"Ajout de {pseudo} à leak.json via Discord",
            "content": encoded,
            "branch": BRANCH
        }
        if sha:
            payload["sha"] = sha

        update = requests.put(url, headers=headers, json=payload)

        if update.status_code in (200, 201):
            await interaction.followup.send(f"`{pseudo}` ajouté à **leak.json** avec succès ! ✅")
        else:
            await interaction.followup.send("Échec de la mise à jour GitHub.")

# Charger le cog
async def setup(bot: commands.Bot):
    await bot.add_cog(LeakCog(bot))
