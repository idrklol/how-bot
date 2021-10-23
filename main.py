import discord
import webserver
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix="w.", intents=intents)
client.remove_command("help")
cogs = ["events.on_message"]


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(
        type=discord.ActivityType.watching, name="you - dsc.gg/crocs"))
    print("i'm up :D")
    for cog in cogs:
        try:
            client.load_extension(cog)
            print(f"{cog} was loaded.")
        except Exception as e:
            print(e)

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please pass in all requirements')
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You dont have all the requirements xd")

@client.event
async def on_member_join(member):
    guild = client.get_guild(874440438604496976)
    channel = guild.get_channel(876101520297443388)
    general = guild.get_channel(876085929117352016)
    verify = guild.get_channel(876102248185339925)
    await channel.send(
        f'{member.mention} joined this server :O\nRemember, you can\'t leave')
    await member.send(
        f'Welcome to **{guild.name}**, {member.name}!\njust to make things clear, you\'ll die if you leave\nhttps://discord.gg/6MYX7qjVpw'
    )
    await general.send(f'{member.mention} just joined, say hi!')
    await verify.send(
        f'welcome {member.mention}!\nPlease react with ✅ above to gain access to the server',
        delete_after=10)


@client.event
async def on_member_remove(member):
    guild = client.get_guild(874440438604496976)
    channel = guild.get_channel(879118347088834620)
    await channel.send(
        f'Semeone just left...\nMay {member.name}#{member.discriminator} rest in peace.'
    )

@client.event
async def on_message(message):
    if message.content == 'w.hi':
        await message.channel.send('Hello :)')


webserver.keep_alive()

client.run(os.environ['token'])
