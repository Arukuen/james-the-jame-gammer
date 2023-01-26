import discord
import os
from dotenv import load_dotenv

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


@tree.command(name = 'add', description = 'Add a reminder')
@discord.app_commands.describe(
    title = 'Title of the event (should be unique)',
)
async def add_reminder(
    interaction: discord.Interaction,
    title: str
):
    await interaction.response.send_message(f'{title}')



client.run(TOKEN)