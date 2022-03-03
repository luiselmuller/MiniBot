import discord
from discord.ext import commands

class SelfRoleColors(commands.Cog):

  def __init__(self, bot):
    self.bot = bot
    
    #emoji_to_role = {
    #  discord.PartialEmoji(name='⚫'): 948022815498588170,
    #  discord.PartialEmoji(name='🟢'): 948022389004980294,
    #  discord.PartialEmoji(name='🔵'): 948022449386168330,
    #  discord.PartialEmoji(name='🟣'): 948022522014736384,
    #  discord.PartialEmoji(name='🟠'): 948022598829228052,
    #  discord.PartialEmoji(name='🟡'): 948024077820514304,
    #  discord.PartialEmoji(name=':Overwatch:', 
    #                       id=948370814795927593): 948024077820514304
    #}
 
  
  #Event example for cogs
  @commands.Cog.listener()
  async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
    """Gives a role based on a reaction emoji."""
    #CHECKS IF IT'S THE REACT MESSAGE
    if 948423394548924456 == payload.message_id:
      member = payload.member
      guild = member.guild

      emoji = payload.emoji.name
      if emoji == '⚫':
        role = discord.utils.get(guild.roles, name = 'Black')
      elif emoji == '🟢':
        role = discord.utils.get(guild.roles, name = 'Green')
      elif emoji == '🔵':
        role = discord.utils.get(guild.roles, name = 'Blue')
      elif emoji == '🟣':
        role = discord.utils.get(guild.roles, name = 'Purple')
      elif emoji == '🟠':
        role = discord.utils.get(guild.roles, name = 'Orange')
      elif emoji == '🟡':
        role = discord.utils.get(guild.roles, name = 'Yellow')

    await member.add_roles(role)

  @commands.Cog.listener()
  async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
    """Removes a role based on a reaction emoji."""
    #CHECKS IF IT'S THE REACT MESSAGE
    if 948423394548924456 == payload.message_id:
      guild = await(self.bot.fetch_guild(payload.guild_id))
      emoji = payload.emoji.name
      
      if emoji == '⚫':
        role = discord.utils.get(guild.roles, name = 'Black')
      elif emoji == '🟢':
        role = discord.utils.get(guild.roles, name = 'Green')
      elif emoji == '🔵':
        role = discord.utils.get(guild.roles, name = 'Blue')
      elif emoji == '🟣':
        role = discord.utils.get(guild.roles, name = 'Purple')
      elif emoji == '🟠':
        role = discord.utils.get(guild.roles, name = 'Orange')
      elif emoji == '🟡':
        role = discord.utils.get(guild.roles, name = 'Yellow')

      member = await(guild.fetch_member(payload.user_id))
      if member is not None:
        await member.remove_roles(role)
      else:
        print("Member not found")
      



intents = discord.Intents.default()
intents.members = True

def setup(bot):
  bot.add_cog(SelfRoleColors(bot))