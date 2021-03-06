import discord
import neverSleep
from discord.ext import commands
import os
import asyncio
import sys

neverSleep.awake("https://howbot.idrklol.repl.co", False)

intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix=".", intents=intents)
client.remove_command("help")
cogs = ["events.on_message"]


def restart_bot():
    os.execv(sys.executable, ['python'] + sys.argv)


@client.command(aliases=["reboot", "reload"])
@commands.has_permissions(administrator=True)
async def restart(ctx):
    await ctx.reply("Success")
    await print('-' * 10 + f'\nRestarting\n' + '-' * 10)
    restart_bot()


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
        f'{member.mention} joined this server :O\nRemember, you can\'t leave', delete_after=60)
    await member.send(
        f'Welcome to **{guild.name}**, {member.name}!\njust to make things clear, you\'ll die if you leave\nhttps://discord.gg/T5BZayunBB'
    )
    await general.send(f'{member.mention} just joined, say hi!')
    await verify.send(
        f'welcome {member.mention}!\nPlease react with ??? above to gain access to the server',
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
@commands.cooldown(1, 4, commands.BucketType.user)
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
@commands.cooldown(1, 4, commands.BucketType.user)
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
@commands.cooldown(1, 4, commands.BucketType.user)
async def ping(ctx):
    await ctx.send(f'{round(client.latency * 1000)}ms')


@client.command(aliases=["av", "pfp"])
@commands.cooldown(1, 4, commands.BucketType.user)
async def avatar(ctx, member: discord.Member = None):
    if member == None:
        member = ctx.author

    avatar = member.avatar_url

    embed = discord.Embed(title=f'{member.name}\'s avatar',
                          description=f'[Download]({member.avatar_url})')
    embed.set_footer(
        text=f"Asked by {ctx.author.name}#{ctx.author.discriminator}")
    embed.set_image(url=avatar)
    await ctx.reply(embed=embed)


@client.command(aliases=["mc", "membercount"])
@commands.cooldown(1, 4, commands.BucketType.user)
async def members(ctx):
    member_count = len(ctx.guild.members)
    user_count = len([m for m in ctx.guild.members if not m.bot])
    msg = f"all: `{member_count}`\nusers: `{user_count}`"
    await ctx.reply(msg)


@client.command(pass_context=True, aliases=["clear", "purge"])
@commands.has_permissions(administrator=True)
@commands.cooldown(1, 4, commands.BucketType.user)
async def clean(ctx, limit: int):
    await ctx.channel.purge(limit=limit + 1)
    await ctx.send(f'{ctx.author.mention} purged {limit} messages',
                   delete_after=5)
    await ctx.message.delete()


@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason='Unspecified'):
    if member.id == ctx.author.id:
        await ctx.send("You cannot ban yourself")
        return

    if member.top_role >= ctx.author.top_role:
        await ctx.send(f"You can only ban members below your top role")
        return

    embed = discord.Embed(
        title=f'***Banned `{member}` for `{reason}`***', color=0x38805d)
    await member.ban(reason=reason)
    await ctx.send(embed=embed, delete_after=10)
    await ctx.message.delete()


@client.command()
@commands.has_permissions(administrator=True)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split("#")

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned `{member}`', delete_after=10)
            await ctx.message.delete()
            return


@client.command(description="Mute command yay!!", aliases=["shut"])
@commands.has_permissions(manage_messages=True)
async def mute(ctx, member: discord.Member, *, reason='Unspecified'):
    if member.id == ctx.author.id:
        await ctx.send("You cannot mute yourself")
        return

    if member.top_role >= ctx.author.top_role:
        await ctx.send(f"You can only mute members below your top role")
        return
    guild = ctx.guild
    mutedRole = discord.utils.get(guild.roles, name="Muted")

    if not mutedRole:
        mutedRole = await guild.create_role(name="Muted")

        for channel in guild.channels:
            await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True, read_messages=False)

    await member.add_roles(mutedRole, reason=reason)
    embed = discord.Embed(title=f'Muted `{member}` for `{reason}`')
    await ctx.send(embed=embed, delete_after=10)
    await member.send(f"You were muted in `{guild.name}` for `{reason}`. DM a staff/owner if you feel this is unjustified")
    await ctx.message.delete()


@client.command(description="Unmute command yay!!")
@commands.has_permissions(manage_messages=True)
async def unmute(ctx, member: discord.Member):
    mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")

    await member.remove_roles(mutedRole)
    embed = discord.Embed(title=f'Unmuted `{member}`')
    await ctx.send(embed=embed, delete_after=10)
    await member.send(f"You were unmuted in `{ctx.guild.name}`")
    await ctx.message.delete()


@client.command(aliases=["abt", 'whois', 'who', 'ui', 'about'], description="Gets info about the user")
async def userinfo(ctx, *, member:discord.Member = None):
    if member == None:
            member = ctx.message.author

    embed=discord.Embed(
      title=f'{member}'
      )
    embed.set_thumbnail(url=member.avatar_url)
    embed.add_field(name="Name", value=f'`{member.name}`')
    embed.add_field(name="Nickname", value=f'`{member.nick}`')
    embed.add_field(name="ID", value=f'`{member.id}`')
    embed.add_field(name="Account Created",value=f'<t:{int(member.created_at.timestamp())}>')
    embed.add_field(name="Joined",value=f'<t:{int(member.joined_at.timestamp())}>')
    members = sorted(ctx.guild.members, key=lambda m: m.joined_at)
    embed.add_field(name="Join Position", value=f'`{str(members.index(member)+1)}`')
    await ctx.send(embed=embed)
  
  
client.run(os.environ['token'])