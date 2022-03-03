import discord
from discord.ext import commands
from youtube_dl import YoutubeDL

class Music(commands.Cog):
  """Music Commands"""

  def __init__(self, bot):
    self.bot = bot

    self.is_playing = False
    self.is_paused = False

    self.music_queue = []
    self.YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
    self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

    self.vc = None

  #searching youtube for the song
  def search_yt(self, item):
    with YoutubeDL(self.YDL_OPTIONS) as ydl:
      try:
          info = ydl.extract_info("ytsearch:%s" % item, download=False)['entries'][0]
      except Exception:
          return False
    return {'source': info['formats'][0]['url'], 'title':info['title']}

  #playing next song from queue
  def play_next(self):
    if len(self.music_queue) > 0:
      self.is_playing = True

      m_url = self.music_queue[0][0]['source']

      self.music_queue.pop(0)

      self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after = lambda e: self.play_next())
    else:
      self.is_playing = False

  #function to play music
  async def play_music(self,ctx):
    if len(self.music_queue) > 0:
      self.is_playing = True
      m_url = self.music_queue[0][0]['source']

      if self.vc == None or not self.vc.is_connected():
        self.vc = await self.music_queue[0][1].connect()

        if self.vc == None:
          await ctx.send("Could not connect to the voice channel")
          return
      else:
        await self.vc.move_to(self.music_queue[0][1])

      self.music_queue.pop(0)

      self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after = lambda e: self.play_next())

    else:
      self.is_playing = False


      
  @commands.command(
    name="connect",
    brief="Connect the bot to the vc.",
    help="Use $connect to connect the bot to your current voice channel."
  )
  async def connect(self, ctx):
    if ctx.author.voice is None:
      await ctx.send("You're not in a voice channel")
    voice_channel = ctx.author.voice.channel

    if ctx.voice_client is None:
      await voice_channel.connect()
    else:
      await ctx.voice_client.move_to(voice_channel)

  @commands.command(
    name="disconnect",
    brief="Disconnect the bot from the vc.",
    help="Use $disconnect to disconnect the bot from your current voice channel."
  )
  async def disconnect(self, ctx):
    self.is_playing = False
    self.is_paused = False
    if self.vc != None and self.is_playing:
      self.vc.stop()
    self.music_queue = []
    await self.vc.disconnect()

  @commands.command(
    name="play",
    brief="Play a song in the vc.",
    help="Use $play [url] or $play [name song] (without brackets) to play a song in your current voice channel. Only youtube urls are accepted."
  )
  async def play(self, ctx, *args):
    query = " ".join(args)

    voice_channel = ctx.author.voice.channel
    if voice_channel is None:
      await ctx.send("Connect to a voice channel!")
    elif self.is_paused:
      self.vc.resume()
    else:
      song = self.search_yt(query)
      if type(song) == type(True):
        await ctx.send("Could not download the song, incorrect format, try a different keyword")
      else:
        await ctx.send("Song added to queue")
        self.music_queue.append([song, voice_channel])

        if self.is_playing == False:
          await self.play_music(ctx)
    
  @commands.command(
    name="pause",
    brief="Pause the song that's currently playing.",
    help="Use $pause to pause the song that's currently playing in your voice channel."
  )
  async def pause(self, ctx, *args):
    if self.is_playing == True:
      self.is_playing = False
      self.is_paused = True
      self.vc.pause()
    elif self.is_paused:
      self.is_playing = True
      self.is_paused = False
      self.vc.resume()

  @commands.command(
    name="resume",
    brief="Resume the previously paused song.",
    help="Use $resume to resume the song that was previously paused in your current voice channel."
  )
  async def resume(self, ctx, *args):
    if self.is_playing == False:
      self.is_playing = True
      self.is_paused = False
      self.vc.resume()

  @commands.command(
    name="skip",
    brief="Skip the currently playing song.",
    help="Use $skip to skip the song that is currently playing in the voice channel."
  )
  async def skip(self, ctx, *args):
    if self.vc != None and self.vc:
      self.vc.stop()
      await self.play_music(ctx)

  @commands.command(
    name="queue",
    brief="Displays the song queue.",
    help="Use $queue to see all of the songs added to the queue."
  )
  async def queue(self, ctx):
    retval = ""

    for i in range(0, len(self.music_queue)):
      if i > 4: break
      retval += self.music_queue[i][0]['title'] + '\n'

    if retval != "":
      await ctx.send(retval)
    else:
      await ctx.send("No music in the queue.")
    
  @commands.command(
    name="clm",
    brief="Clears the queue and stops the music.",
    help="Use $clm to clear all the music in the queue including the song currently playing."
  )
  async def clm(self, ctx, *args):
    if self.vc != None and self.is_playing:
      self.vc.stop()
    self.music_queue = []
    await ctx.send("Music queue cleared")

    
def setup(bot):
  bot.add_cog(Music(bot))