import os
import sys
import asyncio
from dotenv import load_dotenv
import discord
from discord.ext import commands
from keep_alive import keep_alive

# Démarre le petit serveur pour keep-alive (Replit / Glitch…)
keep_alive()
load_dotenv()

# Intents partagés
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# Instancie deux bots avec préfixes distincts
bot1 = commands.Bot(command_prefix="!a ", intents=intents)
bot2 = commands.Bot(command_prefix="!b ", intents=intents)

# Liste des COGS à charger sur chaque bot
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
    "cogs.psn",
    "cogs.psn_embed",
    "cogs.leak"
    "cogs.db",
]

async def load_extensions(bot: commands.Bot):
    """Charge ou recharge tous les COGS sur le bot donné."""
    for ext in COGS:
        try:
            await bot.load_extension(ext)
            print(f"✅ Chargé sur {bot.user or bot}: {ext}")
        except commands.errors.ExtensionAlreadyLoaded:
            await bot.reload_extension(ext)
            print(f"♻️ Rechargé sur {bot.user or bot}: {ext}")

@bot1.event
async def on_ready():
    print(f"🔵 Bot1 connecté en tant que {bot1.user}")
    # Synchronise les slash-commands **après** on_ready
    await bot1.tree.sync()
    print("✅ Slash commands de Bot1 synchronisées")

@bot2.event
async def on_ready():
    print(f"🟢 Bot2 connecté en tant que {bot2.user}")
    # Même chose pour Bot2
    await bot2.tree.sync()
    print("✅ Slash commands de Bot2 synchronisées")

async def cmd_input():
    """Boucle CLI pour recharger ou stopper les deux bots."""
    loop = asyncio.get_event_loop()
    while True:
        try:
            cmd = await loop.run_in_executor(None, input, "> ")
        except EOFError:
            break

        cmd = cmd.strip().lower()
        if cmd == "reload":
            print("♻️ Relancement des cogs sur les deux bots…")
            await load_extensions(bot1)
            await load_extensions(bot2)
            # Resync des slash-commands après rechargement
            await bot1.tree.sync()
            await bot2.tree.sync()
            print("✅ Tous les cogs rechargés et slash commands resynchronisées.")
        elif cmd == "stop":
            print("Fermeture des deux bots…")
            await bot1.close()
            await bot2.close()
            break
        else:
            print("Commande inconnue. Utilise : reload / stop")

async def main():
    # Récupère séparément les deux tokens
    token1 = os.getenv("DISCORD_TOKEN")
    token2 = os.getenv("DISCORD_TOKEN2")
    if not token1 or not token2:
        raise RuntimeError("Il faut définir DISCORD_TOKEN et DISCORD_TOKEN2 dans le .env")

    # Charge les cogs avant de démarrer (onReady n'est pas encore appelé, mais load_extension ne dépend pas de tree.sync)
    await load_extensions(bot1)
    await load_extensions(bot2)

    # Lance les deux bots en parallèle
    tasks = [
        bot1.start(token1),
        bot2.start(token2),
    ]
    # Ajoute la boucle CLI si on est en terminal interactif
    if sys.stdin.isatty():
        tasks.append(cmd_input())

    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
