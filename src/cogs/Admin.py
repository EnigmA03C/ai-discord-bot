import discord
from discord.ext import commands

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_ready(self):
        print('module Admin has been loaded. . .')
    
    @commands.Cog.listener('on_command_error')
    async def on_command_error(self, ctx, error):
        """Error Detection for the Cog

        Args:
            ctx (discord.ext.commands.Context): the command context
            error (commands.errors): The Error that was catch'd
        """
        if isinstance(error, commands.errors.BadArgument):
            await ctx.channel.send('I need an integer for that one')
    
    @commands.Cog.listener('on_message')
    async def on_message(self, ctx: commands.Context):
        """filter for slur's and offensive words
        
        WIP

        Args:
            ctx (discord.ext.commands.Context): The message that needs to be scrutinized
        """
        very_bannable_stuff = ()
        
        if ctx.author.id == self.bot.user.id:
            message = str(ctx.content).lower().split()
            for string in message:
                if string in very_bannable_stuff:
                    await ctx.delete()
                    channel = await ctx.author.create_dm()
                    await channel.send('Hey, this is a warning. You sent a message that triggered the filter and might result in a ban. If you think this was a mistake pls DM Enigma')
        else:
            return
    
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
        async for ctx.message in ctx.channel.history(limit=arg+1):
            await ctx.message.delete()
        await ctx.channel.send('Done!')

async def setup(bot):
    await bot.add_cog(Admin(bot=bot))