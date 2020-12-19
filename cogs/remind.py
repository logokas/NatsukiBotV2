import discord
import re
import attr
import asyncio
import sqlite3
from discord.ext import commands
from datetime import datetime, timedelta, timezone
from sqlitedict import SqliteDict

@attr.s(auto_attribs=True)
class RemindState:
	remindtime: datetime
	guild: int
	context: str

def create_connection(db_file):
	""" 
	create a database connection to the SQLite database
	specified by the db_file
	:param db_file: database file
	:return: Connection object or None
	"""
	conn = None
	conn = sqlite3.connect(db_file)

	return conn

def delete_task(conn, key):
	"""
	Delete a task by task id
	:param conn:  Connection to the SQLite database
	:param id: id of the task
	:return:
	"""
	sql = 'DELETE FROM unnamed WHERE key=?'
	cur = conn.cursor()
	cur.execute(sql, (key,))
	conn.commit()

class RemindCog(commands.Cog):
	'''
	Reminds Staff About Stuff They Must Be
	Reminded of
	'''

	def __init__(self, bot: commands.Bot):
		self.bot = bot
		self.remind = {}
		self.bot.loop.create_task(self.remindchecker())

	@staticmethod
	def parse_time_string(timestr: str) -> int:
		time_units = re.findall(r"\d+[smhdw]", timestr)
		total_time = 0
		for unit in time_units:
			temp = int(unit[:-1])
			if unit[-1] == "m":
				temp = temp * 60
			elif unit[-1] == "h":
				temp = temp * 60 * 60
			elif unit[-1] == "d":
				temp = temp * 60 * 60 * 24
			elif unit[-1] == "w":
				temp = temp * 60 * 60 * 24 * 7
			total_time += temp
		return total_time

	async def add_remind(self, member: discord.Member, time: int, context: str):
		now = datetime.now(timezone.utc)
		remind_time = now + timedelta(seconds=time)
		self.remind[member.id] = RemindState(remindtime=remind_time, guild=member.guild.id, context=context)
		
	@commands.command()
	async def remindme(self, ctx: commands.Context, time: str, *, context: str):
		if ctx.channel.id == 378127658757783564 or ctx.channel.id == 378084541228646400 or ctx.channel.id == 581831181524402207:
			if not re.match(r"\d+[smhdw]", time):
				return await ctx.send("That's not a valid time string. Example: 1h4m30s")
			else:
				await self.add_remind(ctx.author, self.parse_time_string(time), context)
				with SqliteDict('./reminders.sqlite', autocommit=True) as reminddb:
					reminddb[str(ctx.author.id)] = f"{context}"
				embed = discord.Embed(color=discord.Color(0xeb72a4), description=f"{ctx.author.mention}, I will remind you in {time} about this: `{context}` [Jump to Message](http://discord.com/channels/{ctx.guild.id}/{ctx.message.channel.id}/{ctx.message.id})\n")
				await ctx.send(embed=embed)
		else:
			return await ctx.send("You can't use this command here, baka!")
			
	@commands.command(name="forgetall")
	async def remove_remind(self, ctx: commands.Context):
		if ctx.channel.id == 378127658757783564 or ctx.channel.id == 378084541228646400 or ctx.channel.id == 581831181524402207:
			remind_state: RemindState = self.remind.pop(ctx.author.id, None)
			if not remind_state:
				embed = discord.Embed(color=discord.Color(0xdc4a4b), description="You don't have any active reminders set up.")
				await ctx.send(embed=embed)
			conn = create_connection('./reminders.sqlite')
			delete_task(conn, ctx.author.id)
			embed = discord.Embed(color=discord.Color(0xdc4a4b), description=f"{ctx.author.mention}, you no longer have any timed reminders set.")
			await ctx.send(embed=embed)
		else:
			return await ctx.send("You can't use this command here, baka!")

	async def remindchecker(self):
		await self.bot.wait_until_ready()
		while True:
			await self.remind_check()
			await asyncio.sleep(5)

	async def remind_check(self):
		to_remove = []
		for member_id in self.remind:
			if datetime.now(timezone.utc) > self.remind[member_id].remindtime:
				guild: discord.Guild = self.bot.get_guild(self.remind[member_id].guild)
				if not guild.get_member(member_id):
					continue
				else:
					to_remove.append(member_id)
					member: discord.Member = guild.get_member(member_id)

					try:
						with SqliteDict('./reminders.sqlite', autocommit=True) as reminddb:
							embed = discord.Embed(color=discord.Color(0xeb72a4), description=f"This is to notify you that you should do this: `{reminddb[str(member.id)]}`")
							await member.send(embed=embed)
							conn = create_connection('./reminders.sqlite')
							delete_task(conn, member_id)
					except discord.Forbidden:
						pass
		
		for x in to_remove:
			self.remind.pop(x)

def setup(bot):
	bot.add_cog(RemindCog(bot))

def teardown(bot):
	bot.remove_cog("RemindCog")
		