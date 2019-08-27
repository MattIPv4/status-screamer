from __future__ import unicode_literals

import asyncio
import logging
import sys
from datetime import datetime
from io import TextIOWrapper

import discord

from screamer.config import Config

# Logging
logging.basicConfig(level=logging.ERROR)

# Unbuffered
sys.stdout = TextIOWrapper(sys.stdout.detach(), encoding=sys.stdout.encoding, errors="replace", line_buffering=True)


# Timestamp string
def timestamp() -> str:
    return datetime.utcnow().isoformat()


# Message content
def content() -> str:
    return "\N{ZERO WIDTH SPACE}  \N{ANTENNA WITH BARS} Alive at `" + timestamp() + "`"


# The bot
class Screamer(discord.Client):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config = kwargs["config"]
        self.message = None

    async def started(self):
        channel = await self.fetch_channel(self.config.channel)
        await channel.send("\N{WHITE HEAVY CHECK MARK} **Started at `" + timestamp() + "`**")
        self.message = await channel.send(content())

    async def screamer(self):
        while True:
            try:
                if self.message is None:
                    await self.started()
                else:
                    await self.message.edit(content=content())
            except Exception as e:
                print(e)
            await asyncio.sleep(15)

    async def on_ready(self):
        print("Connected as " + self.user.name + " (" + str(self.user.id) + ")")

        self.loop.create_task(self.screamer())

    def run(self):
        super().run(self.config.token)


if __name__ == "__main__":
    # Create the bot instance
    bot = Screamer(config=Config)
    bot.run()
