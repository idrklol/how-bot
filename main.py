import discord
import neverSleep
from discord.ext import commands
import os
import asyncio

neverSleep.awake("https://howbot.idrklol.repl.co", False)

intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix=".", intents=intents)
client.remove_command("help")
cogs = ["events.on_message"]


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(
        type=discord.ActivityType.watching, name="you - .gg/bottle"))
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
        await ctx.send("You don't have permission to do that")


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
    global sn_author_name
    global snipe_message_id

    snipe_message_content = message.content
    snipe_message_author = message.author.id
    snipe_message_id = message.id
    sn_author_name = client.get_user(snipe_message_author)
    await asyncio.sleep(60)

    if message.id == snipe_message_id:
        snipe_message_author = None
        snipe_message_content = None
        snipe_message_id = None
        sn_author_name = None


@client.command()
async def snipe(message):
    if snipe_message_content == None:
        await message.channel.send("Couldn't find anything to snipe!")
    else:
        embed = discord.Embed(description=snipe_message_content)
        embed.set_footer(
            text=
            f"Asked by {message.author.name}#{message.author.discriminator}",
            icon_url=message.author.avatar_url)
        embed.set_author(name=f"{sn_author_name}")
        await message.channel.send(embed=embed)
        return


@client.command()
async def ping(ctx):
    await ctx.send(f'{round(client.latency * 1000)}ms')


@client.command(aliases=["av", "pfp"])
async def avatar(ctx, member: discord.Member = None):
    if member == None:
        member = ctx.author

    avatar = member.avatar_url

    embed = discord.Embed(title=f'{member.name}\'s avatar')
    embed.set_footer(
        text=f"Asked by {ctx.author.name}#{ctx.author.discriminator}")
    embed.set_image(url=avatar)
    await ctx.reply(embed=embed)


@client.command(aliases=["mc", "membercount"])
async def members(ctx):
    member_count = len(ctx.guild.members)
    user_count = len([m for m in ctx.guild.members if not m.bot])
    msg = f"all: `{member_count}`\nusers: `{user_count}`"
    await ctx.reply(msg)


@client.command(pass_context=True, aliases=["clear", "purge"])
@commands.has_permissions(administrator=True)
async def clean(ctx, limit: int):
    await ctx.channel.purge(limit=limit + 1)
    await ctx.send(f'{ctx.author.mention} purged {limit} messages',
                   delete_after=5)
    await ctx.message.delete()


client.run(os.environ['token'])
