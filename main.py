import discord
from discord.ext import commands
from pretty_help import PrettyHelp
from discord.ext import tasks
import os
#import random
from webserver import keep_alive
import time

bot = commands.Bot(command_prefix = "$", 
                   help_command=PrettyHelp(
                                          color=discord.Colour.green()))
#bot.help_command = PrettyHelp(navigation=nav, color=discord.Colour.green())


#######################################################################
# Add @is_me() under @bot.command() so that only I can use the command
#######################################################################
def is_me():
    def predicate(ctx):
        return ctx.message.author.id == 220273852339585025
    return commands.check(predicate)

  
#bot start
@bot.event
async def on_ready():
  change_status.start()
  print(f"{bot.user.name} is ready.")

@bot.command()
@is_me()
async def load(ctx, extension):
  bot.load_extension(f'cogs.{extension}')
  await ctx.send(f'Loaded {extension}')
  
@bot.command()
@is_me()
async def unload(ctx, extension):
  bot.unload_extension(f'cogs.{extension}')
  await ctx.send(f'Unloaded {extension}')

@bot.command()
@is_me()
async def reload(ctx, extension):
  bot.unload_extension(f'cogs.{extension}')
  bot.load_extension(f'cogs.{extension}')
  await ctx.send(f'Reloaded {extension}')
  
#loops through all of the files in the cogs folder
#and loads the cogs
for filename in os.listdir('./cogs'):
  if filename.endswith('.py'):
    bot.load_extension(f'cogs.{filename[:-3]}')



'''USE TO SEND UPDATED EMBEDS FOR ROLE CHANGES
@bot.command()
async def embed(ctx):
  #COLOR ROLES EMBED
  em = discord.Embed(title = "Pick your color!", color=0x00FA9A)
  em.add_field(name="Black", value="⚫", inline=True)
  em.add_field(name="Green", value="🟢", inline=True)
  em.add_field(name="Blue", value="🔵", inline=True)
  em.add_field(name="Purple", value="🟣", inline=True)
  em.add_field(name="Orange", value="🟠", inline=True)
  em.add_field(name="Yellow", value="🟡", inline=True)
  em.set_footer(text="Role switching might be a bit slow sometimes.")
  
  msg = await ctx.send(embed=em)
  
  await msg.add_reaction("⚫")
  await msg.add_reaction("🟢")
  await msg.add_reaction("🔵")
  await msg.add_reaction("🟣")
  await msg.add_reaction("🟠")
  await msg.add_reaction("🟡")

  #custom emojis
  overwatch = discord.utils.get(bot.emojis, name="Overwatch")
    
  em2 = discord.Embed(title = "Pick what you want to be pinged for!", color=0x00FA9A)
  em2.add_field(name="Overwatch", value=f'{overwatch}', inline=True)

  msg2 = await ctx.send(embed=em2)
  
  await msg2.add_reaction(f'{overwatch}')
  '''
    
  

#old help commands
"""============ HELP COMMANDS ============
@bot.group(invoke_without_command=True)
async def help(ctx):
  em = discord.Embed(title="Help", description="Use $help <command> for more information on a command", color=ctx.author.color)

  em.add_field(name="Music", value=" 𝘤𝘰𝘯𝘯𝘦𝘤𝘵 - 𝘥𝘪𝘴𝘤𝘰𝘯𝘯𝘦𝘤𝘵 - 𝘦𝘲𝘶𝘢𝘭𝘪𝘻𝘦𝘳 - 𝘭𝘰𝘰𝘱 -  𝘯𝘰𝘸𝘱𝘭𝘢𝘺𝘪𝘯𝘨 - 𝘱𝘢𝘶𝘴𝘦 - 𝘱𝘭𝘢𝘺 - 𝘲𝘶𝘦𝘶𝘦  -  𝘳𝘦𝘴𝘶𝘮𝘦  -  𝘴𝘦𝘦𝘬 - 𝘴𝘬𝘪𝘱 - 𝘷𝘰𝘭𝘶𝘮𝘦")

  await ctx.send(embed=em)

#music help sub commands
@help.command()
async def connect(ctx):
  em = discord.Embed(title="Connect", description="Connects the bot to the users vc", color=ctx.author.color)
  em.add_field(name = "**Syntax**", value = "$connect")

  await ctx.send(embed=em)

@help.command()
async def disconnect(ctx):
  em = discord.Embed(title="Disconnect", description="Disconnects the bot from the users vc", color=ctx.author.color)
  em.add_field(name = "**Syntax**", value = "$disconnect")

  await ctx.send(embed=em)

@help.command()
async def equalizer(ctx):
  em = discord.Embed(title="Equalizer", description="Allows the user to adjust the eq via reactions", color=ctx.author.color)
  em.add_field(name = "**Syntax**", value = "$equalizer")

  await ctx.send(embed=em)

@help.command()
async def loop(ctx):
  em = discord.Embed(title="loop", description="Loops the song that is currently playing", color=ctx.author.color)
  em.add_field(name = "**Syntax**", value = "$loop [none/current/playlist]")

  await ctx.send(embed=em)

@help.command()
async def play(ctx):
  em = discord.Embed(title="Play", description="Connects to users vc and plays the provided song", color=ctx.author.color)
  em.add_field(name = "**Syntax**", value = "$play [url]")

  await ctx.send(embed=em)

@help.command()
async def pause(ctx):
  em = discord.Embed(title="Pause", description="Pauses the current song", color=ctx.author.color)
  em.add_field(name = "**Syntax**", value = "$pause")

  await ctx.send(embed=em)

@help.command()
async def resume(ctx):
  em = discord.Embed(title="Resume", description="Resumes the current song if paused", color=ctx.author.color)
  em.add_field(name = "**Syntax**", value = "$resume")

  await ctx.send(embed=em)

@help.command()
async def seek(ctx):
  em = discord.Embed(title="Seek", description="Seeks the player backwards or forwards", color=ctx.author.color)
  em.add_field(name = "**Syntax**", value = "$seek <seconds> [reverse=False]")

  await ctx.send(embed=em)

@help.command()
async def nowplaying(ctx):
  em = discord.Embed(title="Now Playing", description="Shows the song that is currently playing", color=ctx.author.color)
  em.add_field(name = "**Syntax**", value = "$nowplaying")

  await ctx.send(embed=em)

@help.command()
async def queue(ctx):
  em = discord.Embed(title="Queue", description="Displays all of the songs in queue", color=ctx.author.color)
  em.add_field(name = "**Syntax**", value = "$queue")

  await ctx.send(embed=em)

@help.command()
async def volume(ctx):
  em = discord.Embed(title="Volume", description="Changes the bots playback volume", color=ctx.author.color)
  em.add_field(name = "**Syntax**", value = "$[volume|vol] <vol>")

  await ctx.send(embed=em)

@help.command()
async def skip(ctx):
  em = discord.Embed(title="Skip", description="Skips the currently playing song", color=ctx.author.color)
  em.add_field(name = "**Syntax**", value="$skip")

  await ctx.send(embed = em)


"""


