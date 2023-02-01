from datetime import datetime, timedelta
from discord.ext import tasks
import discord

class Reminder:
    def __init__(self) -> None:
        self.reminder_date: datetime = None
        self.index = 0
        self.message = None


    def callback(self):
        if self.index >= len(self.intervals):
            print('Done')
            return
        
        delta = timedelta(hours=self.intervals[self.index])
        self.reminder_date = self.date_end - delta
        days_left = delta.days
        hours_left = delta.seconds // 3600

        if self.reminder_date <= datetime.now():
            print('Skip')
            self.index += 1
            self.callback()
            return

        self.message = f"Time Check: `{days_left} day(s) and {hours_left} hour(s)` left before the jam ends"
        print(self.intervals[self.index])
        
        # Start the reminder
        if not self.task.is_running():
            self.task.start()
        else:
            self.task.restart()

        self.index += 1


    def set_and_start(self, title: str, theme: str, date_end: datetime, intervals: list, channel: discord.TextChannel, role: discord.Role):
        # Set the reminder
        self.index = 0
        self.title = title
        self.theme = theme
        self.date_end = date_end
        self.intervals = sorted(intervals, reverse=True)
        self.channel = channel
        self.role = role
        # Start the reminder
        self.callback()


    def time_left(self)->timedelta:
        return self.date_end - datetime.now()


    def force_stop(self):
        if self.task.is_running():
            self.task.cancel()


    @tasks.loop(seconds=5)
    async def task(self):
        # For debugging only
        print(self.reminder_date - datetime.now())
        if datetime.now() >= self.reminder_date:
            print('Reminder done')
            await self.channel.send(f'{self.message} {self.role.mention}', allowed_mentions=discord.AllowedMentions(everyone=True))
            self.task.cancel()
            self.callback()
