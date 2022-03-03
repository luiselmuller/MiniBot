import discord
from discord.ext import commands

class SelfRoleColors(commands.Cog):

  def __init__(self, bot):
    self.bot = bot
  
  #Event example for cogs
  @commands.Cog.listener()
  async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
    """Gives a role based on a reaction emoji."""
    #CHECKS IF IT'S THE REACT MESSAGE
    if 948423403025629196 == payload.message_id:
      member = payload.member
      guild = member.guild
        
      emoji = payload.emoji.name
      if emoji == 'Overwatch':
        role = discord.utils.get(guild.roles, name = 'Overwatch')
      
    await member.add_roles(role)

  @commands.Cog.listener()
  async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
    """Removes a role based on a reaction emoji."""
    #CHECKS IF IT'S THE REACT MESSAGE
    if 948423403025629196 == payload.message_id:
      guild = await(self.bot.fetch_guild(payload.guild_id))
      emoji = payload.emoji.name
      
      if emoji == 'Overwatch':
        role = discord.utils.get(guild.roles, name = 'Overwatch')

      member = await(guild.fetch_member(payload.user_id))
      if member is not None:
        await member.remove_roles(role)
      else:
        print("Member not found")
      


intents = discord.Intents.default()
intents.members = True

def setup(bot):
  bot.add_cog(SelfRoleColors(bot))