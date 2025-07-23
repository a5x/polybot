import os
import discord
from discord.ext import commands
import asyncio

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ✅ Nom des cogs à charger
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
    print("✅ Bot prêt. Tape `reload` ou `stop` dans le terminal pour recharger/arrêter le bot.")

async def load_extensions():
    for ext in COGS:
        try:
            await bot.load_extension(ext)
            print(f"✅ Cog chargée : {ext}")
        except commands.errors.ExtensionAlreadyLoaded:
            await bot.reload_extension(ext)
            print(f"♻️ Cog rechargée : {ext}")

async def cmd_input():
    while True:
        cmd = await asyncio.get_event_loop().run_in_executor(None, input, "> ")
        cmd = cmd.strip().lower()
        if cmd == "reload":
            print("♻️ Relancement des cogs...")
            await load_extensions()
            await bot.tree.sync()
            print("✅ Tous les cogs rechargés.")
        elif cmd == "stop":
            print("Fermeture du bot...")
            await bot.close()
            break
        else:
            print("Commande inconnue. Utilise : reload / stop")

async def main():
    # Récupère le token depuis la variable d'env
    token = os.environ.get("DISCORD_TOKEN")
    if not token:
        raise RuntimeError("⚠️ La variable d'environnement DISCORD_TOKEN n'est pas définie.")
    
    # Lance les cogs puis le bot et la boucle de commandes concurrently
    async with bot:
        await load_extensions()
        await asyncio.gather(
            bot.start(token),
            cmd_input(),
        )

if __name__ == "__main__":
    asyncio.run(main())
