import discord
import os, sys
import asyncio
import random
import datetime
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from libs.database import *
from discord.ext import commands

class Utility(commands.Cog):
	def __init__(self,client):
		self.client = client
		self.counter = 0
		self.cache_msg = ''
		self.cache_user = []

	@commands.Cog.listener()
	async def on_ready(self):
		print('speaker loaded.')

	def reset(self):
		self.counter = 0
		self.cache_msg = ''
		self.cache_user = []

	@commands.Cog.listener()
	async def on_message(self,ctx):
		print(f'[{datetime.datetime.now()}] in {ctx.guild.name} <{ctx.author.id}> {ctx.author} : {ctx.content}')
		if (ctx.author==self.client.user or ctx.content.startswith(os.getenv('PREFIX'))):
			return

		words_list=[['mayu'],['cute','cutie'],['hey','hi','hello'],['marry','date'],['do you'],['me'],['luv','love','liek','like']]
		weight = 0

		for i in range(len(words_list)):
			for j in range(len(words_list[i])):
				if words_list[i][j] in ctx.content.lower():
					weight += (i+1)**2
					break
			
		print(weight)
		if weight == 1:
			async with ctx.channel.typing():
				current_date = datetime.datetime.utcnow() - datetime.timedelta(days = random.randint(0, 180))
				message = await ctx.channel.history(limit=500, after=current_date).flatten()
				f_message = []

				for msg in message:
					if (msg.author.id != int(os.getenv('BOT_ID')) and not msg.content.startswith(os.getenv('PREFIX')) and not 'mayu' in msg.content.lower() and msg.mentions == [] and not msg.content.startswith('$')):
						f_message += [msg]

				random_msg = random.choice(f_message)
				await ctx.channel.send(random_msg.content)
				#print("contains mayu")
				
		elif weight == 5 or weight == 14:
			async with ctx.channel.typing():
				data = cute_msg
				msg = random.choice(data)
				await asyncio.sleep(1)
				await ctx.channel.send(msg)
				#print("contains mayu and cute")

		elif weight == 10:
			async with ctx.channel.typing():
				data = greeting_msg
				msg = random.choice(data)
				await asyncio.sleep(1)
				await ctx.channel.send(msg)
				# print("contains maya and hey")

		elif weight == 17 or weight == 21 or weight == 102 or weight == 54 or weight == 50 or weight == 106 or weight == 53:
			async with ctx.channel.typing():
				msg = "\U0001F633 \U0001F633 \U0001F633"
				await asyncio.sleep(1)
				await ctx.channel.send(msg)

		elif weight == 111 or weight == 86 or weight == 62 or weight == 95:
			async with ctx.channel.typing():
				data = emotion_msg
				emotion = random.choice(data)
				msg = f'I feel {emotion} for you'
				await asyncio.sleep(1)
				await ctx.channel.send(msg)

		else:
			if (self.cache_msg == ctx.content and ctx.author.id not in self.cache_user):
				self.counter += 1
				self.cache_msg = ctx.content
				self.cache_user += [ctx.author.id]

				if (self.counter >= 3):
					async with ctx.channel.typing():
						await asyncio.sleep(1)
						await ctx.channel.send(self.cache_msg)
						self.reset()

			else:
				self.counter = 0
				self.cache_msg = ctx.content
				self.cache_user = [ctx.author.id]
	
	'''
	@commands.Cog.listener()
	async def on_raw_reaction_add(self,reaction,user):
		try:
			pass
			#await asyncio.wait_for(eternity(), timeout=60)
		except asyncio.TimeoutError:
			print('timeout!')
	'''

def setup(client):
	client.add_cog(Utility(client))