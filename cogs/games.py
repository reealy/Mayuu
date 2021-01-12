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
		
		def get_embed(user,tag_user,roll1,roll2,msg1,msg2):

			embed = discord.Embed()
			embed.colour = discord.Colour(0x1914FF)
			embed.title = "Roll-duel  🔫"
			embed.description = f"**{user.mention}** vs. **{tag_user.mention}**"
			embed.add_field(name = f"**{user.name}**", value = msg1, inline = True)
			embed.add_field(name = f"**{tag_user.name}**", value = msg2, inline = True)
			return embed

		def rolling_str(roll1,roll2,status,iteration=0,iteration_status=False):
			str1 = ""
			str2 = ""
			if status == 0:
				for i in range(len(roll1)):
					str1 += "**🎲**\n"
					str2 += "**🎲**\n"
				str1 += "Total : 0"
				str2 += "Total : 0"

			elif status == 1:
				for i in range(iteration):
					str1 += f"**{roll1[i]}**\n"
					str2 += "**🎲**\n"

				if iteration_status:
					str1 += "...\n"
					str2 +=  "**🎲**\n"
				else:
					str1 += f"**{roll1[iteration]}**\n"
					str2 += "**🎲**\n"

				for j in range(len(roll1)-iteration-1):
					str1 += "**🎲**\n"
					str2 += "**🎲**\n"
				
				if iteration_status:
					str1 += f"Total : **{sum(roll1[:iteration])}**"
					str2 += "Total : 0"
				else:
					str1 += f"Total : **{sum(roll1[:iteration+1])}**"
					str2 += "Total : 0"

			elif status == 2:
				for i in range(len(roll1)):
					str1 += f"**{roll1[i]}**\n"
					str2 += "**🎲**\n"
				str1 += f"Total : **{sum(roll1)}**"
				str2 += "Total : 0"

			elif status == 3:
				for i in range(iteration):
					str1 += f"**{roll1[i]}**\n"
					str2 += f"**{roll2[i]}**\n"

				if iteration_status:
					str1 += f"**{roll1[iteration]}**\n"
					str2 +=  "...\n"
				else:
					str1 += f"**{roll1[iteration]}**\n"
					str2 += f"**{roll2[iteration]}**\n"

				for j in range(len(roll1)-iteration-1):
					str1 += f"**{roll1[j+iteration+1]}**\n"
					str2 += "**🎲**\n"
				
				if iteration_status:
					str1 += f"Total : **{sum(roll1)}**"
					str2 += f"Total : **{sum(roll2[:iteration])}**"
				else:
					str1 += f"Total : **{sum(roll1)}**"
					str2 += f"Total : **{sum(roll2[:iteration+1])}**"

			elif status == 4:
				for i in range(len(roll1)):
					str1 += f"**{roll1[i]}**\n"
					str2 += f"**{roll2[i]}**\n"
				str1 += f"Total : **{sum(roll1)}**"
				str2 += f"Total : **{sum(roll2)}**"
			else:
				raise ValueError('Something wrong happened!')
			return str1, str2

		if len(ctx.message.mentions) == 1 and (rolls < 11 and rolls > 0):
			user = ctx.message.author
			tag_user = ctx.message.mentions[0]
			is_bot = False
			is_player1_turn = False 

			if tag_user.id == self.client.user.id:
				is_bot = True
				print("Mayuu!")
			
			roll1 = rolling(rolls,size)
			roll2 = rolling(rolls,size)
			if roll1 > roll2:
				print("player 2 is winner")
				winner = tag_user
				winner_point = sum(roll1)
				loser = user
			elif roll1 < roll2:
				print("player 1 is winner")
				winner = user
				winner_point = sum(roll2)
				loser = tag_user
			else:
				winner = "tie"
				winner_point = sum(roll1)
				

			msg1, msg2 = rolling_str(roll1,roll2,0)
			embed = get_embed(user,tag_user,roll1,roll2,msg1,msg2)
			embed.set_footer(text=f"{tag_user.name}, click on the dice to roll.")
			msg_id = await ctx.channel.send(embed=embed)
			await msg_id.add_reaction(str("🎲"))
			await asyncio.sleep(1)

			if is_bot:
				while True:
					await asyncio.sleep(1)
					for i in range(len(roll1)):
						msg2, msg1 = rolling_str(roll1,roll2,1,i,True)
						embed = get_embed(user,tag_user,roll1,roll2,msg1,msg2)
						embed.set_footer(text=f"{tag_user.name} rolls...  🎲")
						await msg_id.edit(embed=embed)
						await asyncio.sleep(1)

						msg2, msg1 = rolling_str(roll1,roll2,1,i,False)
						embed = get_embed(user,tag_user,roll1,roll2,msg1,msg2)
						embed.set_footer(text=f"{tag_user.name} rolls...  🎲")
						await msg_id.edit(embed=embed)
						await asyncio.sleep(1)

					msg2, msg1 = rolling_str(roll1,roll2,2)
					embed = get_embed(user,tag_user,roll1,roll2,msg1,msg2)
					embed.set_footer(text=f"{user.name}, click on the dice to roll.")
					await msg_id.edit(embed=embed)
					break

				while True:
					try:
						imput = await self.client.wait_for('raw_reaction_add', timeout=30)
					except:
						return

					if imput.user_id == user.id:
						for i in range(len(roll1)):
							msg2, msg1 = rolling_str(roll1,roll2,3,i,True)
							embed = get_embed(user,tag_user,roll1,roll2,msg1,msg2)
							embed.set_footer(text=f"{user.name} rolls...")
							await msg_id.edit(embed=embed)
							await asyncio.sleep(1)

							msg2, msg1 = rolling_str(roll1,roll2,3,i,False)
							embed = get_embed(user,tag_user,roll1,roll2,msg1,msg2)
							embed.set_footer(text=f"{user.name} rolls...")
							await msg_id.edit(embed=embed)
							await asyncio.sleep(1)

						msg2, msg1 = rolling_str(roll1,roll2,4)
						embed = get_embed(user,tag_user,roll1,roll2,msg1,msg2)
						embed.set_footer(text="Result time ! 🥁")
						await msg_id.edit(embed=embed)
				
						if winner == "tie":
							result_msg = f'**{user.mention}** and **{tag_user.mention}** made a tie with **{winner_point}** points !'
						else:
							result_msg = f'**{winner.mention}** wins against **{loser.mention}** with **{winner_point}** points !'
						await ctx.channel.send(result_msg)
						break

					else:
						pass

			else:
				while True:
					try:
						imput = await self.client.wait_for('raw_reaction_add', timeout=30)
					except:
						return

					if imput.user_id == tag_user.id:
						for i in range(len(roll1)):
							msg2, msg1 = rolling_str(roll1,roll2,1,i,True)
							embed = get_embed(user,tag_user,roll1,roll2,msg1,msg2)
							embed.set_footer(text=f"{tag_user.name} rolls...  🎲")
							await msg_id.edit(embed=embed)
							await asyncio.sleep(1)

							msg2, msg1 = rolling_str(roll1,roll2,1,i,False)
							embed = get_embed(user,tag_user,roll1,roll2,msg1,msg2)
							embed.set_footer(text=f"{tag_user.name} rolls...  🎲")
							await msg_id.edit(embed=embed)
							await asyncio.sleep(1)

						msg2, msg1 = rolling_str(roll1,roll2,2)
						embed = get_embed(user,tag_user,roll1,roll2,msg1,msg2)
						embed.set_footer(text=f"{user.name}, click on the dice to roll.")
						await msg_id.edit(embed=embed)
						break
				while True:
					try:
						imput = await self.client.wait_for('raw_reaction_add', timeout=30)
					except:
						return
				
					if imput.user_id == user.id:
						for i in range(len(roll1)):
							msg2, msg1 = rolling_str(roll1,roll2,3,i,True)
							embed = get_embed(user,tag_user,roll1,roll2,msg1,msg2)
							embed.set_footer(text=f"{user.name} rolls...")
							await msg_id.edit(embed=embed)
							await asyncio.sleep(1)

							msg2, msg1 = rolling_str(roll1,roll2,3,i,False)
							embed = get_embed(user,tag_user,roll1,roll2,msg1,msg2)
							embed.set_footer(text=f"{user.name} rolls...")
							await msg_id.edit(embed=embed)
							await asyncio.sleep(1)

						msg2, msg1 = rolling_str(roll1,roll2,4)
						embed = get_embed(user,tag_user,roll1,roll2,msg1,msg2)
						embed.set_footer(text="Result time ! 🥁")
						await msg_id.edit(embed=embed)
				
						if winner == "tie":
							result_msg = f'**{user.mention}** and **{tag_user.mention}** made a tie with **{winner_point}** points !'
						else:
							result_msg = f'**{winner.mention}** wins against **{loser.mention}** with **{winner_point}** points !'
						await ctx.channel.send(result_msg)
						break

					else:
						pass

		else:
			raise ValueError("Invalid command usage!") 
	

	@rollduel.error
	async def rollduel_error(self,ctx,error):
		print(error)

		error_usage = '!roll-duel (@someone) <rolls to do> <size>'
		error_example = '!roll-duel @Mayuu 3 10'
		embed = generate_error(error_usage,error_example)
		await ctx.send(embed=embed)


	@commands.command()
	async def sequencer(self,ctx,*,difficulty="n"):
		def check_diff(difficulty):
			if difficulty.lower() == "number" or difficulty.lower() == "n":
				lettres = ['0','1','2','3','4','5','6','7','8','9']
				char = ["0️⃣","1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣"]
				mode = "Numbers"
			elif difficulty.lower() == "taiko" or difficulty.lower() == "t":
				lettres = ['d','k']
				char = ["🔴","🔵"]
				mode = "Taiko"
			elif difficulty.lower() == "alphabet" or difficulty.lower() == "letter" or difficulty.lower() == "l" or difficulty.lower() == "a":
				lettres = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
				char = [":regional_indicator_a:",":regional_indicator_b:",":regional_indicator_c:",":regional_indicator_d:",":regional_indicator_e:",":regional_indicator_f:",":regional_indicator_g:",":regional_indicator_h:",":regional_indicator_i:",":regional_indicator_j:",":regional_indicator_k:",":regional_indicator_l:",":regional_indicator_m:",":regional_indicator_n:",":regional_indicator_o:",":regional_indicator_p:",":regional_indicator_q:",":regional_indicator_r:",":regional_indicator_s:",":regional_indicator_t:",":regional_indicator_u:",":regional_indicator_v:",":regional_indicator_w:",":regional_indicator_x:",":regional_indicator_y:",":regional_indicator_z:"]
				mode = "Alphabet"
			else:
				raise ValueError('Invalid mode')
			return lettres,char,mode

		def get_answer_id(lettres,lvl):
			answer = []
			for i in range(lvl):
				answer += [random.randint(0, len(lettres)-1)]
			return answer

		def check_answer(answer,answer_id,mode):
			check = ""

			for i in answer_id:
				check += str(mode[i])

			print(check == answer,answer,check)
			if check == answer:
				return True
			else:
				return False

		def get_embed(answer,censor,level,char,mode):

			ans_msg = "\u200b"
			lvl_msg = "\u200b"
			solution = ""

			for i in range(len(answer)-1):
				for j in range(len(answer[i])):
					ans_msg += f"{char[answer[i][j]]}"
				ans_msg += "\n"

			for i in range(len(level)):
				lvl_msg += f"{level[i]}\n"

			if censor == True:
				for i in range(len(answer)):
					solution += "⬛"
			else:
				for i in range(len(answer)):
					solution += char[answer[len(answer)-1][i]]

			embed = discord.Embed()
			embed.colour = discord.Colour(0x1914FF)
			embed.title = "Sequencer  🧩"
			embed.description = f"**Type : {mode}**\n*Will you not forget?*\n\n{solution}"
			embed.add_field(name = "Level", value = f"**{lvl_msg}**", inline = True)
			embed.add_field(name = "Answers", value = f"{ans_msg}", inline = True)
			return embed

		lettres,char,mode = check_diff(difficulty)

		lvl = 1
		timeout = 1.0
		answer_id = get_answer_id(lettres,lvl)
		stored_answer = [answer_id]
		stored_lvl = [lvl]
		user_id = ctx.message.author.id
		waiting_for = False
		embed = get_embed(stored_answer,waiting_for,stored_lvl,char,mode)
		msg_id = await ctx.channel.send(embed=embed)
		await asyncio.sleep(timeout)
		waiting_for = True
		embed = get_embed(stored_answer,waiting_for,stored_lvl,char,mode)
		await msg_id.edit(embed=embed)

		while True:
			try:
				imput = await self.client.wait_for('message', timeout=timeout*3)
			except:
				embed = get_embed(stored_answer,waiting_for,stored_lvl,char,mode)
				embed.set_footer(text="Timeout!\nHope you can answer faster next time!")
				await msg_id.edit(embed=embed)
				print("timeout failed")
				break

			if imput.author.id == user_id:
				if not check_answer(imput.content,answer_id,lettres):
					stored_answer += [answer_id]
					embed = get_embed(stored_answer,waiting_for,stored_lvl,char,mode)
					embed.set_footer(text="Wrong Answer!\nHope you will do better next time!")
					await msg_id.edit(embed=embed)
					print("wrong answer failed")
					break
				else:
					lvl +=1
					timeout += 0.1
					answer_id = get_answer_id(lettres,lvl)
					stored_answer += [answer_id]
					stored_lvl += [lvl]
					waiting_for = False
					embed = get_embed(stored_answer,waiting_for,stored_lvl,char,mode)
					await msg_id.edit(embed=embed)
					waiting_for = True
					embed = get_embed(stored_answer,waiting_for,stored_lvl,char,mode)
					await asyncio.sleep(timeout)
					await msg_id.edit(embed=embed)
			
			else:
				pass

	@sequencer.error
	async def sequencer_error(self,ctx,error):

		error_usage = '!sequencer <mode>'
		error_example = '!sequencer Number'
		embed = generate_error(error_usage,error_example)
		await ctx.send(embed=embed)

def setup(client):
	client.add_cog(Games(client))