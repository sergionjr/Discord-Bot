import os
import random
import json
import discord

from discord.ext import commands
from help_cog import help_cog
from music_cog import music_cog
from alert_cog import alert_cog

#f = open('./config.json')
#data = json.load(f)
#TOKEN = data["TOKEN"]
#f.close()
TOKEN = os.environ['TOKEN']

bot = commands.Bot(command_prefix=".")

bot.remove_command("help")

bot.add_cog(help_cog(bot))
bot.add_cog(music_cog(bot))
bot.add_cog(alert_cog(bot))

bot.run(TOKEN)

"""
    Note on Software Versioning:
    [major].[minor].[release].[build]
    
    major: Really a marketing decision. Are you ready to call the version 1.0? Does the company consider this a major version for which customers might have to pay more, or is it an update of the current major version which may be free? Less of an R&D decision and more a product decision.

    minor: Starts from 0 whenever major is incremented. +1 for every version that goes public.
    
    release: Every time you hit a development milestone and release the product, even internally (e.g. to QA), increment this. This is especially important for communication between teams in the organization. Needless to say, never release the same 'release' twice (even internally). Reset to 0 upon minor++ or major++.
    
    build: Can be a SVN revision, I find that works best.
    
    Examples:
    My current chrome: 83.0.4103.61

..source: https://stackoverflow.com/questions/615227/how-to-do-version-numbers
"""