import discord
import random
import inspirobot
import os, sys
import datetime
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from libs.database import *
from libs.functions import *

from replit import db
from discord.ext import commands

class Fun(commands.Cog):
	def __init__(self,client):
		self.client = client

	@commands.Cog.listener()
	async def on_ready(self):
		print('fun loaded.')

	@commands.command()
	async def roll(self,ctx,*text): 
		try:
			msg = ctx.message.content.split(' ') 
			num = int(msg[i])
		except:
			num = 99 
		
		i = random.randint(0, num)
		author = ctx.message.author.name
		msg = f'**{author}** rolled **{str(i)}** points !'
		await ctx.send(msg)

	@roll.error
	async def roll_error(self,ctx,error):

		error_usage = '!roll (limit)'
		error_example = '!roll 69 the funny number'
		embed = generate_error(error_usage,error_example)
		await ctx.send(embed=embed)

	@commands.command()
	async def emotion(self,ctx,*text):
		data = emotion_msg
		msg = random.choice(data)
		await ctx.send(msg)

	@emotion.error
	async def emotion_error(self,ctx,error):
		
		error_usage = '!emotion'
		error_example = '!emotion How do you feel today Mayuu ?'
		embed = generate_error(error_usage,error_example)
		await ctx.send(embed=embed)

	@commands.command()
	async def inspire(self,ctx):
		quote = inspirobot.generate()	# Generate Image
		quote = quote.url
		await ctx.send(quote)

	@inspire.error
	async def inspire_error(self,ctx,error):

		error_usage = '!inspire'
		error_example = '!inspire'
		embed = generate_error(error_usage,error_example)
		await ctx.send(embed=embed)

	@commands.command()
	async def someone(self,ctx):
		lst = ctx.guild.members
		somebody = random.choice(lst).name
		await ctx.send(somebody)

	@someone.error
	async def someone_error(self,ctx,error):

		error_usage = '!someone'
		error_example = '!someone'
		embed = generate_error(error_usage,error_example)
		await ctx.send(embed=embed)

	@commands.command()
	async def quote(self,ctx,*text):
		current_date = datetime.datetime.utcnow() - datetime.timedelta(days = random.randint(0, 90))
		message = await ctx.channel.history(limit=300, after=current_date).flatten()
		f_message = []
		f_user_message = []
		user = ''

		if (text != ()):
			for part in text[:len(text)-1]:
				user += part+' '
			user += text[len(text)-1]

		for msg in message:
			if (msg.author.id != int(os.getenv('BOT_ID')) and not msg.content.startswith(os.getenv('PREFIX')) and not 'mayu' in msg.content.lower() and msg.mentions == [] and not msg.content.startswith('$')):
				f_message += [msg]
		
		if (user != '' and msg.author != self.client.user):
			for part in f_message:
				if (part.author.name == user):
					f_user_message += [part]

			if (f_user_message != []):
				f_message = f_user_message
			else:
				f_user_message = f_message
		else:
			f_user_message = f_message

		for i in f_user_message:
			print(i.content)
		random_msg = random.choice(f_user_message)

		date = random_msg.created_at.year
		await ctx.send(f'> {random_msg.content}\n- {random_msg.author.name}, {date}')

	@quote.error
	async def quote_error(self,ctx,error):
		print(error)

		error_usage = '!quote <user>'
		error_example = '!quote user'
		embed = generate_error(error_usage,error_example)
		await ctx.send(embed=embed)
	
	@commands.command()
	async def yesno(self, ctx,*msg):
		data = yesno_msg
		msg = random.choice(data)
		await ctx.channel.send(msg)

	@yesno.error
	async def yesno_error(self,ctx,error):

		error_usage = '!yesno <text>'
		error_example = '!yesno Am I an nice person Mayuu ?'
		embed = generate_error(error_usage,error_example)
		await ctx.send(embed=embed)

def setup(client):
	client.add_cog(Fun(client))
