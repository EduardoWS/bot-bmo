import discord
from discord.ext import commands, tasks
import random
import time
from time import sleep
import json
import os
import asyncio
import sqlite3
from sqlite3 import Error
import psycopg2 as db



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
client.remove_command('help')






@client.event
async def on_ready():
    print('BMO está ON !!!')

    await client.change_presence(activity=discord.Game(name='os outros pela janela'))

@client.command()
@commands.has_permissions(administrator=True)
async def activity(ctx, *, activity):
    await client.change_presence(activity=discord.Game(name=activity))
    await ctx.send(f'Status atualizado para: `Jogando {activity}`')







# VV ====================== BANCO DE DADOS ====================== VV

def conexaom():
    con = None
    try:
        con = sqlite3.connect('monopoly.db')
    except Error as ex:
        print(ex)
    return con 


#---------------- INSERIR ----------------
def inserir(conexao, sql):
    try:
        c = conexao.cursor()
        c.execute(sql)
        conexao.commit()
    except Error as ex:
        print(ex)

@client.command()
async def insertt(ctx, dinheiro, member: discord.Member):
    vcon = conexaom()
    member = member.id
    vsql = f"""INSERT INTO banco_dinheiro
            (N_DINHEIRO, N_IDUSER)
            VALUES({dinheiro}, {member})
            """
    inserir(vcon, vsql)
    await ctx.send('Valores inseridos com sucesso!') 

#---------------- DELETAR ----------------
def deletar(conexao, sql):
    try:
        c = conexao.cursor()
        c.execute(sql)
        conexao.commit()
    except Error as ex:
        print(ex)

@client.command()
async def delet(ctx, idu):
    vcon = conexaom()
    vsql = f"DELETE FROM banco_dinheiro WHERE N_ID={idu}"
    deletar(vcon, vsql)
    await ctx.send(f'A conta {idu} foi deletada com sucesso!')

@client.command()
async def deletall(ctx):
    vcon = conexaom()
    vsql = f"DELETE FROM banco_dinheiro"
    deletar(vcon, vsql)
    await ctx.send(f'As contas foram deletadas com sucesso!')

#---------------- UPDATE ----------------
def atualizar(conexao, sql):
    try:
        c = conexao.cursor()
        c.execute(sql)
        conexao.commit()
    except Error as ex:
        print(ex)

@client.command()
async def updat(ctx, dinheiro):
    vcon = conexaom()
    vsql = f"UPDATE banco_dinheiro SET N_DINHEIRO={dinheiro} WHERE N_SENHA={senha}"
    deletar(vcon, vsql)
    await ctx.send(f'A conta foi atualizada com sucesso!') 

#---------------- SELECT ----------------
def consulta(conexao, sql):
    
    c = conexao.cursor()
    c.execute(sql)
    global resultado
    resultado = c.fetchone()
    return resultado

@client.command()
async def banco(ctx, member: discord.Member):
    vcon = conexaom()
    member = member.id 
    vsql = (f"SELECT N_IDUSER FROM banco_dinheiro WHERE N_IDUSER = {member}")
    
    try:
        res = consulta(vcon, vsql)
        if resultado[0] == None:
            pass

    except:
        await ctx.send('Você não tem uma conta criada!')
    else:
        await ctx.send('Conta encontrada!')
        for r in res:
            await ctx.send(r)







# VV ====================== ECONOMIA ====================== VV

@client.command()
async def criarconta(ctx):
    vcon = conexaom()
    autor = ctx.author.id
    nome = ctx.author.name
    criar = f"""INSERT INTO banco_dinheiro
            (N_DINHEIRO, N_IDUSER, T_NOME)
            VALUES('100', '{autor}', '{nome}')
            """
    
    vsql = (f"SELECT N_IDUSER FROM banco_dinheiro WHERE N_IDUSER = {autor}")

    try:
        
        if resultado[0] == None:
            pass
    except:
        inserir(vcon, criar)
        await ctx.send('Conta criada com sucesso! Use o comando `!mybank` para ver mais informações')
    else:
        await ctx.send('Você já tem uma conta! Use o comando `!mybank` para ver mais informações')
    

    
