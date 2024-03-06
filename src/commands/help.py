from discord.ext import commands
from discord import app_commands
import discord

cmds = [
    {
        'name': '/check_code',
        'id': '1214724891421581373',
        'args': ['[code]'],
        'description': 'Check if code is correct.'
    },
    {
        'name': '/set_code',
        'id': '1214721614986346576',
        'args': ['[code]'],
        'description': 'Set the code for a channel.'
    },
    {
        'name': '/get_code',
        'id': '1214721614986346577',
        'args': [''],
        'description': 'Get the code of a channel.'
    },
    {
        'name': '/unset_code',
        'id': '1214721614986346578',
        'args': [''],
        'description': 'Unset the code of a channel.'
    },
    {
        'name': '/stop_deleting',
        'id': '1214731707651985479',
        'args': [''],
        'description': 'Stop deleting messages.'
    },
    {
        'name': '/help',
        'id': '1214737997149245471',
        'args': [''],
        'description': 'Get a list of commands.'
    }
]

class Help(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(description="Get a list of commands")
    async def help(self, interaction: discord.Interaction):
        embed = discord.Embed(title='Commands:', color=0x70e68a)
        embed.set_footer(text='Requested by {}'.format(interaction.user.name), icon_url = interaction.user.display_avatar.url)
        for cmd in cmds:
            embed.add_field(
                            name=f'<{cmd["name"]}:{cmd["id"]}>',
                            value=f'`{cmd["name"]} {" | ".join([arg for arg in cmd["args"] if arg])}` : {cmd["description"]}',
                            inline=False
                        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(Help(bot))
        

