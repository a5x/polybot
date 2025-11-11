
import discord
from discord.ext import commands
from discord import app_commands
import aiohttp
import json


class KickProfile(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@app_commands.command(name="kickprofile", description="Afficher les infos publiques d'un profil Kick")
	@app_commands.describe(username="Nom d'utilisateur Kick sans @")
	async def kickprofile(self, interaction: discord.Interaction, username: str):
		await interaction.response.defer()

		url = f"https://kick.com/api/v2/channels/{username}"
		headers = {
			"User-Agent": "Mozilla/5.0"
		}

		async with aiohttp.ClientSession(headers=headers) as session:
			async with session.get(url) as resp:
				if resp.status != 200:
					await interaction.followup.send("❌ Utilisateur introuvable ou inaccessible.")
					return

				try:
					data = await resp.json()
				except Exception:
					text = await resp.text()
					try:
						data = json.loads(text)
					except Exception:
						await interaction.followup.send("❌ Impossible de parser la réponse de l'API Kick.")
						return
		def recursive_search(obj, key_names):
			if obj is None:
				return None
			if isinstance(obj, dict):
				for k, v in obj.items():
					if k and k.lower() in key_names:
						return v
					res = recursive_search(v, key_names)
					if res is not None:
						return res
			elif isinstance(obj, list):
				for item in obj:
					res = recursive_search(item, key_names)
					if res is not None:
						return res
			return None
		username_v = None
		display_name = None
		followers = None
		kick_id = None
		avatar_url = None
		subscription_enabled = None
		verified = None
		is_affiliate = None
		user_obj = None
		is_banned = None
		profile_pic = None

		if data:
			username_v = recursive_search(data, {'username', 'login', 'slug'})
			display_name = recursive_search(data, {'displayname', 'display_name', 'name', 'title', 'displayName'})
			followers = recursive_search(data, {'followers', 'followerscount', 'followers_count', 'follower_count', 'followersCount'})
			kick_id = recursive_search(data, {'id', 'user_id', 'kick_id'})
			avatar_url = recursive_search(data, {'avatar', 'profileimage', 'avatar_url', 'image', 'profile_picture', 'avatarUrl', 'profileImage'})
			subscription_enabled = recursive_search(data, {'subscription_enabled', 'is_subscribable', 'subscriptions_enabled'})
			verified = recursive_search(data, {'verified', 'is_verified'})
			is_affiliate = recursive_search(data, {'is_affiliate', 'affiliate', 'affiliate_status'})
			user_obj = recursive_search(data, {'user', 'user_data', 'profile', 'account'})
			profile_pic = recursive_search(data, {'profile_pic', 'profile_image', 'profile_image_url', 'profile_pic_url', 'profilePicture'})
			is_banned = recursive_search(data, {'is_banned', 'banned', 'isBanned'})
			if isinstance(followers, dict):
				for possible in ('count', 'total', 'value'):
					if possible in followers:
						followers = followers[possible]
						break

		username_v = username_v or username
		display_name = display_name or "Nom non trouvé"
		followers = str(followers) if followers is not None else "N/A"
		kick_id = str(kick_id) if kick_id is not None else "N/A"


		user_fields = {}
		if user_obj and isinstance(user_obj, dict):
			for k in ('id', 'username', 'email_verified_at', 'bio', 'country', 'state', 'city', 'instagram', 'twitter', 'youtube', 'discord', 'tiktok', 'facebook', 'channel_id', 'created_at', 'updated_at', 'profile_pic', 'is_banned'):
				if k in user_obj:
					user_fields[k] = user_obj[k]

			if 'username' in user_fields and (not username_v or username_v == username):
				username_v = user_fields.get('username', username_v)
			if 'bio' in user_fields:
				bio = user_fields.get('bio')
			if 'id' in user_fields and (kick_id == "N/A"):
				kick_id = str(user_fields.get('id'))
			if 'channel_id' in user_fields:
				channel_id = str(user_fields.get('channel_id'))
			else:
				channel_id = "N/A"

			if not avatar_url and user_fields.get('profile_pic'):
				avatar_url = user_fields.get('profile_pic')

			if user_fields.get('is_banned') is not None:
				is_banned = user_fields.get('is_banned')
		else:
			channel_id = "N/A"

		def bool_to_yesno(v):
			if v is None:
				return "N/A"
			if isinstance(v, bool):
				return "Oui" if v else "Non"
			if isinstance(v, (int, float)):
				return "Oui" if v else "Non"
			if isinstance(v, str):
				if v.lower() in ('true', '1', 'yes', 'oui'):
					return "Oui"
				if v.lower() in ('false', '0', 'no', 'non'):
					return "Non"
			return str(v)

		desc_lines = []
		bio_text = None
		if 'bio' in locals() and bio:
			bio_text = bio
		elif user_fields.get('bio'):
			bio_text = user_fields.get('bio')
		if bio_text:
			desc_lines.append(bio_text)

		desc_lines.append(f"ID Kick : {kick_id}")
		if channel_id and channel_id != "N/A":
			desc_lines.append(f"Channel ID : {channel_id}")

		embed = discord.Embed(
			title=f"@{username_v}",
			url=f"https://kick.com/{username}",
			description="\n".join(desc_lines) if desc_lines else None,
			color=discord.Color.orange()
		)
		if avatar_url:
			embed.set_thumbnail(url=avatar_url)

		embed.add_field(name="Nom complet", value=display_name, inline=True)
		embed.add_field(name="Followers", value=followers, inline=True)
		embed.add_field(name="Kick ID", value=kick_id, inline=True)
		embed.add_field(name="Vérifié", value=bool_to_yesno(verified), inline=True)
		embed.add_field(name="Affiliate", value=bool_to_yesno(is_affiliate), inline=True)
		embed.add_field(name="Subscription actif", value=bool_to_yesno(subscription_enabled), inline=True)
		embed.add_field(name="Banni", value=bool_to_yesno(is_banned), inline=True)

		if user_fields.get('country') or user_fields.get('city'):
			location = ", ".join(filter(None, [user_fields.get('city'), user_fields.get('state'), user_fields.get('country')]))
			embed.add_field(name="Localisation", value=location or "N/A", inline=True)

		if user_fields.get('created_at'):
			embed.add_field(name="Créé le", value=user_fields.get('created_at'), inline=True)

		socials = []
		for s in ('instagram', 'twitter', 'youtube', 'tiktok', 'discord', 'facebook'):
			v = user_fields.get(s)
			if v:
				socials.append(f"{s}: {v}")
		if socials:
			embed.add_field(name="Réseaux", value="\n".join(socials), inline=False)

		await interaction.followup.send(embed=embed)


async def setup(bot):
	await bot.add_cog(KickProfile(bot))

