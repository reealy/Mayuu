import discord
import asyncio
import random

from discord.ext import commands

class Games(commands.Cog):
	def __init__(self,client):
		self.client = client

	@commands.command()
	async def guess(self,ctx):
		while True:
			await ctx.send(ctx.message.author.mention + ' Would you like to play "guess number" game? Write natural number from 1 to 100 or q (quit)')
			randomnum = random.randint(0, 100)
			Attempts = 5
			while Attempts != 0:
				while True:
					guess = await self.client.wait_for('message', timeout=15)
					if guess.content.isdigit():
						break
					elif not guess.content.isdigit():
						await ctx.send(ctx.message.author.mention + ', write natural number from 1 to 100 or q (quit)')
						return
				if int(guess.content) > randomnum:
					await ctx.send('It is bigger')
					Attempts = Attempts - 1
				elif int(guess.content) < randomnum:
					await ctx.send('It is smaller')
					Attempts = Attempts - 1
				elif int(guess.content) == randomnum:
					await ctx.send(f'Ladies and gentlemen, {ctx.author} got it. My number was: {randomnum}')
					break

	@commands.command(aliases=['roll-duel'])
	async def rollduel(self,ctx):
		pass

	@commands.command()
	async def sequencer(self,ctx,*,difficulty="n"):
		print(difficulty)
		pass


def setup(client):
	client.add_cog(Games(client))