@tasks.loop(seconds=1.5)
async def change_status():
  while True:
    await bot.change_presence(status=discord.Status.do_not_disturb,activity=discord.Streaming(
          name="БФФP БΞΞP",
          url=
          "https://www.youtube.com/watch?v=JUe0GaScPdY&list=PLrV16pC7dwvzQn5z-aIbZj9Gtj3njScyq&index=29"))
  
    time.sleep(.3)
  
    await bot.change_presence(status=discord.Status.do_not_disturb,activity=discord.Streaming(
          name="ФФP БΞΞP Б",
          url=
          "https://www.youtube.com/watch?v=JUe0GaScPdY&list=PLrV16pC7dwvzQn5z-aIbZj9Gtj3njScyq&index=29"))
  
    time.sleep(.3)
  
    await bot.change_presence(status=discord.Status.do_not_disturb,activity=discord.Streaming(
          name="ФP БΞΞP БФ",
          url=
          "https://www.youtube.com/watch?v=JUe0GaScPdY&list=PLrV16pC7dwvzQn5z-aIbZj9Gtj3njScyq&index=29"))
  
    time.sleep(.3)
  
    await bot.change_presence(status=discord.Status.do_not_disturb,activity=discord.Streaming(
          name="P БΞΞP БФФ",
          url=
          "https://www.youtube.com/watch?v=JUe0GaScPdY&list=PLrV16pC7dwvzQn5z-aIbZj9Gtj3njScyq&index=29"))
  
    time.sleep(.3)
  
    await bot.change_presence(status=discord.Status.do_not_disturb,activity=discord.Streaming(
          name=" БΞΞP БФФP",
          url=
          "https://www.youtube.com/watch?v=JUe0GaScPdY&list=PLrV16pC7dwvzQn5z-aIbZj9Gtj3njScyq&index=29"))
  
    time.sleep(.3)
  
    await bot.change_presence(status=discord.Status.do_not_disturb,activity=discord.Streaming(
          name="БΞΞP БФФP",
          url=
          "https://www.youtube.com/watch?v=JUe0GaScPdY&list=PLrV16pC7dwvzQn5z-aIbZj9Gtj3njScyq&index=29"))
  
    time.sleep(.3)
  
    await bot.change_presence(status=discord.Status.do_not_disturb,activity=discord.Streaming(
          name="ΞΞP БФФP Б",
          url=
          "https://www.youtube.com/watch?v=JUe0GaScPdY&list=PLrV16pC7dwvzQn5z-aIbZj9Gtj3njScyq&index=29"))
  
    time.sleep(.3)
  
    await bot.change_presence(status=discord.Status.do_not_disturb,activity=discord.Streaming(
          name="ΞP БФФP БΞ",
          url=
          "https://www.youtube.com/watch?v=JUe0GaScPdY&list=PLrV16pC7dwvzQn5z-aIbZj9Gtj3njScyq&index=29"))
  
    time.sleep(.3)
  
    await bot.change_presence(status=discord.Status.do_not_disturb,activity=discord.Streaming(
          name="P БФФP БΞΞ",
          url=
          "https://www.youtube.com/watch?v=JUe0GaScPdY&list=PLrV16pC7dwvzQn5z-aIbZj9Gtj3njScyq&index=29"))
  
    time.sleep(.3)
  
    await bot.change_presence(status=discord.Status.do_not_disturb,activity=discord.Streaming(
          name=" БФФP БΞΞP",
          url=
          "https://www.youtube.com/watch?v=JUe0GaScPdY&list=PLrV16pC7dwvzQn5z-aIbZj9Gtj3njScyq&index=29"))
  
  time.sleep(.3)

  

#keeping bot alive on the webserver
#keep_alive()


#token
s = os.environ['token']
bot.run(s, bot = True, reconnect = True)