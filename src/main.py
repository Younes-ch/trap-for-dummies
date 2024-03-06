import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

class Bot(commands.Bot):

    def __init__(self):
        super().__init__(command_prefix="!", intents=discord.Intents.all(), activity=discord.Activity(type=discord.ActivityType.listening, name="/help"), help_command=None)
        self.available_commands = ["commands.manage_codes", "commands.help", "commands.clear"]

    async def on_ready(self):
        print(f'Logged in as {self.user.name} - {self.user.id}')
        print('------')
        for guild in self.guilds:
            if guild.id != 1214713063358468256:
                await guild.leave()
        try:
            synced = await self.tree.sync()
            print(f"Synced {len(synced)} command(s):")
            for command in synced:
                print('\033[33m', command.name, '\33[0m-->', command.description)
        except Exception as e:
            print(e)

    async def setup_hook(self):
        for extension in self.available_commands:
            await self.load_extension(extension)
            print(f"Loaded \033[33m{extension.replace('commands.', '')}.py\033[0m")
    
    async def on_guild_join(self, guild):
        if guild.id != 1214713063358468256:
            await guild.leave()


bot = Bot()
load_dotenv()
bot.run(os.getenv('TOKEN'))