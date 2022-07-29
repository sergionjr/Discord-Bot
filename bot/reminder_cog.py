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

    @commands.command(name="remind", aliases=["alert"], help="test test")

    async def reminder(self, ctx, arg1):
        print("1 arg reminder function", arg1)
        await ctx.send(arg1)

    @commands.command(name="remind", aliases=["alert"], help="test test")
    async def reminder(self, ctx, arg1, arg2, arg3):
        print("3 arg reminder function", arg1, arg2, arg3)

