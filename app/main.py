import discord
from discord import app_commands
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

class EconomyBot(commands.Bot):
    def __init__(self):
        # Removed command_prefix since we're only using slash commands
        super().__init__(command_prefix=None, intents=intents)
        self.synced = False

    async def setup_hook(self):
        for filename in os.listdir("./app/cogs"):
            if filename.endswith(".py"):
                await self.load_extension(f"app.cogs.{filename[:-3]}")
        
        if not self.synced:
            await self.tree.sync()
            self.synced = True
            print("Slash commands synced!")

    async def on_ready(self):
        print(f"Logged in as {self.user.name} ({self.user.id})")

bot = EconomyBot()
bot.run(os.getenv("DISCORD_TOKEN"))
