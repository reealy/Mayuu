import discord
from discord.ext import commands
import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from libs.database import *
from libs.functions import *

class Help(commands.Cog):
	def __init__(self,client):
		self.client = client

	@commands.Cog.listener()
	async def on_ready(self):
		print('help loaded.')

	@commands.command()
	async def help(self,ctx,args = None):
		embed = discord.Embed()

		# If there are no arguments, just list the commands:
		if not args:

			field1 = ''
			for i in fun_command_lst:
				field1 += f'!{i}\n'

			field2 = ''
			for j in utility_command_lst:
				field2 += f'!{j}\n'
			
			field3 = ''
			for j in game_command_lst:
				field3 += f'!{j}\n'


			embed.colour = discord.Colour(0x1914FF)
			embed.title = "Mayuu~ :cherry_blossom: "
			embed.set_thumbnail(url=self.client.user.avatar_url)
			embed.add_field(name = "Fun :",value = field1, inline = True)
			embed.add_field(name = "Utility :",value = field2, inline = True)
			embed.add_field(name = "Games :",value = field3, inline = True)

			await ctx.send(content="List of commands : (Type `!help <command>` for usage)",embed=embed)

		elif args:
			command_list = sum([fun_command_lst,utility_command_lst,game_command_lst],[])
			if args in command_list:
				print(args)
				if args == "help":
					name = "Help"
					content = "List all commands avaliable. \nAdding a valid command will give the help of that command."
					usage = "!help <command>"
					example = "!help help"

					embed = generate_help(name,content,usage,example)
					await ctx.send(embed=embed)
				
				elif args == "roll":
					name = "Roll"
					content = "Chooses randomly a number between 0 and the limit number. \nUses 99 as the default limit number."
					usage = "!roll <limit>"
					example = "!roll 69"

					embed = generate_help(name,content,usage,example)
					await ctx.send(embed=embed)

				elif args == "emotion":
					name = "Emotion"
					content = "Chooses a random feeling, for example \"love\" or \"happy\"."
					usage = "!emotion"
					example = "!emotion"

					embed = generate_help(name,content,usage,example)
					await ctx.send(embed=embed)

				elif args == "inspire":
					name = "Inspire"
					content = "Not feeling inspired ? \nRandomly generate an image with an inspiring text."
					usage = "!inspire"
					example = "!inspire"

					embed = generate_help(name,content,usage,example)
					await ctx.send(embed=embed)

				elif args == "quote":
					name = "Quote"
					content = "Randomly gives a quote from an user.\n Randomly quotes anybody from the server per default."
					usage = "!quote <user>"
					example = "!quote user"

					embed = generate_help(name,content,usage,example)
					await ctx.send(embed=embed)

				elif args == "someone":
					name = "Someone"
					content = "Randomly chooses an user from the server."
					usage = "!someone"
					example = "!someone"

					embed = generate_help(name,content,usage,example)
					await ctx.send(embed=embed)

				elif args == "yesno":
					name = "Yes/No"
					content = "Answers you honestly with a yes or no answer"
					usage = "!yesno <text>"
					example = "!yesno Will today my lucky day?"

					embed = generate_help(name,content,usage,example)
					await ctx.send(embed=embed)

				elif args == "delay":
					name = "Delay"
					content = "Tag the user after a specified amount of time. \nTime could be either in seconds (s), minutes (min), hours (h) or days (d).\n Removing the message will cancel the command."
					usage = "!delay (time) <text>"
					example = "!delay 30min Breakfast time!"

					embed = generate_help(name,content,usage,example)
					await ctx.send(embed=embed)

				elif args == "counter":
					name = "Counter"
					content = "Counts the number of arguments providen"
					usage = "!counter <text>"
					example = "!counter This will count exactly 6 times"

					embed = generate_help(name,content,usage,example)
					await ctx.send(embed=embed)

				elif args == "infoserv":
					name = "Infoserv"
					content = "Provides some informations about the server."
					usage = "!infoserv"
					example = "!infoserv"

					embed = generate_help(name,content,usage,example)
					await ctx.send(embed=embed)

				elif args == "time":
					name = "Time"
					content = "Gives the time (at UTC+0)."
					usage = "!time"
					example = "!time"

					embed = generate_help(name,content,usage,example)
					await ctx.send(embed=embed)

				elif args == "ping":
					name = "Ping"
					content = "Gives the ping in ms."
					usage = "!ping"
					example = "!ping"

					embed = generate_help(name,content,usage,example)
					await ctx.send(embed=embed)

				elif args == "guess":
					name = "Guess"
					content = "The guess number game. 🎲\nFeatures mutiple difficulty modes :\n\n**Easy (or e) :** 4 Attempts, Number between 1-10.\n**Normal (or n) :** 8 Attempts, Number between 1-100.\n**Hard (or h) :** 12 Attempts, Number between 1-1000.\n\n*There's an automatic timeout after 30 seconds.*"
					usage = "!guess <difficulty>"
					example = "!guess Normal"

					embed = generate_help(name,content,usage,example)
					await ctx.send(embed=embed)

				elif args == "sequencer":
					name = "Sequencer"
					content = "The sequencer memory game. 🧩\nFeatures mutiple modes :\n\n**Number (or n)** Uses numbers between 0-9.\n**Alphabet (or letter/a/l)** Uses alphabet letters between A-Z.\n**Taiko (or t)** Uses the taiko notes from the popular game \"Taiko no Tatsujin\" with d (don) and k (kat).\n\nYou lose if you answer wrong or don't reply in time.\n*Note : Wait for the notes to hide before you send the answer or it will ignore your message.*"
					usage = "!sequencer <mode>"
					example = "!sequencer Number"

					embed = generate_help(name,content,usage,example)
					await ctx.send(embed=embed)

				elif args == "roll-duel" or args == "rollduel":
					name = "Roll-Duel"
					content = "The roll-duel game. 🔫\nTag a user to duel him for a roll battle! The user with the most total points wins.\n*Note : The tagged user always start rolling first.*\n\n*There's an automatic timeout after 30 seconds.*"
					usage = "!roll-duel (@someone) <rolls to do> <size>"
					example = "!roll-duel @Mayuu 3 10"

					embed = generate_help(name,content,usage,example)
					await ctx.send(embed=embed)

				else:
					embed.colour = discord.Colour(0xFF0000)
					embed.title = "❌  Error 404 :"
					embed.description = "No help found!"
					await ctx.send(embed=embed)
					return
			
			else:
				embed.colour = discord.Colour(0xFF0000)
				embed.title = "❌  Command not found! :"
				embed.description = "Type !help for a list of avaliable commands."
				await ctx.send(embed=embed)

		else:
			error_usage = '!help'
			error_example = '!help'
			embed = generate_error(error_usage,error_example)
			await ctx.send(embed=embed)

def setup(client):
	client.add_cog(Help(client))