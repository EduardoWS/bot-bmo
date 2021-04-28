import discord
from discord.ext import commands
import random
from time import sleep
import json
import os

if os.path.exists(os.getcwd() + "/config.json"):
    with open("./config.json") as f:
        configData = json.load(f)
else:
    configTemplate = {"Token": "", "Prefix": "!"}

    with open(os.getcwd() + "/config.json", "w+") as f:
        json.dump(configTemplate, f)

token = configData["Token"]
prefix = configData["Prefix"]

intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix = '!', case_insensitive = True, intents = intents)

@client.event
async def on_ready():
    print('BMO está ON !!!')




@client.command()
async def oi(ctx):
    channel = ctx.channel
    if channel.name == '🤖┃bots':
        await ctx.send(f'Bom dia, {ctx.author.mention}!') 


@client.command()
async def d(ctx, numero):
    channel = ctx.channel
    if channel.name == 'comandos':
        rodar = random.randint(1, int(numero))
        await ctx.send('Rodando...')
        sleep(2)
        await ctx.send(f'`DADO = [{rodar}]`')

@client.command()
async def ajuda(ctx):
    emb = discord.Embed(
        title = 'Meus comandos:',
        description = '''
        `!oi` 
BMO diz Bom dia

`!d [número]` 
BMO roda um dado com um número de lados escolhido''',
        colour = 16715320
    )

    emb.set_author(name='BMO',
    icon_url='https://cdn.discordapp.com/attachments/831946320200728577/836261314837741619/bmopng.png')

    emb.set_thumbnail(url='https://cdn.discordapp.com/attachments/831946320200728577/836260807682686982/bimo.png')

    emb.set_image(url='https://media.giphy.com/media/10bxTLrpJNS0PC/giphy.gif')
    await ctx.send(embed = emb)

@client.command()
async def ping(ctx):
    latency = round(client.latency * 1000, 1)
    await ctx.send(f'Pong! {latency} ms')

@client.command()
async def imposto(ctx, mention):
    await ctx.send(f'O imperador disse para você pagar os impostos! {mention}')


@client.command()
@commands.has_permissions(ban_members=True)
async def banir(ctx, member: discord.Member, *, reason=None):
    channel = ctx.channel
    if channel.name == 'punições-comandos':
        await member.ban(reason=reason)
        channel = client.get_channel(831197248884703283)
        await channel.send(f'{member} foi banido!')

@client.command()
@commands.has_permissions(kick_members=True)
async def kickar(ctx, member: discord.Member, *, reason=None):
    channel = ctx.channel
    if channel.name == 'punições-comandos':
        await member.kick(reason=reason)
        channel = client.get_channel(831197248884703283)
        await channel.send(f'{member.mention} foi kickado!')

@client.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, member):
    bannedUsers = await ctx.guild.bans()
    name, discrimator = member.split('#')

    for ban in bannedUsers:
        user = ban.user

        if(user.name, user.discrimator) == (name, discrimator):
            await ctx.guild.unban(user)
            await ctx.send(f'{user.mention} foi desbanido')
            return







client.run('token')
