from discord.ext import commands
from discord import app_commands
import discord

class ManageCodes(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.codes: dict[int, str] = {}
        self.code_found: dict[int, bool] = {}

    @commands.Cog.listener()
    async def on_ready(self):
        for guild in self.bot.guilds:
            for channel in guild.text_channels:
                self.codes[channel.id] = ""
                self.code_found[channel.id] = False

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        self.codes[channel.id] = ""
        self.code_found[channel.id] = False

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        del self.codes[channel.id]
        del self.code_found[channel.id]

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if self.code_found[message.channel.id]:
            await message.delete()

    @app_commands.command(description="Check if the code is correct")
    @app_commands.describe(code="Check if code is correct")
    async def check_code(self, interaction: discord.Interaction, code: str):
        if self.codes[interaction.channel_id] == code:
            await interaction.response.send_message(f"✅ **Code has been found: ||{code}||**")
            self.code_found[interaction.channel_id] = True
        else:
            await interaction.response.send_message(f"❌ **Code is incorrect**", ephemeral=True)

    @app_commands.command(description="Set the code for the channel")
    @app_commands.describe(code="Set the code for this channel")
    @app_commands.checks.has_role(1214714169757147236)
    async def set_code(self, interaction: discord.Interaction, code: str):
        self.codes[interaction.channel_id] = code
        await interaction.response.send_message(f"✅ **Code for this channel has been set to ||{code}||**", ephemeral=True)
    
    @app_commands.command(description="Get the code for the channel")
    @app_commands.checks.has_role(1214714169757147236)
    async def get_code(self, interaction: discord.Interaction):
        if self.codes[interaction.channel_id] == "":
            await interaction.response.send_message(f"⛔ **Code for this channel is not set yet.**", ephemeral=True)
        else:
            await interaction.response.send_message(f"🔒 **Code for this channel is ||{self.codes[interaction.channel_id]}||**", ephemeral=True)

    @app_commands.command(description="Unset the code for the channel")
    @app_commands.checks.has_role(1214714169757147236)
    async def unset_code(self, interaction: discord.Interaction):
        self.codes[interaction.channel_id] = ""
        await interaction.response.send_message(f"⛔ **Code for this channel has been unset.**", ephemeral=True)

    @app_commands.command(description="Stop deleting messages")
    @app_commands.checks.has_role(1214714169757147236)
    async def stop_deleting(self, interaction: discord.Interaction):
        self.code_found[interaction.channel_id] = False
        await interaction.response.send_message(f"✅ **Code deletion has been stopped.**", ephemeral=True)

    @set_code.error
    @get_code.error
    @unset_code.error
    async def on_error(self, interaction: discord.Interaction, error: Exception):
        if isinstance(error, app_commands.MissingRole):
            embed = discord.Embed(
                title="Permission Error",
                description=":no_entry: - You are missing the required permissions to run this command!",
                color=0xCA3B3B,
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            embed = discord.Embed(
                description=":no_entry: An error occured while executing this command. Please try again later.",
                color=0xCA3B3B,
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(ManageCodes(bot))


    