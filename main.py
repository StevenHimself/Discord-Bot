# Author: Steven Montecinos

import discord, aiohttp, json, os, emoji
from discord import app_commands
from discord.ext import commands

#creating json.config and securing token
if not os.path.exists(os.getcwd() + "/config.json"):
    configTemplate = {"TOKEN": "", "PREFIX": "!"}
    with open(os.getcwd() + "/config.json", "w+") as f:
        json.dump(configTemplate, f)
else:
    with open("./config.json") as f:
        configData = json.load(f)
    
#assigning external variables from config.json
token = configData["TOKEN"]
prefix = configData["PREFIX"]

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all(), application_id=1116698756046389300)


# startup
@bot.event
async def on_ready():
    print("Bot online, Beep Boop.")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)


# text based commands
@bot.tree.command(name="rayjay", description="It's going to be RayJay time!")
async def rayjay(interaction: discord.Interaction):
    await interaction.response.send_message(
        f"Hey there little {interaction.user.mention}! it's Ray Jay time! RAYJAY RAYJAY RAYJAY")


@bot.tree.command(name="battlecry", description="Join Dustin into battle!")
async def battlecry(interaction: discord.Interaction):
    await interaction.response.send_message(
        f"BROTHERS OF THE NORTHERN REGION JOIN ME INTO BATTLE TO BREAK FATHER CALEB'S LEGS!!!  ...both of them")


@bot.tree.command(name="littlegirl", description="Steph's catchphrase")
async def littlegirl(interaction: discord.Interaction):
    await interaction.response.send_message(f"{interaction.user.mention} OH MY GOODNESS!")


@bot.tree.command(name="say", description="Repeats your input")
@app_commands.describe(thing_to_say="user input")
async def say(interaction: discord.Interaction, thing_to_say: str):
    await interaction.response.send_message(f"{interaction.user.name} said: {thing_to_say}")


@bot.tree.command(name="pauliejoke", description="Repeats your joke with a Sopranos twist!")
@app_commands.describe(paulie_joke="user input")
async def say(interaction: discord.Interaction, paulie_joke: str):
    await interaction.response.send_message(f"Ay Ton' you hear what I said? I said {paulie_joke} HEH HEH")


@bot.tree.command(name="quote", description="Generates a random quote!")
@app_commands.checks.cooldown(1, 5, key=lambda i: (i.user.id))
async def quote(interaction: discord.Interaction, category: str):
    await interaction.response.defer()
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://api.api-ninjas.com/v1/quotes?category={category}', headers={'X-Api-Key' : '26hgo+xM8kjRhaavCUsEgQ==dsGnrqp1zdGqwDYS'}) as response:
            raw = await response.text()
            quotemap = json.loads(raw)[0]
            quote = quotemap["quote"]
            author = quotemap["author"]
            category = quotemap["category"]
            match category:
                case "happiness":
                    category = " ".join(emoji.emojize(":grinning_face:"))
                case "birthday":
                    category = " ".join(emoji.emojize(":birthday_cake:"))
                case "inspirational":
                    category = " ".join(emoji.emojize(":raised_fist:"))
                case "death":
                    category = " ".join(emoji.emojize(":skull:"))
                case "alone":
                    category = " ".join(emoji.emojize(":crying_face:"))
                case "intelligence":
                    category = " ".join(emoji.emojize(" " + ":nerd_face:"))
                case "movies":
                    category = " ".join(emoji.emojize(":clapper_board:"))
                case "failure":
                    category = " ".join(emoji.emojize(":pensive_face:"))
                case "knowledge":
                    category = " ".join(emoji.emojize(":books:"))
                case "love":
                    category = " ".join(emoji.emojize(":growing_heart:"))
            await interaction.followup.send(f"\n**Category**: {category.upper()}\n\n*{quote}*\n***-{author}***")


# image/gif based commands
@bot.tree.command(name="cat", description="Generates a random cat image/gif")
@app_commands.checks.cooldown(1, 5, key=lambda i: (i.user.id))
async def catpic(interaction: discord.Interaction):
    await interaction.response.defer()
    async with aiohttp.ClientSession() as session:
        async with session.get('https://api.thecatapi.com/v1/images/search') as response:
            raw = await response.text()
            cat = json.loads(raw)[0]
            embed = discord.Embed(title=emoji.emojize("meow! :grinning_cat:"), color=discord.Colour.purple())
            embed.set_image(url=cat['url'])
            await interaction.followup.send(embed=embed)


@bot.tree.command(name="dog", description="Generates a random dog image/gif")
@app_commands.checks.cooldown(1, 5, key=lambda i: (i.user.id))
async def dogpic(interaction: discord.Interaction):
    await interaction.response.defer()
    async with aiohttp.ClientSession() as session:
        async with session.get('https://dog.ceo/api/breeds/image/random') as response:
            raw = await response.text()
            dog = json.loads(raw)
            embed = discord.Embed(title=emoji.emojize("woof! :dog_face:"), color=discord.Colour.green())
            embed.set_image(url=dog['message'])
            await interaction.followup.send(embed=embed)


@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.CommandOnCooldown):
        await interaction.response.send_message(error, ephemeral=True)
    else:
        raise error


# TODO:music based commands

bot.run(token)
