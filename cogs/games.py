import discord
import asyncio
import random
import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from libs.database import *
from libs.functions import *
from discord.ext import commands

class Games(commands.Cog):
	def __init__(self,client):
		self.client = client

	@commands.Cog.listener()
	async def on_ready(self):
		print('games loaded.')

	@commands.command()
	async def guess(self,ctx,*,difficulty="e"):
		def check_diff(difficulty):
			print(difficulty)
			if difficulty.lower() == "e" or difficulty.lower() == "easy":
				answer = random.randint(1,10)
				difficulty_type = "Easy Mode"
				attempt = 4
			elif difficulty.lower() == "n" or difficulty.lower() == "normal":
				answer = random.randint(1,100)
				difficulty_type = "Normal Mode"
				attempt = 8
			elif difficulty.lower() == "h" or difficulty.lower() == "hard":
				answer = random.randint(1,1000)
				difficulty_type = "Hard Mode"	
				attempt = 12
			else:
				raise ValueError('Invalid mode')
			return answer,attempt,difficulty_type

		def verify(imput,answer):
			try:
				if int(imput) == answer:
					return 0
				elif int(imput) > answer:
					return 1
				elif int(imput) < answer:
					return 2
			except:
				print("invalid?")
				return -1

		def get_embed(answer,attempt,hotncold,difficulty_type):

			ans_msg = "\u200b"
			attempt_msg = "\u200b"
			thermometer_msg = "\u200b"
			thermometer = ["🌿 Perfect~","☀️ Too hot~","❄️ Too cold~"]

			for i in range(len(answer)):
				ans_msg += f"{answer[i]}\n"

			for i in range(len(attempt)):
				attempt_msg += f"{attempt[i]}\n"

			for i in range(len(hotncold)):
				thermometer_msg += f"{thermometer[hotncold[i]]}\n"

			embed = discord.Embed()
			embed.colour = discord.Colour(0x1914FF)
			embed.title = "Guess  🎲"
			embed.description = f"**{difficulty_type}**\n*Try to guess a number, I suppose...*"
			embed.add_field(name = "Attempts", value = f"**{attempt_msg}**", inline = True)
			embed.add_field(name = "Guess", value = f"{ans_msg}", inline = True)
			embed.add_field(name = "🌡️", value = f"{thermometer_msg}", inline = True)
			return embed

		answer,attempt,difficulty_type = check_diff(difficulty)
		stored_guess = []
		stored_attempt = [attempt]
		stored_hotncold = []
		user_id = ctx.message.author.id
		embed = get_embed(stored_guess,stored_attempt,stored_hotncold,difficulty_type)
		msg_id = await ctx.channel.send(embed=embed)

		while attempt > 0:
			try:
				imput = await self.client.wait_for('message', timeout=30)
			except:
				print("timeout!")
				return
			
			if imput.author.id == user_id:
				verification = verify(imput.content,answer)
				print(answer,imput.content,attempt,verification)
				if verification > 0:
					attempt -= 1
					stored_guess += [imput.content]
					stored_hotncold += [verification]
					if attempt != 0:
						stored_attempt += [attempt]	
						print("Not the guessed number")

					embed = get_embed(stored_guess,stored_attempt,stored_hotncold,difficulty_type)
					await msg_id.edit(embed=embed)

				elif verification == 0:
					stored_guess += [imput.content]
					stored_hotncold += [verification]

					embed = get_embed(stored_guess,stored_attempt,stored_hotncold,difficulty_type)
					embed.set_footer(text="You Won! 🎉")
					await msg_id.edit(embed=embed)
					print("Found!")
					return

				else:
					pass
			
			else:
				pass
		
		embed = get_embed(stored_guess,stored_attempt,stored_hotncold,difficulty_type)
		embed.set_footer(text="Seems like it's Game Over...")
		await msg_id.edit(embed=embed)
		print("out of attempts!")

	@guess.error
	async def guess_error(self,ctx,error):

		error_usage = '!guess <difficulty>'
		error_example = '!guess Normal'
		embed = generate_error(error_usage,error_example)
		await ctx.send(embed=embed)

	@commands.command(aliases=['roll-duel'])
	async def rollduel(self,ctx,tag,rolls=3,size=99):
		def rolling(rolls,size):
			lst = []
			for i in range(rolls):
				lst += [random.randint(1,size)]
			return lst

		if len(ctx.message.mentions) == 1 and (rolls < 11 and rolls > 0):
			user_id = ctx.message.author.id
			tag_user_id = ctx.message.mentions[0].id

			if tag_user_id == self.client.user.id:
				print("Mayuu!")
			
			roll1 = rolling(rolls,size)
			roll2 = rolling(rolls,size)
			print(roll1,roll2)

		else:
			raise ValueError("Invalid command usage!") 

	@commands.command()
	async def sequencer(self,ctx,*,difficulty="n"):

		def check_diff(difficulty):
			if difficulty == "number" or difficulty == "n":
				lettres = ['0','1','2','3','4','5','6','7','8','9']
				char = [":zero:",":one:",":two:",":three:",":four:",":five:",":six:",":seven:",":eight:",":nine:"]
			elif difficulty == "taiko" or difficulty == "t":
				lettres = ['d','k']
				char = ["🔴","🔵"]
			elif difficulty == "alphabet" or difficulty == "letter" or difficulty == "l":
				lettres = ['a','b','c','d','e','f','g','h','i','j','k','m','n','o','p','q','r','s','t','u','w','x','y','z']
			else:
				raise ValueError('Invalid mode')
			return lettres,char

		def get_answer_id(lettres,lvl):
			answer = []
			for i in range(lvl):
				answer += [random.randint(0, len(lettres)-1)]
			return answer

		def check_answer(answer,answer_id,mode):
			check = ""

			for i in answer_id:
				check += str(mode[i])

			if check == answer:
				return True
			else:
				return False

		def get_embed(stored_answer):
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

		mode,char = check_diff(difficulty)

		lvl = 1
		timeout = 1.0
		answer_id = get_answer_id(mode,lvl)
		stored_answer = answer_id
		'''
		embed = create_embed(answer)
		msg_id = ctx.send(f'**{ctx.message.author}** plays Sequencer',embed=embed)
		await asyncio.sleep(timeout)

		await msg_id.edit(f'**{ctx.message.author}** plays Sequencer',embed=embed)
		'''
		while True:
			print(answer_id,stored_answer,lvl)
			try:
				user_answer = await self.client.wait_for('message', timeout=timeout*4)
			except:
				print("timeout failed")
				break
				
			if not check_answer(user_answer.content,answer_id,mode):
				print("wrong answer failed")
				break
			else:

				lvl +=1
				timeout += 0.2
				answer_id = get_answer_id(mode,lvl)
				stored_answer.insert(0,answer_id)

def setup(client):
	client.add_cog(Games(client))