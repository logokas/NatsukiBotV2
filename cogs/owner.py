import ast
import traceback

import discord
import requests
from discord.ext import commands
from datetime import datetime, timezone


def insert_returns(body):
    # insert return stmt if the last expression is a expression statement
    if isinstance(body[-1], ast.Expr):
        body[-1] = ast.Return(body[-1].value)
        ast.fix_missing_locations(body[-1])

    # for if statements, we insert returns into the body and the orelse
    if isinstance(body[-1], ast.If):
        insert_returns(body[-1].body)
        insert_returns(body[-1].orelse)

    # for with blocks, again we insert returns into the body
    if isinstance(body[-1], ast.With):
        insert_returns(body[-1].body)

async def nat_admin(ctx):
    if await ctx.bot.is_owner(ctx.author):
        return True
    else:
        return ctx.author.guild_permissions.administrator

def is_admin():
    return commands.check(nat_admin)

async def nat_moderator(ctx):
    if ctx.author.guild_permissions.administrator == True or await ctx.bot.is_owner(ctx.author):
        return True
    else:
        return ctx.author.guild_permissions.manage_guild

def is_moderator():
    return commands.check(nat_moderator)

class OwnerCog(commands.Cog):
    bot: commands.Bot
    
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
        if message.author.id == 626045764149444614:
            return
        bc = self.bot.get_channel(423656208264855563)
        embed = discord.Embed(color=discord.Color(0xeb72a4), description=f"**Message sent by <@{message.author.id}> deleted in <#{message.channel.id}>**\n", timestamp=datetime.utcnow())
        if message.content == "":
            pass
        else:
            embed.add_field(name="**Message**", value=f"{message.content}")
        embed.set_author(name=message.author.name, icon_url=message.author.avatar_url)
        embed.set_footer(text=f"User ID: {message.author.id} • Message ID: {message.id}")
        await bc.send(embed=embed) 

    @commands.Cog.listener()
    async def on_message_edit(self, before: discord.Message, after: discord.Message):
        if before.author.id == 626045764149444614:
            return
        bc = self.bot.get_channel(378127658757783564)
        embed = discord.Embed(color=discord.Color(0xeb72a4), description=f"**Message edited in <#{before.channel.id}>** [Jump to Message](http://discord.com/channels/542010323541032961/{before.channel.id}/{before.id})\n", timestamp=datetime.utcnow())
        if before.content == "" or before.content == None:
            pass
        else:
            embed.add_field(name="**Before**", value=f"{before.content}", inline=False)
            embed.add_field(name="**After**", value=f"{after.content}", inline=False)
            embed.set_author(name=before.author.name, icon_url=before.author.avatar_url)
            embed.set_footer(text=f"User ID: {before.author.id} • Message ID: {before.id}")
            await bc.send(embed=embed) 
        
    @commands.Cog.listener()
    async def on_member_update(self, before: discord.Member, after: discord.Member):
        bc = self.bot.get_channel(423656208264855563)
        if before.id and after.id == 626045764149444614:
            return
        if before.nick == after.nick:
            pass
        else:
            embed = discord.Embed(color=discord.Color(0xeb72a4), description=f"**<@{before.id}> nickname changed**\n", timestamp=datetime.utcnow())
            embed.add_field(name="**Before**", value=f"{before.nick}", inline=False)
            embed.add_field(name="**After**", value=f"{after.nick}", inline=False)
            embed.set_author(name=before.name, icon_url=before.avatar_url)
            embed.set_footer(text=f"User ID: {before.id}")
            await bc.send(embed=embed) 
        if before.roles == after.roles:
            return
        else:
            if len(before.roles) > len(after.roles):
                old_role = next(role for role in before.roles if role not in after.roles)
                embed = discord.Embed(color=discord.Color(0xeb72a4), description=f"**<@{before.id}> was removed from the `{old_role}` role**\n", timestamp=datetime.utcnow())
                embed.set_author(name=before.name, icon_url=before.avatar_url)
                embed.set_footer(text=f"User ID: {before.id}")
                await bc.send(embed=embed)
            else:
                new_role = next(role for role in after.roles if role not in before.roles)
                embed = discord.Embed(color=discord.Color(0xeb72a4), description=f"**<@{before.id}> was given the `{new_role}` role**\n", timestamp=datetime.utcnow())
                embed.set_author(name=before.name, icon_url=before.avatar_url)
                embed.set_footer(text=f"User ID: {before.id}")
                await bc.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        bc = self.bot.get_channel(423656208264855563)
        embed = discord.Embed(color=discord.Color(0x6af77b), description=f"<@{member.id}> {member.name}#{member.discriminator}\n", timestamp=datetime.utcnow())
        embed.set_author(name="Member Joined", icon_url=member.avatar_url)
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(text=f"User ID: {member.id}")
        await bc.send(embed=embed) 

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        bc = self.bot.get_channel(423656208264855563)
        embed = discord.Embed(color=discord.Color(0xdc4a4b), description=f"<@{member.id}> {member.name}#{member.discriminator}\n", timestamp=datetime.utcnow())
        embed.set_author(name="Member Left", icon_url=member.avatar_url)
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(text=f"User ID: {member.id}")
        await bc.send(embed=embed) 

    @commands.Cog.listener()
    async def on_guild_role_create(self, role: discord.Role):
        bc = self.bot.get_channel(423656208264855563)
        embed = discord.Embed(color=discord.Color(0x6af77b), description=f"**Role Created: {role.name}**\n", timestamp=datetime.utcnow())
        embed.set_author(name=f"{role.guild.name}", icon_url=role.guild.icon_url)
        embed.set_footer(text=f"Role ID: {role.id}")
        await bc.send(embed=embed) 

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role: discord.Role):
        bc = self.bot.get_channel(423656208264855563)
        embed = discord.Embed(color=discord.Color(0xdc4a4b), description=f"**Role Deleted: {role.name}**\n", timestamp=datetime.utcnow())
        embed.set_author(name=f"{role.guild.name}", icon_url=role.guild.icon_url)
        embed.set_footer(text=f"Role ID: {role.id}")
        await bc.send(embed=embed) 

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        bc = self.bot.get_channel(423656208264855563)
        embed = discord.Embed(color=discord.Color(0x6af77b), description=f"**Channel Created: #{channel.name}**\n", timestamp=datetime.utcnow())
        embed.set_author(name=f"{channel.guild.name}", icon_url=channel.guild.icon_url)
        embed.set_footer(text=f"Role ID: {channel.id}")
        await bc.send(embed=embed) 

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        bc = self.bot.get_channel(423656208264855563)
        embed = discord.Embed(color=discord.Color(0xdc4a4b), description=f"**Channel Deleted: #{channel.name}**\n", timestamp=datetime.utcnow())
        embed.set_author(name=f"{channel.guild.name}", icon_url=channel.guild.icon_url)
        embed.set_footer(text=f"Role ID: {channel.id}")
        await bc.send(embed=embed) 

    # Hidden means it won't show up on the default help.
    @commands.command(name='load', hidden=True)
    @is_admin()
    # @commands.is_owner()
    async def nat_load(self, ctx, *, cog: str):
        """Command which Loads a Module.
        Remember to use dot path. e.g: cogs.owner"""

        try:
            self.bot.load_extension(cog)
        except Exception as e:
            await ctx.send("```" + "".join(traceback.format_exception(type(e), e, e.__traceback__)) + "```")
        else:
            await ctx.send('**`SUCCESS`**')

    @commands.command(name='unload', hidden=True)
    @is_admin()
    # @commands.is_owner()
    async def nat_unload(self, ctx, *, cog: str):
        """Command which Unloads a Module.
        Remember to use dot path. e.g: cogs.owner"""

        try:
            self.bot.unload_extension(cog)
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`SUCCESS`**')

    @commands.command(name='reload', hidden=True)
    @is_moderator()
    # @commands.is_owner()
    async def nat_reload(self, ctx, *, cog: str):
        """Command which Reloads a Module.
        Remember to use dot path. e.g: cogs.owner"""

        # noinspection PyBroadException
        try:
            self.bot.unload_extension(cog)
            self.bot.load_extension(cog)
        except Exception as e:
            await ctx.send("```" + "".join(traceback.format_exception(type(e), e, e.__traceback__)) + "```")
        else:
            await ctx.send(f'**`SUCCESS`** Reloaded {cog}')

    @commands.command(name='reloadall', hidden=True)
    @is_moderator()
    # @commands.is_owner()
    async def nat_reloadall(self, ctx):
        """Command which Reloads a Module.
        Remember to use dot path. e.g: cogs.owner"""
        extensions = list(self.bot.extensions.keys())
        # noinspection PyBroadException
        for cog in extensions:
            try:
                self.bot.unload_extension(cog)
                self.bot.load_extension(cog)
            except Exception as e:
                await ctx.send("```" + "".join(traceback.format_exception(type(e), e, e.__traceback__)) + "```")
            else:
                await ctx.send(f'**`SUCCESS`** Reloaded {cog}')

    @commands.command(name="playing", hidden=True)
    @is_admin()
    # @commands.is_owner()
    async def pres_playing(self, ctx, *, content):
        await self.bot.change_presence(activity=discord.Game(content))

    @commands.command(name='whois', hidden=True)
    @is_moderator()
    async def who(self, ctx:commands.Context, member: discord.Member = None):
        rolelist = [r.mention for r in member.roles if r != ctx.guild.default_role]
        roles = ", ".join(rolelist)
        embed = discord.Embed(color=discord.Color(0xeb72a4), description=f"{member.mention}", timestamp=datetime.utcnow())
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_author(name=member.name, icon_url=member.avatar_url)
        embed.add_field(name="**Joined**", value=f"{member.joined_at.replace(tzinfo=timezone.utc).astimezone(tz=None).strftime('%a, %b %d, %Y %I:%M %p')}", inline=True)
        embed.add_field(name="**Registered**", value=f"{member.created_at.replace(tzinfo=timezone.utc).astimezone(tz=None).strftime('%a, %b %d, %Y %I:%M %p')}", inline=True)
        embed.add_field(name=f"**Roles [{len(rolelist)}]**", value=f"{roles}", inline=False)
        embed.set_footer(text=f"User ID: {member.id}")
        await ctx.send(embed=embed)

    @commands.command(name="eval", hidden=True)
    @is_admin()
    # @commands.is_owner()
    async def eval_fn(self, ctx, *, cmd):
        """Evaluates input.
        Input is interpreted as newline seperated statements.
        If the last statement is an expression, that is the return value.
        Usable globals:
          - `bot`: the bot instance
          - `discord`: the discord module
          - `commands`: the discord.ext.commands module
          - `ctx`: the invokation context
          - `__import__`: the builtin `__import__` function
        Such that `>eval 1 + 1` gives `2` as the result.
        The following invokation will cause the bot to send the text '9'
        to the channel of invokation and return '3' as the result of evaluating
        >eval ```
        a = 1 + 2
        b = a * 2
        await ctx.send(a + b)
        a
        ```
        """
        fn_name = "_eval_expr"

        cmd = cmd.strip("` ")

        # add a layer of indentation
        cmd = "\n".join(f"    {i}" for i in cmd.splitlines())

        # wrap in async def body
        body = f"async def {fn_name}():\n{cmd}"

        parsed = ast.parse(body)
        body = parsed.body[0].body

        insert_returns(body)

        env = {
            'bot': ctx.bot,
            'discord': discord,
            'commands': commands,
            'ctx': ctx,
            '__import__': __import__
        }
        exec(compile(parsed, filename="<ast>", mode="exec"), env)

        result = (await eval(f"{fn_name}()", env))

        await ctx.send(result)

    @commands.command(name="ip", hidden=True)
    @is_admin()
    # @commands.is_owner()
    async def get_ip(self, ctx):
        await ctx.send(requests.get("https://api.ipify.org").text)


def setup(bot):
    bot.add_cog(OwnerCog(bot))
