import discord

from discord.ext import commands
from youtube_dl import YoutubeDL


class music_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.is_playing = False
        self.is_paused = False

        self.music_queue = []
        self.YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True', 'verbose':'true'}
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn -err_detect ignore_err'}

        self.vc = None

    def search_yt(self, item):
        with YoutubeDL(self.YDL_OPTIONS) as ydl:
            try:
                info = ydl.extract_info("ytsearch:%s" % item, download=False)['entries'][0]
                #print(ydl.extract_info("ytsearch:%s" % item, download=False)['entries'][0])
            except Exception:
                return False
        return {'source': info['formats'][0]['url'], 'title': info['title']}

    def play_next(self):
        if len(self.music_queue) > 0:
            self.is_playing = True

            m_url = self.music_queue[0][0]['source']

            self.music_queue.pop(0)

            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
        else:
            self.is_playing = False




    async def play_music(self, ctx):
        if len(self.music_queue) > 0:
            self.is_playing = True
            m_url = self.music_queue[0][0]['source']

            if (self.vc == None) or not self.vc.is_connected():
                self.vc = await self.music_queue[0][1].connect()

                if self.vc == None:
                    await ctx.send("**:x: Failed to join a voice channel**")
                    return
            else:
                await self.vc.move_to(self.music_queue[0][1])

            self.music_queue.pop(0)

            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
        else:
            self.is_playing = False

    @commands.command(name="embed", aliases=["e"], help="embed test")
    async def embed(self, ctx, *args):
        embed = discord.Embed(title="Sample Embed",
                              url="https://youtube.com",
                              description="Initial sample test for embed",
                              color=discord.Color.magenta())
        embed.set_author(name=ctx.author.display_name,
                         icon_url=ctx.author.avatar_url)

        await ctx.send(embed=embed)

    @commands.command(name="play", aliases=["p", "playing"], help=".play (song) will search (song) on youtube and play the given URL")
    async def play(self, ctx, *args):
        query = " ".join(args)
        #print(query)
        voice_channel = ctx.author.voice.channel
        if voice_channel is None:
            message_notconnected = "**:X: You must be connected to a voice channel!**"
            await ctx.send(message_notconnected)

        elif self.is_paused:
            message_resume = "**:play_pause: Resuming :thumbsup:**"
            self.vc.resume()
            await ctx.send(message_resume)

        else:
            searching_message = "**:musical_note: Searching :mag_right:** `" + query + "`"
            await ctx.send(searching_message)
            song = self.search_yt(query)

            if type(song) == type(True):
                await ctx.send("**Could not download the song. Try a different keyword**")

            else:
                self.music_queue.append([song, voice_channel])
                if self.is_playing == False:
                    message_nowplaying = "**Playing :notes: `" + song['title'] + "` - Now!**"
                    await ctx.send(message_nowplaying)
                    await self.play_music(ctx)

                else:
                    message_addedtoqueue = "** " + str(ctx.author) + " has added the song `" + song['title'] + "` to queue.**"
                    await ctx.send(message_addedtoqueue)

    @commands.command(name="pause", help=".pause (song) will pause the current song being played")
    async def pause(self, ctx, *args):
        if self.is_playing:
            message_pause = "**:pause_button: Current song has been paused.**"
            self.is_playing = False
            self.is_paused = True
            self.vc.pause()
            await ctx.send(message_pause)
        elif self.is_paused:
            message_unpause = "**:play_pause: Current song has been un-paused.**"
            self.is_playing = True
            self.is_paused = False
            self.vc.resume()
            await ctx.send(message_unpause)

    @commands.command(name="resume", aliases=["r"], help="Resumes playing the current song")
    async def resume(self, ctx, *args):
        if self.is_paused:
            message_resume = "**:play_pause: Current song has been resumed.**"
            self.is_playing = True
            self.is_paused = False
            self.vc.resume()
            await ctx.send(message_resume)

    @commands.command(name="skip", aliases=["s"], help="Skips the currently played song")
    async def skip(self, ctx, *args):
        if (self.vc != None) and (self.vc):
            message_skip = "**:fast_forward: Song has been skipped**"
            self.vc.stop()
            await self.play_music(ctx)
            await ctx.send(message_skip)


    @commands.command(name="queue", aliases=["q"], help="Displays all the songs currently in queue")
    async def queue(self, ctx):
        song_list = ""

        for i in range(0, len(self.music_queue)):
            if i > 4:
                break
            song_list += str(i) + ". " + self.music_queue[i][0]['title'] + '\n'
        print(song_list)

        if song_list != "":
            queue_message = "**" + song_list + "**"
            await ctx.send(queue_message)
        else:
            await ctx.send("**:white_square_button: No music currently in the queue.**")

    @commands.command(name="clear", help="Stops the current song and clears the queue")
    async def clear(self, ctx, *args):
        if (self.vc != None) and (self.is_playing):
            self.vc.stop()
        self.music_queue = []
        message_clear = "**:white_check_mark: Music queue has been cleared**"
        await ctx.send(message_clear)

    @commands.command(name="quit", aliases=["stop"], help="Kicks the bot from the voice channel")
    async def leave(self, ctx):
        self.is_playing = False
        self.is_paused = False
        message_quit = "**Disconnected Successfully. Until next time friend :eye: :lips: :eye: **"
        await self.vc.disconnect()
        await ctx.send(message_quit)

