import discord
from discord.ext import commands

class reminder:
    def __init__(self, reminder_id, server_id, user_ids, reminder, private, recurring):
        self.reminder_id = reminder_id
        self.server_id = server_id
        self.user_ids = user_ids
        self.reminder = reminder
        self.private = private
        self.recurring = recurring #true or false
        self.recurring_frequency



class reminder_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.text_channel_text = []

    @commands.command(name="remind", aliases=["e"], help="embed test")
    async def reminder(self, ctx):
        return
