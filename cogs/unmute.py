import discord
from discord.ext import commands
from discord import app_commands

class Unmute(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_load(self):
        @app_commands.command(
            name="unmute",
            description="Retire le rôle Muted d'un membre."
        )
        @app_commands.describe(
            membre="Le membre à unmute"
        )
        async def unmute(interaction: discord.Interaction, membre: discord.Member):
            if not interaction.user.guild_permissions.manage_roles:
                await interaction.response.send_message(
                    "Vous n'avez pas la permission de gérer les rôles.",
                    ephemeral=True
                )
                return

            if not interaction.guild.me.guild_permissions.manage_roles:
                await interaction.response.send_message(
                    "Je n'ai pas la permission de gérer les rôles sur ce serveur.",
                    ephemeral=True
                )
                return

            if membre.top_role >= interaction.guild.me.top_role:
                await interaction.response.send_message(
                    "Je ne peux pas unmute ce membre (son rôle est plus haut ou égal au mien).",
                    ephemeral=True
                )
                return

            muted_role = discord.utils.get(interaction.guild.roles, name="mute")
            if muted_role is None:
                await interaction.response.send_message(
                    "Le rôle **Muted** n'existe pas sur ce serveur.",
                    ephemeral=True
                )
                return

            if muted_role not in membre.roles:
                await interaction.response.send_message(
                    f" {membre.mention} n'a pas le rôle Mute !.",
                    ephemeral=True
                )
                return

            try:
                await membre.remove_roles(muted_role, reason=f"Unmute par {interaction.user}")
                await interaction.response.send_message(
                    f" {membre.mention} a été **unmute** ✅✅."
                )
            except Exception as e:
                await interaction.response.send_message(
                    f" Erreur lors du retrait du rôle : {e}",
                    ephemeral=True
                )

        self.bot.tree.add_command(unmute)

async def setup(bot):
    await bot.add_cog(Unmute(bot))
