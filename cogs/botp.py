import discord
from discord.ext import commands
from discord import app_commands

class AdminCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_load(self):
        admin_group = app_commands.Group(
            name="admin",
            description="Commandes réservées aux admins"
        )

        @admin_group.command(name="botp", description="Le bot parle à votre place.")
        @app_commands.describe(message="Le message que le bot doit envoyer")
        async def botp(interaction: discord.Interaction, message: str):
            if not interaction.user.guild_permissions.administrator:
                await interaction.response.send_message(
                    "❌ Vous devez être administrateur pour utiliser cette commande.",
                    ephemeral=True
                )
                return

            await interaction.channel.send(message)
            await interaction.response.send_message(
                "✅ Message envoyé avec succès !",
                ephemeral=True
            )

        self.bot.tree.add_command(admin_group)

async def setup(bot):
    await bot.add_cog(AdminCommands(bot))
