import discord
from discord.ext import commands
import re
from datetime import datetime, timedelta

async def is_moderator(ctx):
    if ctx.author.guild_permissions.kick_members or await ctx.bot.is_owner(ctx.author):
        return True
    else:
        return False
        
class BlacklistCog(commands.Cog):

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):

        user_date = message.author.created_at
        end_date = user_date + timedelta(days=20)
        mod = commands.check(is_moderator)

        if datetime.utcnow() < end_date:
            protocols = ['http', 'https']
            pLength = len(protocols)

            for x in range(pLength):
                if protocols[x] in message.content:
                    await message.delete()
                    await message.channel.send(f"{message.author.mention}, your link has been removed due to your account age.\nContact a moderator for posting a link.")
        else:
            with open("sitebans.txt") as file:
                siteBlacklist = [links.strip().lower() for links in file.readlines()]
                sblLength = len(siteBlacklist)

            for x in range(sblLength):
                sblRegex = r"(^"+siteBlacklist[x]+"\.)"
                sblMatches = re.finditer(sblRegex, message.content.lower(), re.MULTILINE | re.IGNORECASE)

                for x in enumerate(sblMatches, start=1):
                    if not mod:
                        await message.delete()
                        await message.channel.send(f"{message.author.mention}, you have posted a blacklisted site.")
            
            with open("modbans.txt") as file:
                modBlacklist = [names.strip().lower() for names in file.readlines()]
                mblLength = len(modBlacklist)

            with open("wordfilter.txt") as wordFile:
                wordList = [wordNames.strip().lower() for wordNames in wordFile.readlines()]
                wordLength = len(wordList)

            for x in range(mblLength):
                for y in range(wordLength):
                    wflRegexA = r"("+wordList[y]+" "+modBlacklist[x]+")"
                    wflMatchesA = re.finditer(wflRegexA, message.content.lower(), re.MULTILINE | re.IGNORECASE)
                    for z in enumerate(wflMatchesA, start=1):
                        if not mod:
                            await message.delete()
                            await message.channel.send(f"{message.author.mention}, you mentioned obtaining a blacklisted mod or download link to one.\nPlease refrain from posting links to those in the near future.")
    
def setup(bot):
    bot.add_cog(BlacklistCog(bot))

def teardown(bot):
    bot.remove_cog("BlacklistCog")