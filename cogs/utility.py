import discord
import asyncio
import datetime
import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from libs.functions import *
from discord.ext import commands

class Utility(commands.Cog):
	def __init__(self,client):
		self.client = client
	
	@commands.Cog.listener()
	async def on_ready(self):
		print('utility loaded.')

	@commands.command()
	async def infoserv(self,ctx):
		server = ctx.guild
		icon_url = ctx.guild.icon_url

		servername = server.name
		serverdescription = server.description
		serveruser = server.member_count
		serverowner = server.owner.name
		serverregion = server.region
		try:
			serverinvite = (await server.invites())[0]
		except discord.HTTPException:
			serverinvite = "None"
		
		embed = discord.Embed()
		embed.set_thumbnail(url = icon_url)
		embed.colour = discord.Colour(0x1914FF)
		embed.title = f'__**{servername}**__'
		embed.description = f'*{serverdescription}*'
		embed.add_field(name = "Members : ", value = f'{serveruser}', inline = True)
		embed.add_field(name = "Owner :", value = f'{serverowner}', inline = True)
		embed.add_field(name = "Region", value = f'{serverregion}', inline = True)
		embed.add_field(name = "Invite link", value = f'{serverinvite}', inline = True)
		await ctx.send(embed=embed)

	@infoserv.error
	async def infoserv_error(self,ctx,error):

		error_usage = '!infoserv'
		error_example = '!infoserv'
		embed = generate_error(error_usage,error_example)
		await ctx.send(embed=embed)

	
	@commands.command()
	async def time(self,ctx):
		m = ctx.message.created_at
		t = m.strftime('%d/%m/%Y %H:%M:%S')
		await ctx.send(f'UTC+0: {t}')

	@time.error
	async def time_error(self,ctx,error):

		print(error)
		error_usage = '!time'
		error_example = '!time'
		embed = generate_error(error_usage,error_example)
		await ctx.send(embed=embed)

	@commands.command()
	async def counter(self,ctx,*text):
		msg = ctx.message.content.split(' ')
		if (len(msg) < 2):
			raise ValueError('No argument provided')

		count = len(text)
		await ctx.send(count)

	@counter.error
	async def counter_error(self,ctx,error):

		error_usage = '!counter <text 1> <text 2> <...>'
		error_example = '!counter This will count exactly 6 times'
		embed = generate_error(error_usage,error_example)
		await ctx.send(embed=embed)

	@commands.command(aliases=['reminder','remind-me','timer'])
	async def delay(self, ctx,*text):
		embed = discord.Embed()
		embed.colour = discord.Colour(0x1914FF)
		
		msg = ctx.message.content.split(' ')
		user = ctx.message.author
		msg_id = ctx.message.id
		
		if (len(msg) < 2):
			raise ValueError('No argument provided')

		time_in = msg[1]
		message = ' '.join(msg[2:])

		if "s" in time_in:
			i = time_in.index("s")
			delay_message = f'{time_in[:i]} seconds'
			time_out = [(int(time_in[:i])*1),time_in[i:]]
			print("sec")

		elif "min" in time_in:
			i = time_in.index("min")
			delay_message = f'{time_in[:i]} minutes'
			time_out = [(int(time_in[:i])*1*60),time_in[i:]]
			print("min")

		elif "h" in time_in:
			i = time_in.index("h")
			delay_message = f'{time_in[:i]} hours'
			time_out = [(int(time_in[:i])*1*60*60),time_in[i:]]
			print("hour")

		elif "d" in time_in:
			i = time_in.index("d")
			delay_message = f'{time_in[:i]} days'
			time_out = [(int(time_in[:i])*1*60*60*24),time_in[i:]]
			print("day")

		else:
			raise ValueError('Invalid time argument')
		
		embed.add_field(name = "Message", value = f'{user.mention} {message}', inline = True)
		embed.add_field(name = "Delay", value = f'**{delay_message}**', inline = True)
		embed.set_footer(text="Remove your message to cancel.")

		bot_message = await ctx.send(content="✓ Delayed",embed=embed)
		def check(payload):
			if (payload.message_id == msg_id):
				return True

		try:
			user = await self.client.wait_for('raw_message_delete', timeout=time_out[0], check=check)
		except:
			await ctx.send(f'{user.mention} {message}')
		else:
			await bot_message.delete()

	@delay.error
	async def delay_error(self,ctx,error):

		error_usage = '!delay (time) <message>'
		error_example = '!delay 2h You have cute things to do!'
		embed = generate_error(error_usage,error_example)
		await ctx.send(embed=embed)

	@commands.command()
	async def ping(self,ctx):
		latency = round(self.client.latency*1000)
		await ctx.send(f'Ping : {latency}ms')
		pass

	@delay.error
	async def ping_error(self,ctx,error):

		error_usage = '!ping'
		error_example = '!ping'
		embed = generate_error(error_usage,error_example)
		await ctx.send(embed=embed)

def setup(client):
	client.add_cog(Utility(client))