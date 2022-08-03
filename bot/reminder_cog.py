import discord
import firebase_admin
import json
import os
import datetime

# External
from discord.ext import commands
from discord.ext import tasks
from firebase_admin import credentials
from firebase_admin import db
from datetime import date

serviceAccountKey = json.loads(os.environ['serviceAccountKey'])

cred = credentials.Certificate(serviceAccountKey)

default_app = firebase_admin.initialize_app(cred, {
    'databaseURL': os.environ['databaseURL']
})

ref = db.reference('/Reminders (Test)')


class reminder:

    def __init__(self, description, date, created_on, recurring, recurring_frequency):
        self.description = description
        self.date = date
        self.created_on = created_on
        self.recurring = recurring #true or false
        self.recurring_frequency = recurring_frequency

    def to_dictionary(self):
        return {
            "description": self.description,
            "date" : str(self.date),
            "created_on": str(self.created_on),
            "recurring": self.recurring,
            "recurring_frequency" : self.recurring_frequency
        }


class datetime_helper:

    weekdays = {'monday': 0,
                'tuesday': 1,
                'wednesday': 2,
                'thursday': 3,
                'friday': 4,
                'saturday': 5,
                'sunday': 6}

    def next_weekday(self, d, weekday):
        days_ahead = weekday - d.weekday()
        if days_ahead <= 0:
            days_ahead += 7
        return d + datetime.timedelta(days_ahead)


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

    async def reminder_delete(self, ctx, args):
        reminder_id = args[1]
        try:
            ref.child(f"{ctx.guild.name}:{ctx.guild.id}/{ctx.author.name}:{ctx.author.id}/{reminder_id}").delete()
            await ctx.send(f"{ctx.author.mention}: Your reminder {reminder_id} has been removed successfully.")
        except:
            await ctx.send(f"{ctx.author.mention}: Failed to delete your reminder.")
        return

    async def reminder_clear(self, ctx, args):
        try:
            ref.child(f"{ctx.guild.name}:{ctx.guild.id}/{ctx.author.name}:{ctx.author.id}").delete()
            await ctx.send(f"{ctx.author.mention}: Your reminders have been cleared successfully.")
        except:
            await ctx.send(f"{ctx.author.mention}: Failed to clear your reminders.")
        return

    @commands.command(name="reminder", aliases=["alert"], help=".reminder delete [reminderid] - deletes a reminder with id = reminderid\n .reminder clear - deletes all of your reminders on this server")
    async def reminder(self, ctx, *args):
        reminder_operations = {
            'add': self.reminder_new,
            'modify': self.reminder_modify,
            'delete': self.reminder_delete,
            'clear': self.reminder_clear
        }
        #print(reminder_operations['delete'](ctx, args))
        try:
            #print(reminder_operations[args[0]])
            await reminder_operations[args[0]](ctx, args)
        except:
            await ctx.send(f"{ctx.message.author.mention}: Command not recognized.")

    # @commands.command(name="reminders", help="push a reminder to firebase")
    # async def reminder_push(self, ctx, *args):
    #     await ctx.send("Args provided:" + " ".join(args)) #simple readback
    #     reminder_id, server_id, user_id = args #sets them in order of how they are in the args[] structure.
    #    # reminder = reminder_exo(reminder_id, server_id, user_id) #instantiates class
    #
    #     #Hierarchy: "Reminders (Test)" / "ServerName:ServerID" / "UserName:UserID" /"Reminder Dictionaries"
    #     #ref.child(f"{ctx.guild.name}:{ctx.guild.id}/{ctx.author.name}:{ctx.author.id}").push(reminder.to_dictionary())
    #     return

    @commands.command(name="remindme", help="Reminds user once at a specified date")
    async def remindme(self, ctx, *args):
        if len(args) < 2:
            await ctx.send(f"{ctx.author.mention} ```"
                       f" .remindme [MM-DD or MM/DD] [description] \n"
                       f" .remindme [weekday] [description] \n"
                       f" .remindme [tomorrow] [description]```")
            return

        reminder_date = args[0].lower()  # lowercases the date in case it uses weekday or tomorrow
        description = " ".join(args[1:])

        dth = datetime_helper

        #datetime processing
        try:
            if len(reminder_date) == 5 or len(reminder_date) == 4: #if the date argument is MM-DD, MM/DD, 0M-DD, 0M/DD

                month, day = reminder_date.replace('-', ' ').replace('/', ' ').split()
                month, day = int(month), int(day)
                year = datetime.date.today().year
                #converting them all to ints

                reminder_date = datetime.date(year, month, day)

            elif reminder_date == 'tomorrow':
                reminder_date = datetime.date.today() + datetime.timedelta(days=1)
            else:
                weekday_value = dth.weekdays[reminder_date]
                reminder_date = dth.next_weekday(date.today(), weekday_value)

        except:
            await ctx.send(f"{ctx.author.mention} unrecognized date format")
            return


        r = reminder(
            description=description,
            date=reminder_date,
            created_on=datetime.date.today(),
            recurring=False,
            recurring_frequency='none')


        ref.child(f"{ctx.guild.name}:{ctx.guild.id}/{ctx.author.name}:{ctx.author.id}").push(r.to_dictionary())
        await ctx.send(f"{ctx.author.mention} You will be reminded {reminder_date} to '{description}'")


        # date = {
        #     'tomorrow': (datetime.date.today() + datetime.timedelta(days=1))
        #
        # }[reminder_date]



        #################### datetime processing ^ ############################





    @commands.command(name="myreminders", aliases=["myr"], help="filler")
    async def retrieve(self, ctx):
        user_reminders = ref.child(f"{ctx.guild.name}:{ctx.guild.id}/{ctx.author.name}:{ctx.author.id}").get()

        # sorted_keys uses an inline function to return a list of the keys ordered by the nested {'date':'value'} key:value pair in each dictionary.
        try:
            sorted_keys = sorted(user_reminders, key=lambda x: (user_reminders[x]['date']))
        except:
            await ctx.send(f"{ctx.message.author.mention} you do not have any reminders!")
            return

        message = f"Here are your reminders in this server {ctx.message.author.mention}: (Date | Description | Reminder ID)"
        for key in sorted_keys:
            month_day = user_reminders[key]['date'][5:] # 'MM-DD' extracted from 'YYYY-MM-DD'
            description = (user_reminders[key]['description'])

            message += f"\n {month_day} | '{description}' | {key}"

        await ctx.send(message)

    @commands.command(name="populate", aliases=["pop"], help="filler")
    async def populate(self, ctx):
        reminder_1 = reminder(description = "New league prime capsule",
                              date = date(2022, 8, 30),
                              created_on = datetime.date.today(),
                              recurring = True,
                              recurring_frequency = 'monthly')

        reminder_2 = reminder(description = "Groceries",
                              date = datetime.date(2022, 8, 2),
                              created_on = datetime.date.today(),
                              recurring = False,
                              recurring_frequency = 'none')

        reminder_3 = reminder(description = "Take the chicken out of the oven",
                              date = date(2022, 9, 5),
                              created_on = datetime.date.today(),
                              recurring = True,
                              recurring_frequency = 'weekly')
        reminder_arr = [reminder_1, reminder_2, reminder_3]

        for rem in reminder_arr:
            ref.child(f"{ctx.guild.name}:{ctx.guild.id}/{ctx.author.name}:{ctx.author.id}").push(rem.to_dictionary())

        return

    @tasks.loop(hours=12)
    async def check_for_reminders(self):
       # reminders_list = ref.child(f"{ctx.guild.name}:{ctx.guild.id}/{ctx.author.name}:{ctx.author.id}").get()

        for server in self.bot.guilds:
            #reminders for that server
            server_reminders = ref.child(f"{server.name}:{server.id}").get()

            for user_userid in server_reminders:
                #reminders for the users who have reminders in that server
                user, user_id = user_userid.split(":")

                user_reminders = ref.child(f"{server.name}:{server.id}/{user}:{user_id}").get()

                for key in user_reminders:

                    if user_reminders[key]['date'] == str(date.today()):
                        try:
                            user_entity = await self.bot.fetch_user(int(user_id)) #returns a discord.Member object
                            await server.text_channels[0].send(f"{user_entity.mention} REMINDER: '{user_reminders[key]['description']}'")

                            try:
                                ref.child(f"{server.name}:{server.id}/{user}:{user_id}/{key}").delete()
                            except Exception as Argument:
                                await server.text_channels[0].send("Succesfully reminded user, but failed to delete the reminder afterwards ")


                        except Exception as Argument:
                            await server.text_channels[0].send(f"Error ocurred in trying to mention {user}:{user_id}")


    @commands.Cog.listener()
    async def on_ready(self):
        self.check_for_reminders.start()
