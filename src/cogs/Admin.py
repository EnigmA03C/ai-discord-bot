import discord
from discord.ext import commands


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("module Admin has been loaded. . .")

    @commands.Cog.listener("on_command_error")
    async def on_command_error(self, ctx, error):
        """Error Detection for the Cog

        Args:
            ctx (discord.ext.commands.Context): the command context
            error (commands.errors): The Error that was catch'd
        """
        if isinstance(error, commands.errors.BadArgument):
            await ctx.channel.send("I need an integer for that one")

    @commands.command()
    async def purge(self, ctx, arg: int):
        """Cleans the number of messages specified in the argument of the command

        Good for cleaning up a channel of potential garbage,
        future adaptation will be included in the ban command to
        purge all of the banned users messages (will be an optional argument.)

        Args:
            ctx (discord.ext.commands.Context): the command
            arg (int): number of messages that must be deleted
        """
        async for ctx.message in ctx.channel.history(limit=arg + 1):
            await ctx.message.delete()
        await ctx.channel.send("Done!")


async def setup(bot):
    await bot.add_cog(Admin(bot=bot))
