#Author: Steven Montecinos

import discord, aiohttp, json, os
from discord import app_commands
from discord.ext import commands

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
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)

#text based commands
@bot.tree.command(name="rayjay")
async def rayjay(interaction: discord.Interaction):
    await interaction.response.send_message(f"Hey there little {interaction.user.mention}! it's Ray Jay time! RAYJAY RAYJAY RAYJAY")

@bot.tree.command(name="battlecry")
async def battlecry(interaction: discord.Interaction):
    await interaction.response.send_message(f"{interaction.user.mention} BROTHERS OF THE NORTHERN REGION JOIN ME INTO BATTLE TO BREAK FATHER CALEB'S LEGS!!!  ...both of them")

@bot.tree.command(name="littlegirl")
async def littlegirl(interaction: discord.Interaction):
    await interaction.response.send_message(f"{interaction.user.mention} OH MY GOODNESS!")

@bot.tree.command(name="say")
@app_commands.describe(thing_to_say= "user input")
async def say(interaction: discord.Interaction, thing_to_say: str):
    await interaction.response.send_message(f"{interaction.user.name} said: {thing_to_say}")


#image based commands
@bot.tree.command(name="cat", description="Generates a random cat pic")
@app_commands.checks.cooldown(1,5,key = lambda i : (i.user.id))
async def cat_pic(interaction : discord.Interaction) : 
    await interaction.response.defer
    async with aiohttp.ClientSession() as session:
        async with session.get('https://api.thecatapi.com/v1/images/search') as response:
            raw = await response.text()
            cat = json.loads(raw)[0]
            embed = discord.Embed(title="Cat", color=discord.Colour.green())
            embed.set_image(url= cat['url'])
            await interaction.followup.send(embed=embed)

@bot.tree.command(name="dog", description="Generates a random dog pic")
@app_commands.checks.cooldown(1,5,key = lambda i : (i.user.id))
async def dog_pic(interaction : discord.Interaction) : 
    await interaction.response.send_message.defer
    async with aiohttp.ClientSession() as session:
        async with session.get('https://dog.ceo/api/breeds/image/random') as response:
            raw = await response.text()
            dog = json.loads(raw)[0]
            embed = discord.Embed(title="Dog", color=discord.Colour.green())
            embed.set_image(url= dog['url'])
            await interaction.followup.send(embed=embed)

@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error : app_commands.AppCommandError):
    if isinstance(error,app_commands.CommandOnCooldown):
        await interaction.response.send_message(error, ephemeral=True)
    else: raise error

bot.run(token)

