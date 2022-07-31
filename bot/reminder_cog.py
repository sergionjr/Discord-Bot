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

ref = db.reference('/Reminders (Test)')


dict_entry = """{
"reminderID": "reminderEntry"
}"""

secondary_dict = {
    'rockstar' : 'axel',
    'userID' : '155232'
}

dict_entry = json.loads(dict_entry) #json loads must load a dictionary string. The triple quotes prep it.
ref.push(secondary_dict)

print(ref.get())



class reminder:
    def __init__(self, reminder_id, server_id, user_ids, reminder, private, reminder_date, recurring, recurring_frequency):
        self.reminder_id = reminder_id
        self.server_id = server_id
        self.user_id = user_ids
        self.reminder = reminder
        self.private = private
        self.reminder_date = reminder_date
        self.recurring = recurring #true or false
        self.recurring_frequency = recurring_frequency

class reminder_exo:
    def __init__(self, reminder_id, server_id, user_id):
        self.reminder_id = reminder_id
        self.server_id = server_id
        self.user_id = user_id

    def jsonify(self):
        return {
            "reminder_id": self.reminder_id,
            "server_id": self.server_id,
            "user_id" : self.user_id
        }



class reminder_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.text_channel_text = []

    async def reminder_new(self, ctx, *args):
        await ctx.send("reminder_add")
        await ctx.send("Add a new reminder. Format: .remind new <description> <date (MM-DD-YYYY)> <recurring>")

        return

    async def reminder_modify(self, ctx, *args):
        await ctx.send("reminder_modify")
        return

    async def reminder_delete(self, ctx, *args):
        await ctx.send("reminder_delete")
        return

    async def reminder_delete_all(self, ctx, *args):
        await ctx.send("reminder_delete_all")
        return



    # @commands.Cog.listener()
    # async def on_ready(self):
    #     print()



    @commands.command(name="remind", aliases=["alert"], help="test test")
    async def reminder(self, ctx, *args):
        reminder_operations = {
            'add': self.reminder_new,
            'modify': self.reminder_modify,
            'delete': self.reminder_delete,
            'deleteall': self.reminder_delete_all
        }
        await reminder_operations[args[0]](ctx, args)

        # await ctx.send("argument 1: " + args[0])
        # await ctx.send(args)

    @commands.command(name="reminders", help="push a reminder to firebase")
    async def reminder_push(self, ctx, *args):
        await ctx.send("Args provided:" + " ".join(args))
        reminder_id, server_id, user_id = args
        new_reminder = reminder_exo(reminder_id, server_id, user_id)
        ref.child("testkey1").set(new_reminder.jsonify())
        print(new_reminder)

    @commands.command(name="retrieve", help="filler")
    async def retrieve(self, ctx):
        await ctx.send(str(ref.get()))


    # @commands.Cog.listener()
    # async def on_message(self):
    #     return

