import discord
from discord.ext import commands
import random
from time import sleep

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
        `!bom dia` 
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


client.run('token')
