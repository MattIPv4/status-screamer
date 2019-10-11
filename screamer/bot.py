from __future__ import unicode_literals

import logging
import sys
from datetime import datetime
from io import TextIOWrapper

import discord
from discord.errors import NotFound
from discord.ext import tasks

from screamer.config import Config

# Logging
logging.basicConfig(level=logging.ERROR)

# Unbuffered
sys.stdout = TextIOWrapper(sys.stdout.detach(), encoding=sys.stdout.encoding, errors="replace", line_buffering=True)


# The bot
class Screamer(discord.Client):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config = kwargs["config"]
        self.scream_message = None

    @staticmethod
    def timestamp() -> str:
        return datetime.utcnow().isoformat()

    @staticmethod
    def scream_content() -> str:
        return "\N{ZERO WIDTH SPACE}  \N{ANTENNA WITH BARS} Alive at `" + Screamer.timestamp() + "`"

    async def scream_start(self):
        channel = await self.fetch_channel(self.config.channel)
        await channel.send("\N{WHITE HEAVY CHECK MARK} **Started at `" + Screamer.timestamp() + "`**")
        self.scream_message = await channel.send(Screamer.scream_content())

    @tasks.loop(seconds=15)
    async def scream_task(self):
        try:
            if self.scream_message is None:
                await self.scream_start()
            else:
                await self.scream_message.edit(content=Screamer.scream_content())
        except NotFound:
            await self.scream_start()
        except Exception as e:
            print(e)

    async def on_ready(self):
        print("Connected as " + self.user.name + " (" + str(self.user.id) + ")")
        self.scream_task.start()

    def run(self):
        super().run(self.config.token)


if __name__ == "__main__":
    # Create the bot instance
    bot = Screamer(config=Config)
    bot.run()
