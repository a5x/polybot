import discord
from discord.ext import commands
from discord import app_commands
import aiohttp
import datetime

class Roblox(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="robloxprofile", description="Afficher les infos publiques d'un profil Roblox")
    @app_commands.describe(username="Nom d'utilisateur Roblox")
    async def robloxprofile(self, interaction: discord.Interaction, username: str):
        await interaction.response.defer()
        async with aiohttp.ClientSession() as session:
            # 1) Obtenir l'ID à partir du nom
            url_id = "https://users.roblox.com/v1/usernames/users"
            payload = {"usernames": [username], "excludeBannedUsers": False}
            async with session.post(url_id, json=payload) as resp:
                data = await resp.json()
                if not data["data"]:
                    return await interaction.followup.send("❌ Utilisateur introuvable.")
                user_id = data["data"][0]["id"]

            # 2) Profil général (+ isBanned et description)
            async with session.get(f"https://users.roblox.com/v1/users/{user_id}") as resp:
                profile = await resp.json()
                is_banned = profile.get("isBanned", False)  # :contentReference[oaicite:2]{index=2}
                about_me = profile.get("description", "")

            # 3) Présence (online/offline)
            async with session.post(
                "https://presence.roblox.com/v1/presence/users",
                json={"userIds": [user_id]}
            ) as resp:
                pres = await resp.json()
                pres_data = pres.get("userPresences", [{}])[0]
                ptype = pres_data.get("userPresenceType", 0)
                status = "Online" if ptype == 1 else "Offline"  # :contentReference[oaicite:3]{index=3}

            # 4) Stats sociales
            async with session.get(f"https://friends.roblox.com/v1/users/{user_id}/friends/count") as resp:
                friends = (await resp.json()).get("count", 0)
            async with session.get(f"https://friends.roblox.com/v1/users/{user_id}/followers/count") as resp:
                followers = (await resp.json()).get("count", 0)
            async with session.get(f"https://friends.roblox.com/v1/users/{user_id}/followings/count") as resp:
                followings = (await resp.json()).get("count", 0)

            # 5) Avatar
            thumb_url = (
                f"https://thumbnails.roblox.com/v1/users/avatar?"
                f"userIds={user_id}&size=420x420&format=Png&isCircular=false"
            )
            async with session.get(thumb_url) as resp:
                thumb = await resp.json()
                avatar_url = thumb["data"][0]["imageUrl"] if thumb["data"] else None

            # 6) Vérification du badge “Verified”
            profile_page = f"https://www.roblox.com/users/{user_id}/profile"
            async with session.get(profile_page) as resp:
                html = await resp.text()
                is_verified = 'data-is-verified="true"' in html

            # 7) (Optionnel) RAP & valeur via Rolimon’s (nécessite proxy/API clé)
            try:
                rol_api = f"https://api.rolimons.com/playerapi/user?user={user_id}"
                async with session.get(rol_api) as resp:
                    rol = await resp.json()
                    rap   = rol.get("rap", "N/A")
                    value = rol.get("value", "N/A")
            except:
                rap, value = "N/A", "N/A"

        # Formatage des dates
        created = datetime.datetime.fromisoformat(profile["created"].replace("Z", "+00:00"))
        created_str = created.strftime("%d %B %Y")

        # Construction de l’embed
        embed = discord.Embed(
            title=f"{profile['name']}",
            url=profile_page,
            color=discord.Color.dark_gray()
        )
        if avatar_url:
            embed.set_thumbnail(url=avatar_url)

        embed.add_field(
            name="Social",
            value=f"👥 Amis : {friends} | Followers : {followers} | Following : {followings}",
            inline=False
        )
        embed.add_field(name="ID", value=user_id, inline=True)
        embed.add_field(
            name="Vérifié",
            value="✅" if is_verified else "❌",
            inline=True
        )
        embed.add_field(name="Statut", value=status, inline=True)
        embed.add_field(name="Banni ?", value="❌ Oui" if is_banned else "✅ Non", inline=True)
        embed.add_field(name="Date de création", value=created_str, inline=True)
        embed.add_field(name="About Me", value=about_me or "—", inline=False)
        embed.add_field(name="RAP", value=str(rap), inline=True)
        embed.add_field(name="Valeur estimée", value=str(value), inline=True)

        await interaction.followup.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Roblox(bot))
