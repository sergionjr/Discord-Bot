# 🤖 MudBot: A Multi-Purpose Discord Bot (1.2.0)

MudBot was created primarily to be an assistant to my own discord needs. Discord music bots typically have inconvenient command syntaxes (p!play, p!, ;;play),
so mudbot has aggregated the most simplistic features from the best bots into itself. Without a paywall separating the best bitrate, MudBot streams at the best quality,
minimizes spam in your server, and is regularly updated to be the simple jack-of-all-trades that we cannot find.

### 🛠Current & Planned Features

- [X] Music Cog (Using FFMPEG & YoutubeDL)

- [X] Help Cog 

- [X] Reminders Cog (Create a reminder, recurring reminder)

- [ ] Greetings Cog (User join, User level, User ranking)

- [ ] Gimmicks Cog (Roll the die, play a game)

### 📃Current Commands
```
.help - displays all the available commands

.play (or .p) <keywords> - finds the song on youtube and plays it in current channel

.queue (or .q)  - displays the current music queue

.skip - skips the current song being played

.clear - stops the music and clears the queue

.quit (or .stop) - disconnects the bot from the voice channel

.pause - pauses the current song being played or resumes if already paused

.resume - resumes playing the current song                  
```

### 🏃‍♂️How to run
Clone repository and install the required dependencies

`pip install PyNaCl`

`pip install ffmpeg-python`

`pip install youtube_dl`

`pip install discord.py`


Then, plug in your bot token key in `TOKEN = <key>` in `bot.py`
and run the `bot.py` script.


