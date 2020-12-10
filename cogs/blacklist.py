## Blacklist.py Guide
## To add new mods/words/whitelist to the ban list, enter the respective TXT file 
# and type the new word to censor. Save and the bot should already see the new term.
## Example:
# exit music
# comedy club
# a brand new day
# abridged

## To add new site bans, enter the site ban TXT file and type the new site to censor.
# Save and the bot should already see the new term. MAKE SURE TO INCLUDE .[domain]
## Example:
# gamejolt.com
# itch.io
# mega.nz

import discord
from discord.ext import commands
import re
from datetime import datetime, timedelta

class BlacklistCog(commands.Cog):

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        '''
        Manages the Censor Mode of Natsu with New Accounts
        and Site/Mod Bans
        '''
        # checks if message is not from NatBot
        if message.author.id == 626045764149444614:
            return

        # grabs the user creation date and adds X days as a end_date
        user_date = message.author.created_at
        end_date = user_date + timedelta(days=20)
        # checks if the sender is a mod on the server

        # checks if the current time is less of the end date of the user
        if datetime.utcnow() < end_date:
            # link protocols to see and filter out
            protocols = ['http', 'https']
            pLength = len(protocols)
            for x in range(pLength):
                # checks if new person message has the key words in protocols
                if protocols[x] in message.content:
                    # NatBot will delete and ask the user to contact a mod to post a link
                    await message.delete()
                    await message.channel.send(f"{message.author.mention}, your link has been removed due to your account age.\nContact a moderator for posting a link.")
        else:
            # loads site bans
            with open("sitebans.txt") as file:
                siteBlacklist = [links.strip().lower() for links in file.readlines()]
                sblLength = len(siteBlacklist)

            # checks if message contains any words in the txt file
            for x in range(sblLength):
                sblRegex = r"(?<!r/)"+siteBlacklist[x]+"\."
                sblMatches = re.finditer(sblRegex, message.content.lower(), re.MULTILINE | re.IGNORECASE)
                for x in enumerate(sblMatches, start=1):
                    # checks if user is not a mod
                    mod = message.author.guild_permissions.kick_members
                    if mod:
                        # NatBot will warn for now about the link
                        await message.channel.send(f"{message.author.mention}, you have posted a blacklisted site.\nPlease refrain from posting links to those in the near future.")
            
            # loads mod bans
            with open("modbans.txt") as file:
                modBlacklist = [names.strip().lower() for names in file.readlines()]
                mblLength = len(modBlacklist)

            # loads common words
            with open("wordfilter.txt") as wordFile:
                wordList = [wordNames.strip().lower() for wordNames in wordFile.readlines()]
                wordLength = len(wordList)

            # loads whitelisted mod words (for mods like EM:R v EM)
            with open("modwhitelist.txt") as wordFile:
                modWhitelist = [wordNames.strip().lower() for wordNames in wordFile.readlines()]
                wblLength = len(modWhitelist)

            # checks if message contains any words in the txt files
            for x in range(mblLength):
                for y in range(wordLength):
                    for z in range(wblLength):
                        wflRegexA = r"("+wordList[y]+" "+modBlacklist[x]+"$|"+wordList[y]+" "+modBlacklist[x]+" (?!"+modWhitelist[z]+"))"
                        wflMatchesA = re.finditer(wflRegexA, message.content.lower(), re.MULTILINE | re.IGNORECASE)
                        for a in enumerate(wflMatchesA, start=1):
                            # checks if user is not a mod
                            mod = message.author.guild_permissions.kick_members
                            if not mod:
                                # NatBot will warn for now about the link
                                await message.channel.send(f"{message.author.mention}, you mentioned obtaining a blacklisted mod or download link to one.\nPlease refrain from posting links to those in the near future.")

def setup(bot):
    bot.add_cog(BlacklistCog(bot))

def teardown(bot):
    bot.remove_cog("BlacklistCog")