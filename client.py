import os
import platform

import random
from datetime import datetime

from discord import Intents, Embed
from discord.colour import Color
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_option


APP_ENV = os.getenv('APP_ENV', "")
BOT_TOKEN = os.getenv('BOT_TOKEN')
guild_ids = [218962182606422016] # bay of pigs

bot = commands.Bot(command_prefix='!', description="the pork bot", intents=Intents.all())
slash = SlashCommand(bot, sync_commands=APP_ENV.lower() == 'production')


@bot.event
async def on_ready():
    print("Ready!")

@slash.slash(name="ping", guild_ids=guild_ids, description="Ping the bot")
async def _ping(ctx):
    await ctx.send(f"Pong! ({bot.latency*1000}ms)")

@slash.slash(
  name="roll",
  guild_ids=guild_ids,
  description="Roll an N-sided die",
  options=[
    create_option(
      name="num_sides",
      description="How many sides to the die? (default: 6)",
      option_type=4,
      required=False,
    ),
    create_option(
      name="num_dice",
      description="How many die to roll? (default: 2)",
      option_type=4,
      required=False,
    ),
  ])
async def roll(ctx: SlashContext, num_sides: int = 6, num_dice: int = 2):
  rolls = []
  for _ in range(num_dice):
    rolls.append(random.randint(1, num_sides))
  await ctx.send(content=f"Rolled {num_dice} {num_sides}-sided dice. Output: {rolls}, Total: {sum(rolls)}")

@slash.slash(name="sysinfo", guild_ids=guild_ids)
async def system_info(ctx: SlashContext):
    embed = Embed(title="System Information", timestamp=datetime.utcnow(), color=Color.green())
    embed.add_field(name="System", value=platform.system(), inline=False)
    embed.add_field(name="Release", value=platform.release(), inline=False)
    embed.add_field(name="Version", value=platform.version(), inline=False)
    await ctx.send(embed=embed)

@slash.slash(name="version", guild_ids=guild_ids)
async def version(ctx: SlashContext):
    embed = Embed(title="Version Information", timestamp=datetime.utcnow(), color=Color.green())
    embed.add_field(name="Release Date/Time", value=os.getenv("HEROKU_RELEASE_CREATED_AT"), inline=False)
    embed.add_field(name="Release Version", value=os.getenv("HEROKU_RELEASE_VERSION"), inline=False)
    embed.add_field(name="Commit", value=os.getenv("HEROKU_SLUG_COMMIT"), inline=False)
    embed.add_field(name="Description", value=os.getenv("HEROKU_SLUG_DESCRIPTION"), inline=False)
    await ctx.send(embed=embed)

bot.run(BOT_TOKEN)