@client.command()
async def bank(ctx, member: discord.Member):
    connection = sqlite3.connect("monopoly.db")
    c = connection.cursor()
    vsql = ("SELECT N_IDUSER, N_DINHEIRO FROM banco_dinheiro WHERE N_IDUSER = ?")
    val = (member.id, )
    c.execute(vsql, val)
    resultado = c.fetchmany()

    
    try:
        if resultado[0] == None:
            pass
    except:
        await ctx.send(f'Essa pessoa não tem uma conta criada!')
    else:
        for r in resultado:
            idu = r[0]
            saldo = r[1]

        emb = discord.Embed(
        title = 'BANK:',
        description = f'''
Nome: `{member.name}`

ID da conta: ||`{idu}`||

Saldo: `{saldo} Cookies`
        ''',
        colour = 16715320
        )

        emb.set_author(name='BMO',
        icon_url='https://cdn.discordapp.com/attachments/831946320200728577/836261314837741619/bmopng.png')

        emb.set_thumbnail(url=member.avatar_url)
        await ctx.send(embed = emb)


@client.command()
async def mybank(ctx):
    connection = sqlite3.connect("monopoly.db")
    c = connection.cursor()
    vsql = ("SELECT N_IDUSER, N_DINHEIRO FROM banco_dinheiro WHERE N_IDUSER = ?")
    val = (ctx.author.id, )
    c.execute(vsql, val)
    resultado = c.fetchmany()

    nome = ctx.author.name
    try:
        if resultado[0] == None:
            pass
    except:
        await ctx.send('Você não tem uma conta criada! Crie uma conta com `!criarconta`')
    else:
        for r in resultado:
            idu = r[0]
            saldo = r[1]

        emb = discord.Embed(
        title = 'BANK:',
        description = f'''
Nome: `{nome}`

ID da conta: ||`{idu}`||

Saldo: `{saldo} Cookies`
        ''',
        colour = 16715320
        )

        emb.set_author(name='BMO',
        icon_url='https://cdn.discordapp.com/attachments/831946320200728577/836261314837741619/bmopng.png')

        emb.set_thumbnail(url=ctx.author.avatar_url)
        await ctx.send(embed = emb)

 






@client.command()
async def pay(ctx, quant, member: discord.Member):
    connection = sqlite3.connect("monopoly.db")
    c = connection.cursor()

    pagar = f"""INSERT INTO banco_dinheiro
            (N_DINHEIRO, N_IDUSER)
            VALUES(?, ?)
            """
    pag = (quant, member.id)

    vsql = (f"SELECT N_IDUSER, N_DINHEIRO FROM banco_dinheiro WHERE N_IDUSER = ?")
    val = (member.id,)
    c.execute(vsql, val)
    resultado = c.fetchmany()
    try:
        if resultado[0] == None:
            pass
    except:
        await ctx.send(f'Essa pessoa não tem uma conta criada!')
    else:
        for r in resultado:
            idu = r[0]
            saldo = r[1]
            
        
        vsql2 = ("SELECT N_IDUSER, N_DINHEIRO FROM banco_dinheiro WHERE N_IDUSER = ?")
        val2 = (ctx.author.id,)
        c.execute(vsql2, val2)
        resultado2 = c.fetchmany()
        try:
            if resultado2[0] == None:
                pass
        except:
            await ctx.send(f'Você não tem uma conta criada! Crie uma conta com `!criarconta`')
        else:
            for r in resultado2:
                idu2 = r[0]
                saldo2 = r[1]
            if saldo2 < int(quant):
                await ctx.send('Cookies insuficientes!')
            else:
                vcon = conexaom()
                total = saldo + int(quant)
                total2 = saldo2 - int(quant)
                updt = ("UPDATE banco_dinheiro SET N_DINHEIRO=? WHERE N_IDUSER=?")
                up = (total, member.id)
                c = vcon.cursor()
                c.execute(updt, up)
                vcon.commit()
                
                
                updt2 = ("UPDATE banco_dinheiro SET N_DINHEIRO=? WHERE N_IDUSER=?")
                up2 = (total2, ctx.author.id)
                c = vcon.cursor()
                c.execute(updt2, up2)
                vcon.commit()
                await ctx.send(f'Transação realizada com sucesso! Novo saldo: `{total2} cookies`')





















