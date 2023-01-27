import discord
import os
from dotenv import load_dotenv
from datetime import MAXYEAR, MINYEAR, datetime, timedelta
import database

load_dotenv()
# Discord token goes here
TOKEN = os.getenv('DISCORD_TOKEN')
PERMITTED_ROLE_ID = int(os.getenv('PERMITTED_ROLE_ID'))


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



client.run(TOKEN)