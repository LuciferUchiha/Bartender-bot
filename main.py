import os
import discord
from dotenv import load_dotenv

from bartender import Bartender

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv("DISCORD_GUILD")
KEYWORDS = ("$bt", "bartender", "god")

client = discord.Client()

@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(
        f"{client.user} is connected to the following guild:\n"
        f"{guild.name}(id: {guild.id})"
    )

@client.event
async def on_message(message):
    if message.author != client.user and message.content.lower().startswith(KEYWORDS):
        for prefix in KEYWORDS:
            message.content = message.content.removeprefix(prefix)
        await message.channel.send(Bartender().handle(message))



client.run(TOKEN)