# VV ====================== TASKS LOOP ====================== VV

@client.command()
async def loop(ctx, enabled='start', interval=10, message=""):
    if enabled.lower() == 'stop':
        msg.cancel()
    elif enabled.lower() == 'start':
        msg.change_interval(seconds=int(interval))
        msg.start(ctx, message)


@tasks.loop(seconds=10)
async def msg(ctx, message):
    await ctx.send(message)














# VV ====================== COMANDOS EXCLUSIVOS DA CATEGORIA RPG ====================== VV

@client.command()
async def rodar(ctx, dado):
    fd = dado.find('d')
    num1 = dado[:fd]
    num2 = dado[fd+1:]
    cont = 0
    await ctx.send('Rodando...')
    sleep(2)
    for n in range(1, int(num1)+1):
        rd = random.randint(1, int(num2))
        cont += rd
        await ctx.send(f'`DADO = [{rd}]`')
        sleep(2)
    await ctx.send(f'`TOTAL = {cont}`')





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

    """ emb.set_image(url='https://media.giphy.com/media/10bxTLrpJNS0PC/giphy.gif') """
    channel = ctx.channel
    if channel.name == '🎲┃comandos':
        await ctx.send(embed = emb)
    else:
        await ctx.send('Canal errado, bobinho(a)!')












# VV ====================== COMANDO AJUDA EMBED ====================== VV

