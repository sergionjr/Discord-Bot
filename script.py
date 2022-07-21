import discord
import random

TOKEN = 'OTk5NDIzODg0MTIwMDQ3NzE2.G68QHq.3MREpmimrSM4Tbln9lijLln2UZQSenXs6tw1nc'

client = discord.Client()


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    print(message)
    user_name = str(message.author)
    user_message = str(message.content)
    channel = str(message.channel.name)
    print("New Message:", user_message, "From:", user_name, "At:", message.created_at, "In Channel:", channel)

    if message.author == client.user:
        return
    if user_message.lower() == '.hello':
        await message.channel.send("Hello " + user_name)
        return
    elif user_message.lower() == '.random':
        await message.channel.send("Here is your random number:" + str(random.randint(1, 100)))
        return

client.run(TOKEN)
