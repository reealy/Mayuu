import discord
import asyncio
import random

from discord.ext import commands

class Games(commands.Cog):
	def __init__(self,client):
		self.client = client

	@commands.command()
	async def guess(self,ctx,*,difficulty="e"):
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
	async def rollduel(self,ctx,tag):
		pass

	@commands.command()
	async def sequencer(self,ctx,*,difficulty="n"):
		def check_diff(difficulty):
			if difficulty == "number" or difficulty == "n":
				lettres = ['0','1','2','3','4','5','6','7','8','9']
			elif difficulty == "taiko" or difficulty == "t":
				lettres = ['d','k']
			elif difficulty == "alphabet" or difficulty == "letter" or difficulty == "l":
				lettres = ['a','b','c','d','e','f','g','h','i','j','k','m','n','o','p','q','r','s','t','u','w','x','y','z']
			else:
				raise ValueError('Invalid mode')
			return lettres

		def give_letter(lettres,lvl):
			answer = ''
			for i in range(lvl):
				answer += random.choice(lettres)
			return answer

		def create_embed(answer):
			embed = discord.Embed()
			embed.colour = discord.Colour(0x1914FF)
			embed.description = answer
			embed.add_field(name = "Levels :", value = f'Level **1**', inline = True)
			embed.add_field(name = "Answers :", value = ' ', inline = True)
			return embed

		def censor(embed,lvl):
			msg = ''
			for i in range(lvl):
				msg += "⬛"
			return msg

		lettres = check_diff(difficulty)
		lvl = 1
		timeout = 2.0
		answer = give_letter(lettres,lvl)
		embed = create_embed(answer)
		msg_id = ctx.send(f'**{ctx.message.author}** plays Sequencer',embed=embed)
		await asyncio.sleep(timeout)

		await msg_id.edit(f'**{ctx.message.author}** plays Sequencer',embed=embed)
		while True:
			print(answer,lvl)

			try:
				user_answer = await self.client.wait_for('message', timeout=timeout*2)
			except:
				print("timeout failed")
				break
				
			if answer != user_answer.content:
				print("wrong answer failed")
				break
			else:
				lvl +=1
				timeout += 0.5
				answer = give_letter(lettres,lvl)

def setup(client):
	client.add_cog(Games(client))