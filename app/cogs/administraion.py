import discord
from discord import app_commands
from discord.ext import commands

class Administration(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="give", description="Give coins to a user (Admin only)")
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.describe(
        user="The user to give coins to",
        amount="Amount of coins to give"
    )
    async def give(self, interaction: discord.Interaction, user: discord.User, amount: int):
        from app.database.db import Database
        db = Database()
        
        if amount <= 0:
            await interaction.response.send_message("Amount must be positive!", ephemeral=True)
            return
            
        await db.update_balance(str(user.id), amount)
        embed = discord.Embed(
            title="💸 Coins Given",
            description=f"Gave {amount} coins to {user.mention}",
            color=discord.Color.purple()
        )
        await interaction.response.send_message(embed=embed)

    @give.error
    async def give_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.MissingPermissions):
            await interaction.response.send_message(
                "You need administrator permissions to use this command!",
                ephemeral=True
            )

async def setup(bot):
    await bot.add_cog(Administration(bot))
