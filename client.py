import os
import discord
from discord.ext import commands
from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import create_option, create_choice


APP_ENV = os.getenv('APP_ENV', "")
BOT_TOKEN = os.getenv('BOT_TOKEN')
guild_ids = [218962182606422016] # bay of pigs

bot = commands.Bot(command_prefix='!', description="the pork bot", intents=discord.Intents.all())
slash = SlashCommand(bot, sync_commands=APP_ENV.lower() == 'production')


@bot.event
async def on_ready():
    print("Ready!")

@slash.slash(name="ping", guild_ids=guild_ids, description="Ping the bot")
async def _ping(ctx):
    await ctx.send(f"Pong! ({bot.latency*1000}ms)")

bot.run(BOT_TOKEN)
