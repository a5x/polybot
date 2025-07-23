import os
import discord
from discord.ext import commands
import asyncio

# Charger le token depuis les variables d'environnement
TOKEN = os.getenv("ODM1MTk1ODQ2NzAxNzQ0MTQ4.GZuXsR.vstOuQTcHc5JS8ac1K9PL5GH-cZCugB-0HO_7s")
if not TOKEN:
    raise RuntimeError("Le token DISCORD_TOKEN n'est pas défini dans les variables d'environnement.")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Nom des cogs à charger
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
    print("✅ Bot prêt. Utilise 'reload' ou 'stop' en console pour gérer le bot.")

async def load_extensions():
    for ext in COGS:
        try:
            await bot.load_extension(ext)
            print(f"✅ Cog chargée : {ext}")
        except commands.errors.ExtensionAlreadyLoaded:
            await bot.reload_extension(ext)
            print(f"♻️ Cog rechargée : {ext}")

async def cmd_input():
    """
    Gestion de la console stdin. Ignore l'EOF pour éviter les crashs sur Railway.
    """
    loop = asyncio.get_event_loop()
    while True:
        try:
            cmd = await loop.run_in_executor(None, input, "> ")
        except EOFError:
            # Plus de stdin disponible, on sort proprement
            break

        cmd = cmd.strip().lower()
        if cmd == "reload":
            print("♻️ Relancement des cogs...")
            await load_extensions()
            await bot.tree.sync()
            print("✅ Tous les cogs rechargés et slash commands synchronisées.")
        elif cmd == "stop":
            print("🔌 Arrêt du bot...")
            await bot.close()
            break
        else:
            print("❓ Commande inconnue. Utilise : reload / stop")

async def main():
    # Charger les cogs avant de démarrer le bot
    await load_extensions()
    # Démarrer le bot et la lecture console en parallèle
    await asyncio.gather(
        bot.start(TOKEN),
        cmd_input()
    )

if __name__ == "__main__":
    asyncio.run(main())
