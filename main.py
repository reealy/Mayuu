import discord
import os

from discord.ext import commands
from libs.keep_alive import keep_alive

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix=os.getenv('PREFIX'), description="Mayuu~ provides some cute commands :", intents=intents)
bot.remove_command('help')

# Verify the owner
def owner(ctx):
  return ctx.message.author.id == int(os.getenv('OWNER_ID'))

'''
Owner permissions command only
'''

# Load cogs
@bot.command()
@commands.check(owner)
async def load(ctx,extension = None):
  if extension:
    bot.load_extension(f'cogs.{extension}')

# Unload cogs
@bot.command()
@commands.check(owner)
async def unload(ctx,extension = None):
  if extension:
    bot.unload_extension(f'cogs.{extension}')

# Reload cogs
@bot.command()
@commands.check(owner)
async def reload(ctx,extension = None):
  if extension:
    try:
     bot.reload_extension(f'cogs.{extension}')
    except:
     bot.load_extension(f'cogs.{extension}')

# Search cogs
for filename in os.listdir('./cogs'):
  if filename.endswith('.py'):
    bot.load_extension(f'cogs.{filename[:-3]}')

# Print that the bot runs
@bot.event
async def on_ready():
  await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="!help 🌟"))
  print('{0.user} enters!'.format(bot))

keep_alive()
bot.run(os.getenv('TOKEN'))