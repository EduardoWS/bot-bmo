import discord
from discord.ext import commands
import random
from time import sleep
import json
import os
import asyncio

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
    else:
        await ctx.send('Canal errado, bobinho(a)!')


@client.command()
async def d(ctx, numero):
    channel = ctx.channel
    if channel.name == '🎲┃comandos':
        rodar = random.randint(1, int(numero))
        await ctx.send('Rodando...')
        sleep(2)
        await ctx.send(f'`DADO = [{rodar}]`')
    else:
        await ctx.send('Canal errado, bobinho(a)!')

@client.command()
async def rpg(ctx):
    emb = discord.Embed(
        title = 'Comandos RPG:',
        description = '''
`!d [número]` 
BMO roda um dado com um número de lados escolhido
        ''',
        colour = 16715320
    )

    emb.set_author(name='BMO',
    icon_url='https://cdn.discordapp.com/attachments/831946320200728577/836261314837741619/bmopng.png')

    emb.set_thumbnail(url='https://cdn.discordapp.com/attachments/831946320200728577/836260807682686982/bimo.png')

    emb.set_image(url='https://media.giphy.com/media/10bxTLrpJNS0PC/giphy.gif')
    channel = ctx.channel
    if channel.name == '🎲┃comandos':
        await ctx.send(embed = emb)
    else:
        await ctx.send('Canal errado, bobinho(a)!')





