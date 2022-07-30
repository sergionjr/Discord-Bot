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


dict_entry = """{
"reminderID": "reminderEntry"
}"""

secondary_dict = {
    'rockstar' : 'axel'
    'userID'
}

dict_entry = json.loads(dict_entry) #json loads must load a dictionary string. The triple quotes prep it.
ref.push(secondary_dict)

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

    async def reminder_add(self, ctx):
        await ctx.send("reminder_add")
        return

    async def reminder_modify(self, ctx):
        await ctx.send("reminder_modify")
        return

    async def reminder_delete(self, ctx):
        await ctx.send("reminder_delete")
        return

    async def reminder_delete_all(self, ctx):
        await ctx.send("reminder_delete_all")
        return



    # @commands.Cog.listener()
    # async def on_ready(self):
    #     print()



    @commands.command(name="remind", aliases=["alert"], help="test test")
    async def reminder(self, ctx, *args):
        reminder_operations = {
            'add': self.reminder_add,
            'modify': self.reminder_modify,
            'delete': self.reminder_delete,
            'deleteall': self.reminder_delete_all
        }
        await reminder_operations[args[0]](ctx)

        # await ctx.send("argument 1: " + args[0])
        # await ctx.send(args)

    @commands.command(name="reminders", help="push a reminder to firebase")
    async def reminder_push(self, ctx, *args):
        await ctx.send("Args provided:" + " ".join(args))
        print(args)

    @commands.command(name="retrieve", help="filler")
    async def retrieve(self, ctx):
        await ctx.send(str(ref.get()))


    # @commands.Cog.listener()
    # async def on_message(self):
    #     return

