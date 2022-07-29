import discord
from discord.ext import commands


class help_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.version = '(1.1)'
        self.text_channels = []
        self.help_message = """    
```
General commands:
.help - displays all the available commands
.play (or .p) <keywords> - finds the song on youtube and plays it in current channel
.queue (or .q)  - displays the current music queue
.skip - skips the current song being played
.clear - stops the music and clears the queue
.quit (or .stop) - disconnects the bot from the voice channel
.pause - pauses the current song being played or resumes if already paused
.resume - resumes playing the current song                  
```
"""



    @commands.Cog.listener()
    async def on_ready(self):
        for guild in self.bot.guilds:
            for channel in guild.text_channels:
                self.text_channels.append(channel)

        #await self.send_to_first("Mud Cookie is **LIVE!!** " + self.version + self.help_message)

    async def send_to_first(self, msg):
        primary_channel = self.text_channels[0]
        await primary_channel.send(msg)

    @commands.command(name="help", help="Displays all of the available bot commands")
    async def help(self, ctx):
        await ctx.send(self.help_message)


