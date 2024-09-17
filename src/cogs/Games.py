import discord
from discord.ext import commands
import random


class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("module Games has been loaded. . .")

    @commands.command(aliases=("8ball",))
    async def eight_ball(self, ctx, *arg):
        """simple 8ball implementation

        Args:
            ctx (discord.ext.commands.Context): user that invoked the 8ball command
            *arg: strings that come after the main command, must have a '?' at the end to work
        """
        argument = " ".join(arg)
        if argument[-1] != "?":
            await ctx.send("The message has to be a question")
        else:
            r = random.randint(1, 3)
            if r == 1:
                await ctx.send("yes")
            elif r == 2:
                await ctx.send("no")
            elif r == 3:
                await ctx.send("maybe")


async def setup(bot):
    await bot.add_cog(Games(bot))
