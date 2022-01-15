import discord
import webserver
from discord.ext import commands
import os
import asyncio
import random

intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix="w.", intents=intents)
client.remove_command("help")
cogs = ["events.emote_thingy"]


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
async def on_message(message):
    if message.content == 'w.hi':
        await message.channel.send('Hello :)')
    await client.process_commands(message)


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
        f'Welcome to **{guild.name}**, {member.name}!\njust to make things clear, you\'ll die if you leave\nhttps://discord.gg/T5BZayunBB'
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
        f'Someone just left...\nMay {member.name}#{member.discriminator} rest in peace.'
    )

snipe_message_content = None
snipe_message_author = None
snipe_message_id = None

@client.event
async def on_message_delete(message):

    global snipe_message_content
    global snipe_message_author
    global snipe_message_id

    snipe_message_content = message.content
    snipe_message_author = message.author.id
    snipe_message_id = message.id
    await asyncio.sleep(60)

    if message.id == snipe_message_id:
        snipe_message_author = None
        snipe_message_content = None
        snipe_message_id = None

@client.command()
async def snipe(message):
    if snipe_message_content==None:
        await message.channel.send("Couldn't find anything to snipe!")
    else:
        embed = discord.Embed(description=f"`Author:` <@{snipe_message_author}> \n `Message:` \n {snipe_message_content}")
        embed.set_footer(text=f"Asked by {message.author.name}#{message.author.discriminator}", icon_url=message.author.avatar_url)
        embed.set_author(name= f"Sniped!")
        await message.channel.send(embed=embed)
        return

webserver.keep_alive()

client.run(os.environ['token'])
