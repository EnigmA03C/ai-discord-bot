import os
import discord
from discord.ext import commands
import json
import logging

with open("src/config/data.json", "r") as file:
    config = json.load(file)

token = config["token"]

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.voice_states = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print("Logged in as")
    print(bot.user.name)
    print(bot.user.id)
    print("----------")
    print("Discord.py version")
    print(discord.__version__)
    print("----------")


async def load_cogs():
    # Loading Bot modules
    for filename in os.listdir("src/cogs"):
        if filename.endswith(".py") and filename != "__init__.py":
            await bot.load_extension(f"cogs.{filename[:-3]}")


async def main():
    async with bot:
        logging.basicConfig(
            level=logging.DEBUG, filename="src/data/discord.log", filemode="w"
        )
        await load_cogs()
        await bot.start(token=token)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
