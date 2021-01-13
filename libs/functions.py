import discord

def generate_error(usage,example):
	embed = discord.Embed()
	embed.colour = discord.Colour(0xFF0000)

	error_message = "❌	Invalid command usage!"
	error_usage = usage
	error_example = example

	embed.title = f'{error_message}'
	embed.add_field(name = "Usage :", value = f"`{error_usage}`", inline = False)
	embed.add_field(name = "Example :", value = f"`{error_example}`", inline = True)
	embed.set_footer(text="Type !help <command> for more information about this command.")
	return embed

def generate_help(name,content,usage,example):
	embed = discord.Embed()
	embed.colour = discord.Colour(0x1914FF)

	command = f"{name} command"
	embed.title = f'{command}'
	embed.description = content
	embed.add_field(name = "Usage :", value = f"`{usage}`", inline = False)
	embed.add_field(name = "Example :", value = f"`{example}`", inline = True)
	return embed