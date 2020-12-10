import logging
import sys
import traceback

from discord.ext import commands
from discord.ext.commands import Bot

# cause stupid gateway crap 
import discord
# tells discord we use presence, members, messages, and guild logging intents
intents = discord.Intents(presences=True, members=True, messages=True, guilds=True)

from SECRET import token

initial_extensions = [
    "cogs.owner",
    "cogs.roles",
    "cogs.error",
    "cogs.suggestions",
    "cogs.fun",
    "cogs.gulag",
    "cogs.basics",
    "cogs.mod",
    "cogs.automod",
    "cogs.blacklist",
    "cogs.remind"
]

logging.basicConfig(level=logging.INFO)

bot: Bot = commands.Bot(command_prefix=commands.when_mentioned_or("!"), intents=intents)

if __name__ == '__main__':
    for extension in initial_extensions:
        # noinspection PyBroadException
        try:
            bot.load_extension(extension)
        except Exception:
            print(f'Failed to load extension {extension}.', file=sys.stderr)
            traceback.print_exc()

bot.run(token)
