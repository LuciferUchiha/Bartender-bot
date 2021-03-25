import os
import json
import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
KEYWORD = '$bt'

client = discord.Client()

with open('recipes.json') as recipes_file:
    recipes = json.load(recipes_file)

with open('ingredients.json') as ingredients_file:
    ingredients = json.load(ingredients_file)

@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

@client.event
async def on_message(message):
    if message.author != client.user and message.content.startswith(KEYWORD):
        await message.channel.send('Hello, I am your bartender')



client.run(TOKEN)