@client.command()
async def ajuda(ctx):
    canal = client.get_channel(831196504618172437)
    canal2 = client.get_channel(835228205211189298)
    emb = discord.Embed(
        title = 'Meus comandos:',
        description = f'''
        `!oi` 
BMO diz Bom dia

`!rpg`
BMO mostra os comandos específicos da Categoria RPG. Só funciona no canal {canal2.mention}

`!ideia1`
BMO da dicas de desenhos fáceis. Só funciona no canal {canal.mention}

`!ideia2`
BMO da dicas de desenhos difíceis. Só funciona no canal {canal.mention}
''',    
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
    autor = ctx.author.name
    if autor == 'BerserkerWS':
        await ctx.send(f'O imperador disse para você pagar os impostos! {mention}')
    else:
        await ctx.send(f'Você não é o imperador!!')

@client.command()
async def ideia1(ctx):
    channel = ctx.channel
    if channel.name == '💡┃ideias-desenhos':
        ideias = ['Desenha uma árvore', 'Desenha um espantalho', 'Desenha o Finn', 'Desenha o Jake', 'Desenha a Marceline',
        'Desenha o BMO', 'Desenha o Rei Gelado', 'Desenhe o Tom e Jerry', 'Desenhe o Bob Esponja', 'Desenhe uma Pizza',
        'Desenhe um Sorvete', 'Desenhe o Pikachu', 'Desenhe o Mickey', 'Desenhe um Minion', 'Desenhe o Snoopy', 'Desenhe o Bart',
        'Desenhe um carro', 'Desenhe uma fruta', 'Desenhe um cacto', 'Desenhe uma rosquinha', 'Desenhe um campo de flores ou alguma flor',
        'Desenhe um céu com arco-íris', 'Desenhe uma boneca de pano', 'Desenhe uma paisagem com muitas árvores', 'Desenhe o Stitch',
        'Desenhe uma raposa', 'Desenhe a Dory', 'Desenhe o Nemo', 'Desenhe uma tartaruga', 'Desenhe uma águia', 'Desenhe um tubarão',
        'Desenhe um leão', 'Desenhe um polvo', 'Desenhe um cisne-negro', 'Desenha uma onça-pintada', 'Desenhe um urso', 'Desenhe uma cobra',
        'Desenhe o Garfield', 'Desenhe um gato', 'Desenha a Princesa de Fogo', 'Desenha o Finn e o Jake juntos', 'Desenha eu e a Marceline', 
        'Desenha o Lich']
        r1 = random.choice(ideias)
        mensagem = await channel.send(r1)
        channel.send(mensagem)
        await channel.send('`Essa mensagem será deletada em 60 segundos!`')
        await asyncio.sleep(60)
        await channel.send('`Mensagem deletada!`')
        await mensagem.delete()
        

    else:
        msg = await ctx.send('Canal errado, bobinho(a)!')


@client.command()
async def ideia2(ctx):
    channel = ctx.channel
    if channel.name == '💡┃ideias-desenhos':
        ideias = ['Faça uma caricatura de si mesmo(a)', 'Desenhe espelhos de diferentes ângulos',
        'Rascunhe você de super-heroína/super-herói', 'Tente desenhar a si mesmo(a) com o dobro da idade',
        'Rabisque um autorretrato no reflexo de uma colher', 'Ilustre a vista de uma janela',
        'Esboce as nuvens', 'Aproveite a perspectiva e trace a visão de cima de uma ponte ou de baixo de um penhasco',
        'Desenhe um objeto e, em seguida, coloque um rosto nele', 'Crie uma capa alternativa para seu livro ou álbum preferido',
        'Retrate uma cena para sua música favorita', 'Dê um rosto para o personagem de um livro que você ama',
        'Ilustre seu conto de fadas dos sonhos', 'Combine formas de animais e faça uma criatura mítica',
        'Transforme a cena de um sonho em um desenho', 'Crie sua própria logomarca', 'Desenhe todas as refeições que fizer ao longo da semana',
        'Escolha um objeto e o desenhe de formas diferentes por sete dias', 'Desenhe sapatos velhos',
        'Desenhe um copo de água', 'Desenhe uma cena em um restaurante', 'Desenhe garrafas de vinho',
        'Desenhe o seu animal de estimação favorito', 'Desenhe o rosto de uma pessoa idosa', 'Desenhe um carro velho',
        'Desenhe qualquer coisa feita de metal']
        r1 = random.choice(ideias)
        mensagem = await channel.send(r1)
        channel.send(mensagem)
        await channel.send('`Essa mensagem será deletada em 60 segundos!`')
        await asyncio.sleep(60)
        await channel.send('`Mensagem deletada!`')
        await mensagem.delete()
        

    else:
        msg = await ctx.send('Canal errado, bobinho(a)!')
        








@client.command()
@commands.has_permissions(ban_members=True)
async def banir(ctx, member: discord.Member, *, reason):
    channel = ctx.channel
    if channel.name == 'punições-comandos':
        await member.ban(reason=reason)
        channel = client.get_channel(831197248884703283)
        emb = discord.Embed(
        title = 'BANIDO(A)!!',
        description = f'{member.mention} foi executado pelos Guardas Reais.',
        colour = 16715320
    )

        emb.set_author(name='BMO',
        icon_url='https://cdn.discordapp.com/attachments/831946320200728577/836261314837741619/bmopng.png')

        emb.set_thumbnail(url='https://cdn.discordapp.com/attachments/831946320200728577/836260807682686982/bimo.png')

        emb.set_image(url='https://media.giphy.com/media/fe4dDMD2cAU5RfEaCU/giphy.gif')

        emb.add_field(name='Motivo:', value=f'{reason}', inline=True)
    


        await channel.send(embed = emb) #f'{member} foi banido!'

@client.command()
@commands.has_permissions(kick_members=True)
async def kickar(ctx, member: discord.Member, *, reason):
    channel = ctx.channel
    if channel.name == 'punições-comandos':
        await member.kick(reason=reason)
        channel = client.get_channel(831197248884703283)
        emb = discord.Embed(
        title = 'KICKADO(A)!!',
        description = f'{member.mention} foi expulso(a) do Reino Doce.',
        colour = 16715320
    )

        emb.set_author(name='BMO',
        icon_url='https://cdn.discordapp.com/attachments/831946320200728577/836261314837741619/bmopng.png')

        emb.set_thumbnail(url='https://cdn.discordapp.com/attachments/831946320200728577/836260807682686982/bimo.png')

        emb.set_image(url='https://media.giphy.com/media/u2LJ0n4lx6jF6/giphy.gif')

        emb.add_field(name='Motivo:', value=f'{reason}', inline=True)
    


        await channel.send(embed = emb) #f'{member.mention} foi kickado!'






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
