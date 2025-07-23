import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
import asyncio

# Charge les variables d'environnement depuis .env si présent
load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ✅ Liste des cogs à charger
COGS = [
    "cogs.jeux",
    "cogs.economie",
    "cogs.serverinfo",
    "cogs.userinfo",
    "cogs.kick",
    "cogs.magasin",
    "cogs.botp",
    "cogs.peche",
    "cogs.ban",
    "cogs.unban",
    "cogs.mute",
    "cogs.unmute",
    "cogs.tempmute",
    "cogs.warn",
    "cogs.hswarn",
    "cogs.poker",
    "cogs.help",
    "cogs.blackjack",
    "cogs.roulette",
    "cogs.clear",
    "cogs.coursechevaux",
    "cogs.claque",
    "cogs.botinfo",
    "cogs.role",
    "cogs.ticket",
    "cogs.robloxprofile",
    "cogs.instagramprofile",
    "cogs.statusbot",
    "cogs.psn",
]

@bot.event
async def on_ready():
    print(f"✅ Connecté en tant que {bot.user}")
    await bot.tree.sync()
    print("✅ Slash commands ON")

async def load_extensions():
    for ext in COGS:
        try:
            await bot.load_extension(ext)
            print(f"✅ Cog chargée : {ext}")
        except commands.errors.ExtensionAlreadyLoaded:
            await bot.reload_extension(ext)
            print(f"♻️ Cog rechargée : {ext}")

async def main():
    # Récupération du token depuis la variable d'environnement
    token = os.environ.get("DISCORD_TOKEN")
    if not token:
        raise RuntimeError("⚠️ La variable d'environnement DISCORD_TOKEN n'est pas définie.")

    # Chargement des cogs
    await load_extensions()

    # Démarrage du bot
    await bot.start(token)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Arrêt manuel reçu, fermeture du bot...")
        # Nettoyage si besoin
        sys.exit(0)
