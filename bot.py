import os
from threading import Thread
from flask import Flask
import discord
from discord.ext import commands

# --- MAŁY SERWER HTTP DLA RENDERA ---
app = Flask("")


@app.route("/")
def home():
    return "Bot działa 24/7!"


def run_http():
    # Render automatycznie przekazuje port w zmiennej PORT
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)


def keep_alive():
    t = Thread(target=run_http)
    t.daemon = True
    t.start()


# ------------------------------------

TOKEN = os.getenv("TOKEN")

if not TOKEN:
    raise Exception("Brak TOKEN w zmiennych środowiskowych Render!")
KANAL_LOGOW = 1417656464209608704

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"✅ Bot działa jako {bot.user}")
    print("Serwery:", bot.guilds)


@bot.event
async def on_member_remove(member):
    kanal = bot.get_channel(KANAL_LOGOW)

    if kanal:
        await kanal.send(f"📤 **{member.name}** opuścił serwer.")


# Uruchamiamy serwer www tuż przed włączeniem bota
keep_alive()

bot.run(TOKEN)
