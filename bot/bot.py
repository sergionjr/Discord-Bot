import os
import random
import json
import discord

from discord.ext import commands
from help_cog import help_cog
from music_cog import music_cog

f = open('./config.json')
data = json.load(f)
TOKEN = data["TOKEN"]
f.close()

bot = commands.Bot(command_prefix=".")

bot.remove_command("help")

bot.add_cog(help_cog(bot))
bot.add_cog(music_cog(bot))
bot.add_cog(alert_cog(bot))

bot.run(TOKEN)





# @client.event
# async def on_ready():
#     print('We have logged in as {0.user}'.format(client))
#
#
# @client.event
# async def on_message(message):
#     print(message)
#     user_name = str(message.author)
#     user_message = str(message.content)
#     channel = str(message.channel.name)
#     print("New Message:", user_message, "From:", user_name, "At:", message.created_at, "In Channel:", channel)
#
#     if message.author == client.user:
#         return
#     if user_message.lower() == '.hello':
#         await message.channel.send("Hello " + user_name)
#         return
#     elif user_message.lower() == '.random':
#         await message.channel.send("Here is your random number:" + str(random.randint(1, 100)))
#         return
#
# client.run(TOKEN)
