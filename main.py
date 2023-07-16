# Author: Steven Montecinos
import discord, aiohttp, json, os, emoji, wavelink
from discord import app_commands
from discord.ext import commands
from typing import Any
from wavelink import node

# creating json.config and securing token
if not os.path.exists(os.getcwd() + "/config.json"):
    configTemplate = {"TOKEN": "", "PREFIX": "!"}
    with open(os.getcwd() + "/config.json", "w+") as f:
        json.dump(configTemplate, f)
else:
    with open("./config.json") as f:
        configData = json.load(f)

# assigning external variables from config.json
token = configData["TOKEN"]
prefix = configData["PREFIX"]

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all(), application_id=1116698756046389300)


# startup
@bot.event
async def on_ready():
    print("Bot online, Beep Boop.")
    bot.loop.create_task(connect_nodes())  # HTTPS and websocket applications


@bot.event
async def on_wavelink_node_ready(node: wavelink.Node) -> None:
    print(f"Node <{node.id}> is ready")


async def connect_nodes():
    await bot.wait_until_ready()
    node: wavelink.Node = wavelink.Node(uri='http://lavalink.clxud.dev:2333', password='youshallnotpass')
    await wavelink.NodePool.connect(client=bot, nodes=[node])


class Player(wavelink.Player):
    def __init__(self, dj: discord.Member, *args: Any, **kwargs: Any):
        super().__init__()
        self.dj = dj
        self.queue = wavelink.Queue


# music based commands
@bot.command()
async def play(ctx: commands.Context, *, search: wavelink.YouTubeTrack):
    if not ctx.voice_client:
        vc: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
    else:
        vc: wavelink.Player = ctx.voice_client

    await vc.play(search)


@bot.command()
async def connect(ctx: commands.Context, *, channel: discord.VoiceChannel | None = None):
    try:
        channel = channel or ctx.author.voice.channel
    except AttributeError:
        return await ctx.send("No voice channel to connect to. Please either provide one or join one.")

    vc: wavelink.Player = await channel.connect(cls=wavelink.Player)
    return vc

@bot.command()
async def disconnect(ctx : commands.Context, *, channel: discord.VoiceChannel | None = None):
    vc = ctx.voice_client
    if vc:
        await vc.disconnect()
    else:
        await ctx.send("I am not connected to voice channel!")


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
@app_commands.describe(your_joke="user input")
async def say(interaction: discord.Interaction, your_joke: str):
    await interaction.response.send_message(f"Ay Ton' you hear what I said? I said {your_joke} HEH HEH")


@bot.tree.command(name="quote", description="Generates a random quote from multiple categories!")
@app_commands.checks.cooldown(1, 5, key=lambda i: i.user.id)
@app_commands.choices(categories=[app_commands.Choice(name="anger", value="anger"),
                                  app_commands.Choice(name="art", value="art"),
                                  app_commands.Choice(name="change", value="change"),
                                  app_commands.Choice(name="courage", value="courage"),
                                  app_commands.Choice(name="experience", value="experience"),
                                  app_commands.Choice(name="failure", value="failure"),
                                  app_commands.Choice(name="family", value="family"),
                                  app_commands.Choice(name="fear", value="fear"),
                                  app_commands.Choice(name="food", value="food"),
                                  app_commands.Choice(name="forgiveness", value="forgiveness"),
                                  app_commands.Choice(name="friendship", value="friendship"),
                                  app_commands.Choice(name="funny", value="funny"),
                                  app_commands.Choice(name="god", value="god"),
                                  app_commands.Choice(name="graduation", value="graduation"),
                                  app_commands.Choice(name="happiness", value="happiness"),
                                  app_commands.Choice(name="health", value="health"),
                                  app_commands.Choice(name="hope", value="hope"),
                                  app_commands.Choice(name="humor", value="humor"),
                                  app_commands.Choice(name="inspirational", value="inspirational"),
                                  app_commands.Choice(name="intelligence", value="intelligence"),
                                  app_commands.Choice(name="knowledge", value="knowledge"),
                                  app_commands.Choice(name="life", value="life"),
                                  app_commands.Choice(name="love", value="love"),
                                  app_commands.Choice(name="success", value="success"),
                                  ])
async def random_quote(interaction: discord.Interaction, categories: app_commands.Choice[str]):
    await interaction.response.defer()
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://api.api-ninjas.com/v1/quotes?category={categories.value}',
                               headers={'X-Api-Key': '26hgo+xM8kjRhaavCUsEgQ==dsGnrqp1zdGqwDYS'}) as response:
            raw = await response.text()
            quotemap = json.loads(raw)[0]
            quote = quotemap["quote"]
            author = quotemap["author"]
            category = quotemap["category"]
            match category:
                case "inspirational":
                    category += (emoji.emojize(":raised_fist:"))
                case "intelligence":
                    category += (emoji.emojize(":nerd_face:"))
                case "failure":
                    category += (emoji.emojize(":pensive_face:"))
                case "knowledge":
                    category += (emoji.emojize(":books:"))
                case "anger":
                    category += (emoji.emojize(":enraged_face:"))
                case "health":
                    category += (emoji.emojize(":hospital:"))
                case "humor":
                    category += (emoji.emojize(":face_with_tears_of_joy:"))
                case "funny":
                    category += (emoji.emojize(":rolling_on_the_floor_laughing:"))
                case "art":
                    category += (emoji.emojize(":artist_palette:"))
                case "love":
                    category += (emoji.emojize(":growing_heart:"))
                case "family":
                    category += (emoji.emojize(":family:"))
                case "fear":
                    category += (emoji.emojize(":face_screaming_in_fear:"))
                case "graduation":
                    category += (emoji.emojize(":graduation_cap:"))
                case "hope":
                    category += (emoji.emojize(":pleading_face:"))
                case "success":
                    category += (emoji.emojize(":check_mark_button:"))
                case "change":
                    category += (emoji.emojize(":exclamation_question_mark:"))
                case "friendship":
                    category += (emoji.emojize(":handshake:"))
                case "forgiveness":
                    category += (emoji.emojize(":person_bowing:"))
                case "food":
                    category += (emoji.emojize(":fork_and_knife:"))
                case "life":
                    category += (emoji.emojize(":seedling:"))
                case "courage":
                    category += (emoji.emojize(":person_fencing:"))
                case "experience":
                    category += (emoji.emojize(":old_man:"))

            await interaction.followup.send(f"**Category**: {category.upper()}\n\n*{quote}*\n***-{author}***")


# image/gif based commands
@bot.tree.command(name="cat", description="Generates a random cat image/gif")
@app_commands.checks.cooldown(1, 5, key=lambda i: (i.user.id))
async def cat_pic(interaction: discord.Interaction):
    await interaction.response.defer()
    async with aiohttp.ClientSession() as session:
        async with session.get('https://api.thecatapi.com/v1/images/search') as response:
            raw = await response.text()
            cat = json.loads(raw)[0]
            embed = discord.Embed(title=emoji.emojize("meow! :grinning_cat:"), color=discord.Colour.purple())
            embed.set_image(url=cat['url'])
            await interaction.followup.send(embed=embed)


@bot.tree.command(name="dog", description="Generates a random dog image/gif")
@app_commands.checks.cooldown(1, 5, key=lambda i: i.user.id)
async def dog_pic(interaction: discord.Interaction):
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


bot.run(token)
