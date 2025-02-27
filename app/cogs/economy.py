import discord
from discord import app_commands
from discord.ext import commands
import random
from app.database.db import Database

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = Database()

    @app_commands.command(name="balance", description="Check your balance")
    @app_commands.describe(user="Check another user's balance (optional)")
    async def balance(self, interaction: discord.Interaction, user: discord.User = None):
        target_user = user or interaction.user
        user_id = str(target_user.id)
        balance = await self.db.get_balance(user_id)
        embed = discord.Embed(
            title="💰 Balance",
            description=f"{target_user.mention}'s balance: **{balance}** coins",
            color=discord.Color.green()
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="work", description="Work to earn coins")
    @app_commands.checks.cooldown(1, 3600)
    async def work(self, interaction: discord.Interaction):
        user_id = str(interaction.user.id)
        earnings = random.randint(50, 200)
        await self.db.update_balance(user_id, earnings)
        
        embed = discord.Embed(
            title="🏢 Work",
            description=f"You worked hard and earned **{earnings}** coins!",
            color=discord.Color.blue()
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="shop", description="View available items")
    async def shop(self, interaction: discord.Interaction):
        items = {
            "VIP Role": 1000,
            "Custom Color": 500,
            "Profile Badge": 250
        }
        
        embed = discord.Embed(title="🛒 Shop", color=discord.Color.gold())
        for item, price in items.items():
            embed.add_field(
                name=item,
                value=f"Price: {price} coins",
                inline=False
            )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="buy", description="Buy an item from the shop")
    @app_commands.describe(item="The item to purchase")
    @app_commands.choices(item=[
        app_commands.Choice(name="VIP Role", value="vip role"),
        app_commands.Choice(name="Custom Color", value="custom color"),
        app_commands.Choice(name="Profile Badge", value="profile badge")
    ])
    async def buy(self, interaction: discord.Interaction, item: str):
        user_id = str(interaction.user.id)
        items = {
            "vip role": 1000,
            "custom color": 500,
            "profile badge": 250
        }
        
        if item not in items:
            await interaction.response.send_message("Item not found!", ephemeral=True)
            return
            
        balance = await self.db.get_balance(user_id)
        price = items[item]
        
        if balance < price:
            await interaction.response.send_message("Insufficient funds!", ephemeral=True)
            return
            
        await self.db.update_balance(user_id, -price)
        await interaction.response.send_message(f"Successfully purchased {item} for {price} coins!")

    @work.error
    async def work_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.CommandOnCooldown):
            retry_after = int(error.retry_after)
            await interaction.response.send_message(
                f"You're still working! Try again in {retry_after // 60} minutes.",
                ephemeral=True
            )

async def setup(bot):
    await bot.add_cog(Economy(bot))
