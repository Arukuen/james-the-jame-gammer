import discord
import os
from dotenv import load_dotenv
from datetime import MAXYEAR, MINYEAR, datetime, timedelta
import database
from reminder import Reminder

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')


class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.reminder = Reminder()
        self.synced = False

    def start_reminder(self, title: str, theme: str, date_end: datetime, duration: str):
        current_guild: discord.Guild = self.get_guild(database.fetch_config('guild_id'))
        current_channel: discord.TextChannel = current_guild.get_channel(database.fetch_config('channel_id'))
        current_role= current_guild.get_role(database.fetch_config('jammer_role_id'))
        self.reminder.set_and_start(title, theme, date_end, database.fetch_config('duration')[duration], current_channel, current_role)

    def time_left(self)->timedelta:
        if database.is_empty():
            return None
        return self.reminder.time_left()
    
    def get_theme(self)->str:
        if database.is_empty():
            return None
        
        current = database.fetch_closest()
        theme = current['theme']
        match current['duration']:
            case '2 days':
                duration = timedelta(days=2)
            case '1 week':
                duration = timedelta(weeks=1)
            case '2 weeks':
                duration = timedelta(weeks=2)

        if current['date_end'] - duration > datetime.now():
            return None
        return theme


    def get_list(self)->list:
        if database.is_empty():
            return None
        return map(lambda jam: jam['title'], database.fetch_all())


    def reset(self):
        database.init()
        self.reminder.force_stop()


    async def on_ready(self):
        # Sync the commands
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync()
            self.synced = True

        # Initialized the database along with the config not exist
        if not database.is_exist():
            database.init()

        if not database.is_empty():
            current = database.fetch_closest()
            self.start_reminder(current['title'], current['theme'], current['date_end'], current['duration'])

        # Setup the current guild and channel
        print(f'Logged in as {self.user}.')


intents = discord.Intents.default()
intents.message_content = True
client = MyClient(intents=intents)
tree = discord.app_commands.CommandTree(client)



@tree.command(name = 'set_config', description = 'Set the configuration for the bot')
@discord.app_commands.describe(
    channel = 'Channel to message',
    jammer = 'Role of jammer'
)
async def set_channel(
    interaction: discord.Interaction,
    channel: discord.TextChannel,
    jammer: discord.Role
):
    database.set_config('guild_id', interaction.guild_id)
    database.set_config('channel_id', channel.id)
    database.set_config('jammer_role_id', jammer.id)
    await interaction.response.send_message(f'Set the channel to `{channel}` and jammer to `{jammer}`')



@tree.command(name = 'create_jam', description = 'Create a new game jam reminder. Overwrites the current jam if it exists')
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
@discord.app_commands.choices(duration = [
    discord.app_commands.Choice(name = '2 days', value = '2 days'),
    discord.app_commands.Choice(name = '1 week', value = '1 week'),
    discord.app_commands.Choice(name = '2 weeks', value = '2 weeks'),
])

async def create_jam(
    interaction: discord.Interaction,
    title: str,
    theme: str,
    duration: discord.app_commands.Choice[str],
    year: int,
    month: int,
    day: int,
    hour: int,
    minute:int,
):
    if database.fetch_config('jammer_role_id') == -1 or database.fetch_config('channel_id') == -1:
        await interaction.response.send_message('Set up the channel and jammer first')
        return 
    try:
        date_end = datetime(year, month, day, hour, minute)
    except:
        await interaction.response.send_message(f'Invalid date input')
        return
    database.add_jam(title, theme, date_end, duration.value)
    client.start_reminder(title, theme, date_end, duration.value)
    await interaction.response.send_message(f'Game Jam `{title}` added with duration `{duration.value}`')



@tree.command(name = 'timeleft', description = 'Display the remaining time')
async def timeleft(
    interaction: discord.Interaction,
):
    delta = client.time_left()
    if delta == None:
        await interaction.response.send_message('No currently running reminder')
        return
    days = delta.days
    hours = delta.seconds // 3600
    minutes = (delta.seconds % 3600) // 60
    await interaction.response.send_message(f'Time Left: `{days} day(s), {hours} hour(s), and {minutes} minute(s)`')



@tree.command(name = 'theme', description = 'Display the theme of the jam')
async def theme(
    interaction: discord.Interaction,
):
    theme = client.get_theme()
    if theme == None:
        await interaction.response.send_message('The theme is not yet viewable')
        return
    await interaction.response.send_message(f'The theme is `{theme}`')



@tree.command(name = 'list', description = 'Display the list of game jams')
async def list(
    interaction: discord.Interaction,
):
    jam_list = client.get_list()
    if jam_list == None:
        await interaction.response.send_message('No currently running reminder')
        return
    list_str = '\n'.join(jam_list)
    await interaction.response.send_message(list_str)



@tree.command(name = 'reset', description = 'Reset the bot')
async def reset(
    interaction: discord.Interaction,
):
    client.reset()
    await interaction.response.send_message(f'Bot resetted')


client.run(TOKEN)