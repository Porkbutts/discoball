import os
import platform

from datetime import datetime

from client import slash, GUILD_IDS

from discord import Embed, Color
from discord_slash import SlashContext


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