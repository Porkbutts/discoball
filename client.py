import os
import platform

import random
from datetime import datetime

from discord import Intents, Embed
from discord.colour import Color
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
import discord_slash
from discord_slash.model import SlashCommandOptionType
from discord_slash.utils.manage_commands import create_option


APP_ENV = os.getenv('APP_ENV', "")
BOT_TOKEN = os.getenv('BOT_TOKEN')
GUILD_IDS = [218962182606422016]  # bay of pigs

bot = commands.Bot(command_prefix='!',
                   description="the pork bot", intents=Intents.all())
slash = SlashCommand(bot, sync_commands=APP_ENV.lower() == 'production')


@bot.event
async def on_ready():
    print("Ready!")


@slash.slash(name="ping", guild_ids=GUILD_IDS, description="Ping the bot")
async def _ping(ctx):
    await ctx.send(f"Pong! ({bot.latency*1000}ms)")


@slash.slash(
    name="roll",
    guild_ids=GUILD_IDS,
    description="Roll an N-sided die",
    options=[
        create_option(
            name="num_sides",
            description="How many sides to the die? (default: 6)",
            option_type=SlashCommandOptionType.INTEGER,
            required=False,
        ),
        create_option(
            name="num_dice",
            description="How many die to roll? (default: 2)",
            option_type=SlashCommandOptionType.INTEGER,
            required=False,
        ),
    ])
async def roll(ctx: SlashContext, num_sides: int = 6, num_dice: int = 2):
  rolls = []
  for _ in range(num_dice):
    rolls.append(random.randint(1, num_sides))
  await ctx.send(content=f"Rolled {num_dice} {num_sides}-sided dice. Output: {rolls}, Total: {sum(rolls)}")


bot.run(BOT_TOKEN)
