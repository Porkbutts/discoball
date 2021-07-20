from json.decoder import JSONDecodeError
from datastore import Datastore
import os
import platform

import json
import random
from datetime import datetime

from discord import Intents, Embed
from discord.colour import Color
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from discord_slash.model import SlashCommandOptionType
from discord_slash.utils.manage_commands import create_option


APP_ENV = os.getenv('APP_ENV', "")
BOT_TOKEN = os.getenv('BOT_TOKEN')
GUILD_IDS = [218962182606422016]  # bay of pigs

bot = commands.Bot(command_prefix='!',
                   description="the pork bot", intents=Intents.all())
slash = SlashCommand(bot, sync_commands=APP_ENV.lower() == 'production')
ds = Datastore()

@bot.event
async def on_ready():
    print("Ready!")


@slash.slash(name="ping", guild_ids=GUILD_IDS, description="Ping the bot")
async def _ping(ctx):
    await ctx.send(f"Pong! ({bot.latency*1000}ms)")


@slash.slash(name="sysinfo", guild_ids=GUILD_IDS, description="Print the bot system information")
async def system_info(ctx: SlashContext):
  embed = Embed(title="Platform Information", color=Color.blurple())
  embed.add_field(name="System", value=platform.system(), inline=False)
  embed.add_field(name="Release", value=platform.release(), inline=False)
  embed.add_field(name="Version", value=platform.version(), inline=False)
  await ctx.send(embed=embed)


@slash.slash(name="version", guild_ids=GUILD_IDS, description="Print the app version information")
async def version(ctx: SlashContext):
  try:
    dt = datetime.strptime(
        os.getenv("HEROKU_RELEASE_CREATED_AT"), "%Y-%m-%dT%H:%M:%SZ")
  except ValueError:
    dt = None
  embed = Embed(title="Deployment Information", timestamp=dt, color=Color.blurple())
  embed.add_field(name="Release Version", value=os.getenv(
      "HEROKU_RELEASE_VERSION"), inline=False)
  embed.add_field(name="Commit", value=os.getenv(
      "HEROKU_SLUG_COMMIT"), inline=False)
  embed.add_field(name="Description", value=os.getenv(
      "HEROKU_SLUG_DESCRIPTION"), inline=False)
  await ctx.send(embed=embed)

DICE = {
    1: "<:diceone:866483928164073503>",
    2: "<:dicetwo:866484579070509067>",
    3: "<:dicethree:866484611944153118>",
    4: "<:dicefour:866484638952587265>",
    5: "<:dicefive:866484664264032276>",
    6: "<:dicesix:866484690965233685>",
}

@slash.slash(
    name="roll",
    guild_ids=GUILD_IDS,
    description="Roll an N-sided die",
    options=[
        create_option(
            name="num_dice",
            description="How many die to roll? (default: 2)",
            option_type=SlashCommandOptionType.INTEGER,
            required=False,
        ),
    ])
async def roll(ctx: SlashContext, num_dice: int = 2):
  embed = Embed(title="Results", color=Color.blurple())
  rolls = [random.choice(list(DICE.items())) for _ in range(num_dice)]
  embed.add_field(name="Rolls", value=" ".join(map(lambda r: r[1], rolls)), inline=True)
  embed.add_field(name="Total", value=sum(map(lambda r: r[0], rolls)), inline=True)
  await ctx.send(embed=embed)


@slash.slash(
    name="save",
    guild_ids=GUILD_IDS,
    description="Update a key/value",
    options=[
        create_option(
            name="key",
            description="key",
            option_type=SlashCommandOptionType.STRING,
            required=True,
        ),
        create_option(
            name="value",
            description="value",
            option_type=SlashCommandOptionType.STRING,
            required=True,
        ),
    ])
async def save(ctx: SlashContext, key, value):
    try:
        decoded = json.loads(value)
    except JSONDecodeError:
        decoded = value
    ds.data[key] = decoded
    formatted = json.dumps(ds.data, indent=2)
    embed = Embed(title="Datastore", color=Color.blurple())
    embed.add_field(name="result", value=f"```json\n{formatted}\n```", inline=False)
    await ctx.send(embed=embed)
    ds.save()


@slash.slash(
    name="read",
    guild_ids=GUILD_IDS,
    description="Read the value of a key stored with save()",
    options=[
        create_option(
            name="key",
            description="key",
            option_type=SlashCommandOptionType.STRING,
            required=True,
        ),
    ])
async def read(ctx: SlashContext, key):
    embed = Embed(title="Datastore", color=Color.blurple())
    embed.add_field(name="key", value=key, inline=True)
    formatted = json.dumps(ds.data[key], indent=2)
    embed.add_field(name="value", value=f"```json\n{formatted}\n```", inline=False)
    await ctx.send(embed=embed)


bot.run(BOT_TOKEN)