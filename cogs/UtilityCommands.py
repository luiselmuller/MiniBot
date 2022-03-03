import discord
from discord.ext import commands

class UtilityCommands(commands.Cog):

  def __init__(self, bot):
    self.bot = bot
    
  #command example for cogs
  @commands.command()
  @commands.has_permissions(manage_messages=True)
  async def clear(self, ctx, amount = 5):
    await ctx.channel.purge(limit=amount+1)
    
def setup(bot):
  bot.add_cog(UtilityCommands(bot))