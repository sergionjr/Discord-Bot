import random

from discord.ext import commands

class eight_ball:
    responses = ["As I see it, yes.", "Ask again later.", "Better not tell you now.", "Cannot predict now.",
                 "Concentrate and ask again.", "Don’t count on it.", "It is certain.", "It is decidedly so.",
                 "Most likely.", "My reply is no.", "My sources say no.", "Outlook not so good.",
                 "Outlook good.","Reply hazy, try again.", "Signs point to yes.", "Very doubtful.",
                 "Without a doubt.", "Yes.", "Yes – definitely.", "You may rely on it."]

class gimmick_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name="magic8ball", aliases=["m8ball", "m8b", "m8"], help="Ask a question to the magic 8 ball.")
    async def magic_eight_ball(self, ctx) -> None:
        message : str = eight_ball.responses[random.randint(0, len(eight_ball.responses) + 1)]
        await ctx.reply(f"{ctx.message.author.mention} {message}")

    @commands.command(name="dice", help="Spin the dice!")
    async def dice(self, ctx) -> None:
        user_roll : int = random.randint(1, 6)
        message : str = f"Your dice roll was a {user_roll}!"
        await ctx.reply(f"{ctx.message.author.mention} {message}")

    @commands.command(name="roll", help="Rolls a number between the specified two numbers (inclusive)")
    async def roll(self, ctx, *args) -> None:

        if len(args) == 1:
            low, high = [1, int(args[0])]
        elif len(args) == 2:
            low, high = [int(args[0]), int(args[1])]
        else:
            raise ValueError(await ctx.reply("You must have a 1 or 2 number range."))
            return

        roll = random.randint(low, high)

        message : str = f"Your roll between ({low} and {high}): {roll}"
        await ctx.reply(f"{ctx.message.author.mention} {message}")
