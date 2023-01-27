import discord
import os
from dotenv import load_dotenv
from datetime import MAXYEAR, MINYEAR, datetime, timedelta
import database

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')


class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.synced = False

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync()
            self.synced = True
        print(f'Logged in as {self.user}.')


intents = discord.Intents.default()
intents.message_content = True
client = MyClient(intents=intents)
tree = discord.app_commands.CommandTree(client)



@tree.command(name = 'create_jam', description = 'Create a new game jam reminder')
@discord.app_commands.describe(
    title = 'Title of the jam (should be unique)',
    theme = 'Theme of the jam',
    duration = 'Length of the jam',
    year = 'What year to remind',
    month = 'What month to remind (1-12)',
    day = 'What day to remind (1-31)',
    hour = 'What hour to remind (0-23)',
    minute = 'What minute to remind (0-59)',
)
async def create_jam(
    interaction: discord.Interaction,
    title: str,
    theme: str,
    duration: str,
    year: int,
    month: int,
    day: int,
    hour: int,
    minute:int,
):
    date = datetime(year, month, day, hour, minute)
    database.add_jam(title, theme, date, duration)
    await interaction.response.send_message(f'{title} with duration {duration} and year {year}')



@tree.command(name = 'timeleft', description = 'Display the remaining time')
@discord.app_commands.describe(
    title = 'Optional title of the jam to show time left. Default is the current jam'
)
async def timeleft(
    interaction: discord.Interaction,
    title: str = None
):
    await interaction.response.send_message(f'Time Left')



@tree.command(name = 'theme', description = 'Display the theme of the jam')
@discord.app_commands.describe(
    title = 'Optional title of the jam to show the theme. Default is the current jam'
)
async def theme(
    interaction: discord.Interaction,
    title: str = None
):
    # Create a checker should not show before the jam
    await interaction.response.send_message(f'Theme')



@tree.command(name = 'list', description = 'Display the list of game jams')
async def list(
    interaction: discord.Interaction,
):
    await interaction.response.send_message(f'List')



@tree.command(name = 'delete', description = 'Delete a game jam')
@discord.app_commands.describe(
    title = 'Title of the jam to delete'
)
async def delete(
    interaction: discord.Interaction,
    title: str
):
    await interaction.response.send_message(f'Delete')



client.run(TOKEN)