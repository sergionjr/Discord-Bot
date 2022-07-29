import discord
import firebase_admin
import json
import os

# External
from discord.ext import commands
from firebase_admin import credentials
from firebase_admin import db

# Internal


serviceAccountKey = json.loads(os.environ['serviceAccountKey'])

cred = credentials.Certificate(serviceAccountKey)

default_app = firebase_admin.initialize_app(cred, {
    'databaseURL': "https://mudbot-68f45-default-rtdb.firebaseio.com"
})

ref = db.reference('/Database reference')

dict_entry = json.loads("{ 'reminderID' : 'reminderEntry'}")
print(dict_entry)
ref.push(dict_entry)

print(ref.get())



class reminder:
    def __init__(self, reminder_id, server_id, user_ids, reminder, private, recurring, recurring_frequency):
        self.reminder_id = reminder_id
        self.server_id = server_id
        self.user_ids = user_ids
        self.reminder = reminder
        self.private = private
        self.recurring = recurring #true or false
        self.recurring_frequency = recurring_frequency



class reminder_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.text_channel_text = []

    @commands.Cog.listener()
    async def on_ready(self):
        print()

    @commands.command(name="remind", aliases=["alert"], help="test test")
    async def reminder(self, ctx, arg1):
        print("1 arg reminder function", arg1)
        await ctx.send(arg1)

    @commands.command(name="remind", aliases=["alert"], help="test test")
    async def reminder(self, ctx, arg1, arg2, arg3):
        print("3 arg reminder function", arg1, arg2, arg3)

