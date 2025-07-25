import discord
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

class DBCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name="db", description="Ajoute une entrée dans psn_db.json")
    async def db(self, ctx, pseudo: str, date: str):
        await ctx.defer()

        # 📥 Récupération du contenu du fichier
        url = f"https://api.github.com/repos/{REPO}/contents/{FILE_PATH}?ref={BRANCH}"
        headers = {"Authorization": f"token {GITHUB_TOKEN}"}
        res = requests.get(url, headers=headers)
        if res.status_code != 200:
            return await ctx.respond("❌ Erreur lors de la lecture de psn_db.json sur GitHub.")

        data = res.json()
        sha = data["sha"]
        current_content = json.loads(base64.b64decode(data["content"]).decode())

        # 🧱 Ajout de la nouvelle entrée en bas
        new_entry = OrderedDict(current_content)
        new_entry[pseudo] = date

        # 🧬 Encodage du nouveau contenu
        new_content = base64.b64encode(json.dumps(new_entry, indent=2, ensure_ascii=False).encode()).decode()

        # 📤 Commit sur GitHub
        update_res = requests.put(url, headers=headers, json={
            "message": f"Ajout de {pseudo} dans psn_db.json",
            "content": new_content,
            "sha": sha,
            "branch": BRANCH
        })

        if update_res.status_code in [200, 201]:
            await ctx.respond(f"✅ L'entrée `{pseudo}` → `{date}` a été ajoutée avec succès !")
        else:
            await ctx.respond("❌ Échec de la mise à jour du fichier sur GitHub.")

def setup(bot):
    bot.add_cog(DBCommand(bot))
