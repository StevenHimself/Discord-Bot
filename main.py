#Author: Steven Montecinos

import discord
from discord import app_commands
from discord.ext import commands
import json
import os

if os.path.exists(os.getcwd() + "/config.json") :
    #pass //this is a dummy pass to generate a json file that will secure the bot's token
    with open("./config.json") as f:
        configData = json.load(f)
else:
    configTemplate = {"Token" : "", "Prefix" : "!"}

    with open(os.getcwd() + "/config.json", "w+") as f:
        json.dump(configTemplate, f)

token = configData["Token"]
prefix = configData["Prefix"]

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all(), application_id=1116698756046389300)

#startup
@bot.event
async def on_ready():
    print("Bot online, Beep Boop.")
    try:
        synced = await bot.tree.sync()
        print(f"Synced{len(synced)} command(s)")
    except Exception as e:
        print(e)

#commands
@bot.tree.command(name="rayjay")
async def rayjay(interaction: discord.Interaction):
    await interaction.response.send_message(f"Hey there little {interaction.user.mention}! it's Ray Jay time! RAYJAY RAYJAY RAYJAY")

@bot.tree.command(name="battlecry")
async def rayjay(interaction: discord.Interaction):
    await interaction.response.send_message(f"BROTHERS OF THE NORTHERN REGION JOIN ME INTO BATTLE TO BREAK FATHER CALEB'S LEGS!!!  ...both of them")

@bot.tree.command(name="say")
@app_commands.describe(thing_to_say= "user input")
async def say(interaction: discord.Interaction, thing_to_say: str):
    await interaction.response.send_message(f"{interaction.user.name} said: {thing_to_say}")

bot.run(token)

