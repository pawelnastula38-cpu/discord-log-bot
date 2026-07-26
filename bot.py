import os
from threading import Thread

from flask import Flask
import discord
from discord.ext import commands


# ---------- SERWER HTTP DLA RENDERA ----------

app = Flask(__name__)


@app.route("/")
def home():
    return "Bot działa 24/7!"


def run_http():
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)


def keep_alive():
    server = Thread(target=run_http)
    server.daemon = True
    server.start()


# ---------- KONFIGURACJA BOTA ----------

TOKEN = os.getenv("TOKEN")

if not TOKEN:
    raise Exception("❌ Brak TOKEN! Dodaj TOKEN w Render → Environment Variables")


KANAL_LOGOW = 1417656464209608704


intents = discord.Intents.default()
intents.members = True


bot = commands.Bot(
    command_prefix="!",
    intents=intents
)


# ---------- ZDARZENIA ----------

@bot.event
async def on_ready():
    print(f"✅ Zalogowano jako: {bot.user}")
    print(f"🌐 Połączono z {len(bot.guilds)} serwerami")


@bot.event
async def on_member_remove(member):
    kanal = bot.get_channel(KANAL_LOGOW)

    if kanal:
        await kanal.send(
            f"📤 **{member.name}** opuścił serwer."
        )


# ---------- START ----------

keep_alive()

bot.run(TOKEN)
