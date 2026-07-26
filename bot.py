import discord
from discord.ext import commands
import os

TOKEN = os.getenv("TOKEN")

KANAL_LOGOW = 1417656464209608704

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)

@bot.event
async def on_ready():
    print(f"✅ Bot działa jako {bot.user}")
    print("Serwery:", bot.guilds)

@bot.event
async def on_member_remove(member):
    kanal = bot.get_channel(KANAL_LOGOW)

    if kanal:
        await kanal.send(
            f"📤 **{member.name}** opuścił serwer."
        )

bot.run(TOKEN)
