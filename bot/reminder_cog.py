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





#print("ref:", ref, type(ref))


dict_entry = """{
"reminderID": "reminderEntry"
}"""

secondary_dict = {
    'rockstar' : 'axel',
    'userID' : '155232'
}

dict_entry = json.loads(dict_entry) #json loads must load a dictionary string. The triple quotes prep it.
ref.push(secondary_dict)




class reminder:
    def __init__(self, server_id, user_ids, reminder, reminder_date, recurring, recurring_frequency):

        self.server_id = server_id
        self.user_id = user_ids
        self.reminder = reminder
        self.reminder_date = reminder_date
        self.recurring = recurring #true or false
        self.recurring_frequency = recurring_frequency

class reminder_exo:
    def __init__(self, reminder_id, server_id, user_id):
        self.reminder_id = reminder_id
        self.server_id = server_id
        self.user_id = user_id

    def to_dictionary(self):
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

    async def reminder_clear(self, ctx):
        try:
            ref.child(f"{ctx.author.id}/{ctx.guild.id}").delete()
            await ctx.send(f"{ctx.author.mention}: Your reminders have been cleared successfully.")
        except:
            await ctx.send(f"{ctx.author.mention}: Failed to clear your reminders")
        return



    # @commands.Cog.listener()
    # async def on_ready(self):
    #     print()



    @commands.command(name="reminder", aliases=["alert"], help="test test")
    async def reminder(self, ctx, *args):
        reminder_operations = {
            'add': self.reminder_new,
            'modify': self.reminder_modify,
            'delete': self.reminder_delete,
            'clear': self.reminder_clear
        }
        try:
            await reminder_operations[args[0]](ctx)
        except:
            await ctx.send(f"{ctx.message.author.mention}: Command not recognized.")
       # await ctx.send("argument 1: " + args[0])
       # await ctx.send(args)

    @commands.command(name="reminders", help="push a reminder to firebase")
    async def reminder_push(self, ctx, *args):
        await ctx.send("Args provided:" + " ".join(args)) #simple readback

        reminder_id, server_id, user_id = args #sets them in order of how they are in the args[] structure.
        reminder = reminder_exo(reminder_id, server_id, user_id) #instantiates class

        #Hierarchy: "Reminders (Test)" / "UserID" / "Server ID" /"Reminder Dictionaries"
        #ref.child(<userid>/<reminderid>)
        ref.child(f"{ctx.author.id}/{ctx.guild.id}").push(reminder.to_dictionary())
        #print(reminder)

    @commands.command(name="myreminders", aliases=["myr"], help="filler")
    async def retrieve(self, ctx):
        user_reminders = ref.child(f"{ctx.author.id}/{ctx.guild.id}").get()

        if not user_reminders: #if the dictionary of user reminders is empty
            await ctx.send(f"{ctx.message.author.mention} you do not have any reminders!")
            return

        message = f"Here are your reminders {ctx.message.author.mention}:"
        for key in user_reminders.keys():
            message += f"\n {user_reminders[key]}"
        await ctx.send(message)


        #print(ctx.guild.id)
        #print(reminder_object)
        #print(type(reminder_object))

    # @commands.Cog.listener()
    # async def on_message(self):
    #     return