@client.command()
async def ajuda(ctx):
    canal = client.get_channel(831196504618172437)
    canal2 = client.get_channel(835228205211189298)
    emb = discord.Embed(
title = 'COMANDOS GERAIS:',
description = f'''

`!oi` 
BMO diz Bom dia

`!ping`
BMO mostra sua latência em ms

`!userinfo`
BMO mostra suas informações

`!ficha [@user]`
BMO mostra a ficha de @user

`!economia`
BMO lista todos os comandos da categoria "economia"

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

    """ emb.set_image(url='https://media.giphy.com/media/10bxTLrpJNS0PC/giphy.gif') """
    await ctx.send(embed = emb)

@client.command()
async def economia(ctx):
    emb = discord.Embed(
title = 'COMANDOS ECONOMIA:',
description = f'''

`!criarconta` 
Cria uma conta no Bank

`!bank [@user]`
BMO mostra as informações do Bank de @user

`!mybank`
BMO mostra as informações do seu Bank

`!pay [quantidade] [@user]`
Transfere cookies para @user
''',


colour = 16715320
)

    emb.set_author(name='BMO',
    icon_url='https://cdn.discordapp.com/attachments/831946320200728577/836261314837741619/bmopng.png')

    emb.set_thumbnail(url='https://cdn.discordapp.com/attachments/831946320200728577/836260807682686982/bimo.png')

    
    await ctx.send(embed = emb)











@client.command()
async def adm(ctx):
    emb = discord.Embed(title='COMANDOS DE PUNIÇÕES', 
    description=f'''
    `!kickar [id] [motivo]`
    BMO expulsa um infrator do Reino Doce

    `!banir [id] [motivo]`
    BMO dá a ordem para a execução do criminoso

    `!unban [id]`
    BMO ressuscita uma pessoa das trevas

    `!mute03 [id] [motivo]`
    BMO silencia um plebeu por 30 minutos

    `!mute1 [id] [motivo]`
    BMO silencia um plebeu por 1 hora

    `!mute2 [id] [motivo]`
    BMO silencia um plebeu por 2 horas
    
    `!mute3 [id] [motivo]`
    BMO silencia um plebeu por 3 horas

    `!mute10 [id] [motivo]`
    BMO silencia um plebeu por 10 horas

    `!unmute [id]`
    BMO retira o silenciamento do plebeu''',

    colour = 16715320
    )

    emb.set_author(name='ADM',
    icon_url='https://cdn.discordapp.com/attachments/831946320200728577/836261314837741619/bmopng.png')

    emb.set_thumbnail(url='https://cdn.discordapp.com/attachments/831946320200728577/836260807682686982/bimo.png')
    channel = ctx.channel
    if channel.name == 'administração':
        await ctx.send(embed = emb)
    






#VV ====================== EMBED INFOS ====================== VV

@client.command()
async def userinfo(ctx):
    user = ctx.author

    emb = discord.Embed(title='User INFO', description=f'Aqui está as infos sobre {user.mention}', colour=user.colour)
    emb.set_thumbnail(url=user.avatar_url)
    emb.add_field(name='NOME', value=f'`{user.name}`', inline=False)
    emb.add_field(name='APELIDO', value=f'`{user.nick}`', inline=False)
    emb.add_field(name='CARGO', value=f'`{user.top_role.name}`', inline=False)
   

   #data entrou no server
    hora = user.joined_at.hour
    if hora == 1:
        emb.add_field(name='ENTROU', value=f'`{user.joined_at.strftime(f"%d/%m/%Y às {hora + 21}:%M")}`', inline=False)
    elif hora == 2:
        emb.add_field(name='ENTROU', value=f'`{user.joined_at.strftime(f"%d/%m/%Y às {hora + 21}:%M")}`', inline=False)
    elif hora == 3:
        emb.add_field(name='ENTROU', value=f'`{user.joined_at.strftime(f"%d/%m/%Y às 0{hora -3}:%M")}`', inline=False)
    elif hora == 0:
        emb.add_field(name='ENTROU', value=f'`{user.joined_at.strftime(f"%d/%m/%Y às {hora + 21}:%M")}`', inline=False)
    else:
        emb.add_field(name='ENTROU', value=f'`{user.joined_at.strftime(f"%d/%m/%Y às {hora - 3}:%M")}`', inline=False)
    

    #data criação da conta
    horac = user.created_at.hour
    if horac == 1:
        emb.add_field(name='CONTA CRIADA EM', value=f'`{user.created_at.strftime(f"%d/%m/%Y às {horac + 21}:%M")}`', inline=False)
    elif horac == 2:
        emb.add_field(name='CONTA CRIADA EM', value=f'`{user.created_at.strftime(f"%d/%m/%Y às {horac + 21}:%M")}`', inline=False)
    elif horac == 3:
        emb.add_field(name='CONTA CRIADA EM', value=f'`{user.created_at.strftime(f"%d/%m/%Y às 0{horac - 3}:%M")}`', inline=False)
    elif horac == 0:
        emb.add_field(name='CONTA CRIADA EM', value=f'`{user.created_at.strftime(f"%d/%m/%Y às {horac + 21}:%M")}`', inline=False)
    else:
        emb.add_field(name='CONTA CRIADA EM', value=f'`{user.created_at.strftime(f"%d/%m/%Y às {horac - 3}:%M")}`', inline=False)

    emb.add_field(name='ID', value=f'`{user.id}`', inline=False)
    await ctx.send(embed = emb)




@client.command()
async def ficha(ctx, member: discord.Member):
    
    emb = discord.Embed(title='User INFO', description=f'Aqui está as infos sobre {member.mention}', colour=member.colour)
    emb.set_thumbnail(url=member.avatar_url)
    emb.add_field(name='NOME', value=f'`{member.name}`', inline=False)
    emb.add_field(name='APELIDO', value=f'`{member.nick}`', inline=False)
    emb.add_field(name='CARGO', value=f'`{member.top_role.name}`', inline=False)

    #data entrou no server
    hora = member.joined_at.hour
    if hora == 1:
        emb.add_field(name='ENTROU', value=f'`{member.joined_at.strftime(f"%d/%m/%Y às {hora + 21}:%M")}`', inline=False)
    elif hora == 2:
        emb.add_field(name='ENTROU', value=f'`{member.joined_at.strftime(f"%d/%m/%Y às {hora + 21}:%M")}`', inline=False)
    elif hora == 3:
        emb.add_field(name='ENTROU', value=f'`{member.joined_at.strftime(f"%d/%m/%Y às 0{hora - 3}:%M")}`', inline=False)
    elif hora == 0:
        emb.add_field(name='ENTROU', value=f'`{member.joined_at.strftime(f"%d/%m/%Y às {hora + 21}:%M")}`', inline=False)
    else:
        emb.add_field(name='ENTROU', value=f'`{member.joined_at.strftime(f"%d/%m/%Y às {hora - 3}:%M")}`', inline=False)
    

    #data criação da conta
    horac = member.created_at.hour
    if horac == 1:
        emb.add_field(name='CONTA CRIADA EM', value=f'`{member.created_at.strftime(f"%d/%m/%Y às {horac + 21}:%M")}`', inline=False)
    elif horac == 2:
        emb.add_field(name='CONTA CRIADA EM', value=f'`{member.created_at.strftime(f"%d/%m/%Y às {horac + 21}:%M")}`', inline=False)
    elif horac == 3:
        emb.add_field(name='CONTA CRIADA EM', value=f'`{member.created_at.strftime(f"%d/%m/%Y às 0{horac - 3}:%M")}`', inline=False)
    elif horac == 0:
        emb.add_field(name='CONTA CRIADA EM', value=f'`{member.created_at.strftime(f"%d/%m/%Y às {horac + 21}:%M")}`', inline=False)
    else:
        emb.add_field(name='CONTA CRIADA EM', value=f'`{member.created_at.strftime(f"%d/%m/%Y às {horac - 3}:%M")}`', inline=False)



    emb.add_field(name='ID', value=f'`{member.id}`', inline=False)
    await ctx.send(embed = emb)
















# VV ====================== OUTROS COMANDOS ====================== VV

@client.command()
async def oi(ctx):
    channel = ctx.channel
    if channel.name == '🤖┃bots':
        await ctx.send(f'Bom dia, {ctx.author.mention}!') 
    else:
        await ctx.send('Canal errado, bobinho(a)!')



@client.command()
async def ping(ctx):
    latency = round(client.latency * 1000, 1)
    await ctx.send(f'Pong! {latency} ms')


@client.command()
async def imposto(ctx, mention):
    autor = ctx.author.id
    if autor == 611235322411352107:
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
        




























#VV ====================== COMANDOS DE PUNIÇÕES ====================== VV

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

@client.command(description='Mutes the specified user.')
@commands.has_permissions(manage_messages=True)
async def mute03(ctx, member: discord.Member, *, reason=None):
    channel = ctx.channel
    if channel.name == 'punições-comandos':
        guild = ctx.guild
        mutedRole = discord.utils.get(guild.roles, name='Muted')

        if not mutedRole:
            mutedRole = await guild.create_role(name='Muted')

            for channel in guild.channels:
                await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True, read_messages=True)

        
        channel = client.get_channel(831197248884703283)
        emb = discord.Embed(
        title = 'SILENCIADO(A)!!',
        description = f'{member.mention} foi silenciado(a) do Reino Doce.',
        colour = 16715320
    )

        emb.set_author(name='BMO',
        icon_url='https://cdn.discordapp.com/attachments/831946320200728577/836261314837741619/bmopng.png')

        emb.set_thumbnail(url='https://cdn.discordapp.com/attachments/831946320200728577/836260807682686982/bimo.png')

        """ emb.set_image(url='https://media1.tenor.com/images/029763582b4705fa973c47e72ce8e9f5/tenor.gif?itemid=17302394') """

        emb.add_field(name='MOTIVO:', value=f'`{reason}`', inline=True)
        emb.add_field(name='TEMPO:', value='`30 minutos`')

        
        await channel.send(embed = emb)
        """ await ctx.send(f'{member.mention} foi silenciado por {reason}') """
        await member.send(f'Você foi silenciado(a) no {guild.name} por {reason}')
        await member.add_roles(mutedRole, reason=reason)
        await asyncio.sleep(1800)
        await channel.send(f'{member.mention} você pode voltar a falar agora!')
        await member.remove_roles(mutedRole)

@client.command(description='Mutes the specified user.')
@commands.has_permissions(manage_messages=True)
async def mute1(ctx, member: discord.Member, *, reason=None):
    channel = ctx.channel
    if channel.name == 'punições-comandos':
        guild = ctx.guild
        mutedRole = discord.utils.get(guild.roles, name='Muted')

        if not mutedRole:
            mutedRole = await guild.create_role(name='Muted')

            for channel in guild.channels:
                await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True, read_messages=True)

        
        channel = client.get_channel(831197248884703283)
        emb = discord.Embed(
        title = 'SILENCIADO(A)!!',
        description = f'{member.mention} foi silenciado(a) do Reino Doce.',
        colour = 16715320
    )

        emb.set_author(name='BMO',
        icon_url='https://cdn.discordapp.com/attachments/831946320200728577/836261314837741619/bmopng.png')

        emb.set_thumbnail(url='https://cdn.discordapp.com/attachments/831946320200728577/836260807682686982/bimo.png')

        """ emb.set_image(url='https://media1.tenor.com/images/029763582b4705fa973c47e72ce8e9f5/tenor.gif?itemid=17302394') """

        emb.add_field(name='MOTIVO:', value=f'`{reason}`', inline=True)
        emb.add_field(name='TEMPO:', value='`1 hora`')

        
        await channel.send(embed = emb)
        """ await ctx.send(f'{member.mention} foi silenciado por {reason}') """
        await member.send(f'Você foi silenciado(a) no {guild.name} por {reason}')
        await member.add_roles(mutedRole, reason=reason)
        await asyncio.sleep(3600)
        await channel.send(f'{member.mention} você pode voltar a falar agora!')
        await member.remove_roles(mutedRole)

@client.command(description='Mutes the specified user.')
@commands.has_permissions(manage_messages=True)
async def mute2(ctx, member: discord.Member, *, reason=None):
    channel = ctx.channel
    if channel.name == 'punições-comandos':
        guild = ctx.guild
        mutedRole = discord.utils.get(guild.roles, name='Muted')

        if not mutedRole:
            mutedRole = await guild.create_role(name='Muted')

            for channel in guild.channels:
                await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True, read_messages=True)

        
        channel = client.get_channel(831197248884703283)
        emb = discord.Embed(
        title = 'SILENCIADO(A)!!',
        description = f'{member.mention} foi silenciado(a) do Reino Doce.',
        colour = 16715320
    )

        emb.set_author(name='BMO',
        icon_url='https://cdn.discordapp.com/attachments/831946320200728577/836261314837741619/bmopng.png')

        emb.set_thumbnail(url='https://cdn.discordapp.com/attachments/831946320200728577/836260807682686982/bimo.png')

        """ emb.set_image(url='https://media1.tenor.com/images/029763582b4705fa973c47e72ce8e9f5/tenor.gif?itemid=17302394') """

        emb.add_field(name='MOTIVO:', value=f'`{reason}`', inline=True)
        emb.add_field(name='TEMPO:', value='`2 horas`')

        
        await channel.send(embed = emb)
        """ await ctx.send(f'{member.mention} foi silenciado por {reason}') """
        await member.send(f'Você foi silenciado(a) no {guild.name} por {reason}')
        await member.add_roles(mutedRole, reason=reason)
        await asyncio.sleep(7200)
        await channel.send(f'{member.mention} você pode voltar a falar agora!')
        await member.remove_roles(mutedRole)

@client.command(description='Mutes the specified user.')
@commands.has_permissions(manage_messages=True)
async def mute3(ctx, member: discord.Member, *, reason=None):
    channel = ctx.channel
    if channel.name == 'punições-comandos':
        guild = ctx.guild
        mutedRole = discord.utils.get(guild.roles, name='Muted')

        if not mutedRole:
            mutedRole = await guild.create_role(name='Muted')

            for channel in guild.channels:
                await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True, read_messages=True)

        
        channel = client.get_channel(831197248884703283)
        emb = discord.Embed(
        title = 'SILENCIADO(A)!!',
        description = f'{member.mention} foi silenciado(a) do Reino Doce.',
        colour = 16715320
    )

        emb.set_author(name='BMO',
        icon_url='https://cdn.discordapp.com/attachments/831946320200728577/836261314837741619/bmopng.png')

        emb.set_thumbnail(url='https://cdn.discordapp.com/attachments/831946320200728577/836260807682686982/bimo.png')

        """ emb.set_image(url='https://media1.tenor.com/images/029763582b4705fa973c47e72ce8e9f5/tenor.gif?itemid=17302394') """

        emb.add_field(name='MOTIVO:', value=f'`{reason}`', inline=True)
        emb.add_field(name='TEMPO:', value='`3 horas`')

        
        await channel.send(embed = emb)
        """ await ctx.send(f'{member.mention} foi silenciado por {reason}') """
        await member.send(f'Você foi silenciado(a) no {guild.name} por {reason}')
        await member.add_roles(mutedRole, reason=reason)
        await asyncio.sleep(10800)
        await channel.send(f'{member.mention} você pode voltar a falar agora!')
        await member.remove_roles(mutedRole)

@client.command(description='Mutes the specified user.')
@commands.has_permissions(manage_messages=True)
async def mute10(ctx, member: discord.Member, *, reason=None):
    channel = ctx.channel
    if channel.name == 'punições-comandos':
        guild = ctx.guild
        mutedRole = discord.utils.get(guild.roles, name='Muted')

        if not mutedRole:
            mutedRole = await guild.create_role(name='Muted')

            for channel in guild.channels:
                await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True, read_messages=True)

        
        channel = client.get_channel(831197248884703283)
        emb = discord.Embed(
        title = 'SILENCIADO(A)!!',
        description = f'{member.mention} foi silenciado(a) do Reino Doce.',
        colour = 16715320
    )

        emb.set_author(name='BMO',
        icon_url='https://cdn.discordapp.com/attachments/831946320200728577/836261314837741619/bmopng.png')

        emb.set_thumbnail(url='https://cdn.discordapp.com/attachments/831946320200728577/836260807682686982/bimo.png')

        """ emb.set_image(url='https://media1.tenor.com/images/029763582b4705fa973c47e72ce8e9f5/tenor.gif?itemid=17302394') """

        emb.add_field(name='MOTIVO:', value=f'`{reason}`', inline=True)
        emb.add_field(name='TEMPO:', value='`10 horas`')

        
        await channel.send(embed = emb)
        """ await ctx.send(f'{member.mention} foi silenciado por {reason}') """
        await member.send(f'Você foi silenciado(a) no {guild.name} por {reason}')
        await member.add_roles(mutedRole, reason=reason)
        await asyncio.sleep(36000)
        await channel.send(f'{member.mention} você pode voltar a falar agora!')
        await member.remove_roles(mutedRole)




@client.command(description='Unmutes a specified user.')
@commands.has_permissions(manage_messages=True)
async def unmute(ctx, member: discord.Member):
    mutedRole = discord.utils.get(ctx.guild.roles, name='Muted')

    await member.remove_roles(mutedRole)
    await ctx.send(f'Unmuted {member.mention}')
    await member.send(f'You were unmuted in the server {ctx.guild.name}')






client.run(token)
