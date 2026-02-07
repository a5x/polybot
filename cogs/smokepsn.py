import discord
from discord import app_commands
from discord.ext import commands

class SmokePsnView(discord.ui.View):
    def __init__(self, psn: str):
        super().__init__(timeout=None)
        self.psn = psn

    @discord.ui.button(label="Temp", style=discord.ButtonStyle.red)
    async def temp_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title="Smoke PSN",
            description=f"PSN : `{self.psn}`",
            color=discord.Color.red()
        )
        embed.set_footer(text="Status: Temp")
        await interaction.response.edit_message(embed=embed)

    @discord.ui.button(label="Fail", style=discord.ButtonStyle.blurple)
    async def fail_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title="Smoke PSN",
            description=f"PSN : `{self.psn}`",
            color=discord.Color.blue()
        )
        embed.set_footer(text="Status: Fail")
        await interaction.response.edit_message(embed=embed)

class SmokePsn(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="smokepsn", description="Envoyer un PSN avec des boutons Temp et Fail.")
    @app_commands.describe(psn="Le PSN à afficher.")
    async def smokepsn(self, interaction: discord.Interaction, psn: str):
        embed = discord.Embed(
            title="Smoke PSN",
            description=f"PSN : `{psn}`",
            color=discord.Color.red()
        )
        embed.set_footer(text="Status: Temp")
        view = SmokePsnView(psn)
        await interaction.response.send_message(embed=embed, view=view)

async def setup(bot):
    await bot.add_cog(SmokePsn(bot))