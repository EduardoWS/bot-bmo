import discord
from discord.ext import commands, tasks
import random
import time
from time import sleep
import datetime
from math import ceil
import json
import os
import asyncio
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



@client.listen('on_message')
async def on_message(message):
    channel = message.channel
    if channel.name == '💸┃loja':
        if message.author == client.user:
            await asyncio.sleep(20) 
            await message.delete()
        else:
            await asyncio.sleep(20) 
            await message.delete()

    elif channel.name == 'jujuba-8h':
        if message.author == client.user:
            await asyncio.sleep(60) 
            await message.delete()
        else:
            await asyncio.sleep(60) 
            await message.delete()

    elif channel.name == 'algodão-doce-12h':
        if message.author == client.user:
            await asyncio.sleep(60) 
            await message.delete()
        else:
            await asyncio.sleep(60) 
            await message.delete()

    elif channel.name == 'marshmallow-24h':
        if message.author == client.user:
            await asyncio.sleep(60) 
            await message.delete()
        else:
            await asyncio.sleep(60) 
            await message.delete()



# VV ====================== BANCO DE DADOS Postgres ====================== VV

db_host = "ec2-54-166-167-192.compute-1.amazonaws.com"
db_user = "mrjebrcdeikwqs"
db_name = "d47hnkn5vcli2n"
db_pass = "8dfd4737ba4fabd6c43e008b02f3d446b8e1f75a228d8c50c874b81ebb6b3307"


como_usar = """
    conn = db.connect(dbname=db_name, user=db_user, host=db_host, password=db_pass)

    cur = conn.cursor()

    cur.execute("INSERT INTO bank (cookies, iduser, nome) VALUES (100, 12345, 'teste')")
    conn.commit()

    cur.close()

    conn.close()
                 """



# VV ====================== ECONOMIA ====================== VV

@client.command()
async def criarconta(ctx):
    conn = db.connect(dbname=db_name, user=db_user, host=db_host, password=db_pass)
    cur = conn.cursor()
    
    
    
    cur.execute("SELECT iduser FROM bank WHERE iduser = %s", (ctx.author.id,))
    resultado = cur.fetchone()

    if resultado == None:
        cur.execute("INSERT INTO bank (cookies, iduser, nome) VALUES (5, %s, %s)", (ctx.author.id, ctx.author.name))
        conn.commit()
        await ctx.send('Conta criada com sucesso! Use o comando `!mybank` para ver mais informações')
        

    else:
        await ctx.send('Você já tem uma conta! Use o comando `!mybank` para ver mais informações')

    cur.close()
    conn.close()
    
    
@client.command()
async def bank(ctx, member: discord.Member):
    conn = db.connect(dbname=db_name, user=db_user, host=db_host, password=db_pass)
    cur = conn.cursor()
    
    
    cur.execute("SELECT iduser, cookies FROM bank WHERE iduser = %s", (member.id,))
    resultado = cur.fetchmany()

    
    if resultado == []:
        await ctx.send(f'Essa pessoa não tem uma conta criada!')

    else:
        
        for r in resultado:
            idu = r[0]
            saldo = r[1]

        emb = discord.Embed(
        title = 'BANK:',
        description = f'''
Nome: `{member.name}`

Saldo: `{saldo} Cookies`

ID da conta: ||`{idu}`||
        ''',
        colour = 16715320
        )

        emb.set_author(name='BMO',
        icon_url='https://cdn.discordapp.com/attachments/831946320200728577/836261314837741619/bmopng.png')

        emb.set_thumbnail(url=member.avatar_url)
        await ctx.send(embed = emb)
    
    cur.close()
    conn.close()


@client.command()
async def mybank(ctx):
    conn = db.connect(dbname=db_name, user=db_user, host=db_host, password=db_pass)
    cur = conn.cursor()


    cur.execute("SELECT iduser, cookies FROM bank WHERE iduser = %s", (ctx.author.id,))
    resultado = cur.fetchmany()



    if resultado == []:
        await ctx.send('Você não tem uma conta criada! Crie uma conta com `!criarconta`')

    else:
        for r in resultado:
            idu = r[0]
            saldo = r[1]

        emb = discord.Embed(
        title = 'BANK:',
        description = f'''
Nome: `{ctx.author.name}`

Saldo: `{saldo} Cookies`

ID da conta: ||`{idu}`||
        ''',
        colour = 16715320
        )

        emb.set_author(name='BMO',
        icon_url='https://cdn.discordapp.com/attachments/831946320200728577/836261314837741619/bmopng.png')

        emb.set_thumbnail(url=ctx.author.avatar_url)
        await ctx.send(embed = emb)

    cur.close()
    conn.close()
 




@client.command()
async def pay(ctx, quant, member: discord.Member):
    conn = db.connect(dbname=db_name, user=db_user, host=db_host, password=db_pass)
    cur = conn.cursor()


    cur.execute("SELECT iduser, cookies FROM bank WHERE iduser = %s", (member.id,))
    resultado = cur.fetchmany()

    
    if resultado == []:
        await ctx.send(f'Essa pessoa não tem uma conta criada!')

    else:
        for r in resultado:
            idu = r[0]
            saldo = r[1]
            

        cur.execute("SELECT iduser, cookies FROM bank WHERE iduser = %s", (ctx.author.id,))
        resultado2 = cur.fetchmany()
        
        if resultado2 == []:
            await ctx.send('Você não tem uma conta criada! Crie uma conta com `!criarconta`')

        else:
            for r in resultado2:
                idu2 = r[0]
                saldo2 = r[1]
            if saldo2 < int(quant):
                await ctx.send('Cookies insuficientes!')
            else:
                
                total = saldo + int(quant)
                total2 = saldo2 - int(quant)
                
                
                cur.execute("UPDATE bank SET cookies=%s WHERE iduser=%s", (total, member.id))
                conn.commit()

                cur.execute("UPDATE bank SET cookies=%s WHERE iduser=%s", (total2, ctx.author.id))
                conn.commit()

                
                await ctx.send(f'Transação realizada com sucesso! Novo saldo: `{total2} cookies`')
    cur.close()
    conn.close()


# VV ====================== FAZENDA ====================== VV

@client.command()
async def farm(ctx):
    channel = ctx.channel
    if channel.name == '🤖┃servos':

        conn = db.connect(dbname=db_name, user=db_user, host=db_host, password=db_pass)
        cur = conn.cursor()
    
        cur.execute("SELECT iduser FROM bank WHERE iduser = %s", (ctx.author.id,))
        bank = cur.fetchone()


        
        if bank == None:
            await ctx.send(f'{ctx.author.mention}, você precisa ter uma conta no banco para usar esse comando. Crie uma conta com `!criarconta`')

        else:
            cur.execute("SELECT iduser FROM fazenda WHERE iduser = %s", (ctx.author.id,))
            resultado = cur.fetchone()

            if resultado == None:
                cur.execute("INSERT INTO fazenda (iduser, lotes, loteid, s_j, s_ad, s_m, nome) VALUES (%s, 1, 'A', 50, 0, 0, %s)", (ctx.author.id, ctx.author.name))
                    
                guild = ctx.guild
                campRole = discord.utils.get(guild.roles, name='Camponês')
                await ctx.author.add_roles(campRole)
                emb = discord.Embed(
                title = '🌱 FAZENDA:',
                description = f'''
        **Agora você é um camponês!!**

        A categoria fazenda foi liberada e você ganhou:

        > 50 sementes de jujuba
        > Lote A


        **Use o comando `!farmt` para ver o tutorial**
                    ''',
                colour = 65280
                )

                """ emb.set_author(name='BMO',
                icon_url='https://cdn.discordapp.com/attachments/831946320200728577/836261314837741619/bmopng.png') """

                emb.set_thumbnail(url="https://cdn.discordapp.com/attachments/831946320200728577/840330089525805096/pngwing.com_1.png")
                await ctx.send(embed = emb)
                #await ctx.send('Agora você é um Camponês! \nA fazenda foi liberada e você ganhou: \n> `1 lote de terra (lote A)` \n> `50 sementes de jujuba`')
                conn.commit()

            else:
                await ctx.send('Você já é um Camponês!')
    else:
        await ctx.send('Canal errado, bobinho(a)!')

    
    cur.close()
    conn.close()




@client.command()
async def farmt(ctx):
    channel = ctx.channel
    if channel.name == '🤖┃servos':
        canalloja = client.get_channel(839548779417567263)
        canalj = client.get_channel(839552215068049448)
        canalad = client.get_channel(839552283322351686)
        canalm = client.get_channel(839552365690093609)
        emb = discord.Embed(
            title = 'TUTORIAL DA FAZENDA:',
            description = f'''
    **Aqui você aprenderá como ser um bom camponês**

Você começa com o `Lote A` que tem capacidade de até 1000 sementes para plantar.
Você também começa com 50 sementes de jujuba.

No canal {canalloja.mention} você poderá comprar sementes e lotes de terra.

Para ver quantas sementes e quais lotes você possui, digite `!myfarm`



**Plantação:**

> Existem 3 canais para plantar e colher: {canalj.mention}, {canalad.mention} e {canalm.mention}.
> 
> Você só poderá plantar jujubas no canal `jujuba-8h`
> Você só poderá plantar algodão doce no canal `algodão-doce-12h`
> Você só poderá plantar marshmallow no canal `marshmallow-24h`
> 
> Jujubas demoram 8 horas para você poder colher
> Algodões-doces demoram 12 horas para você poder colher
> Marshmallows demoram 24 horas para você poder colher
> 
> O comando para plantar é:
> `!plantar [sementes] [letra do lote]`
> 
> Ex: `!plantar 50 A`
> 
> Não é possível plantar menos que 50 sementes.
> Ao plantar em um lote ele ficará indisponível para o plantio.



**Colheita:**

> O comando para colher é:
> `!colher [letra do lote]`
> 
> Ex: `!colher A`
> 
> Lucro de 1000 jujubas:
> `25 a 50 cookies`
> 
> Lucro de 1000 algodões-doces:
> `67 a 125 cookies`
> 
> Lucro de 1000 marshmallows:
> `200 a 500 cookies`

> Ao plantar jujubas, você terá `3 dias` para colher. Depois disso, as jujubas apodrecerão e você perderá tudo.
> 
> Ao plantar algodões-doces, você terá `2 dias` para colher. Depois disso, os algodões-doces apodrecerão e você perderá tudo.
> 
> Ao plantar marshmallows, você terá `1 dia` para colher. Depois disso, os marshmallows apodrecerão e você perderá tudo.


            ''',
            colour= 65280
        )
        await ctx.send(embed = emb)

    else:
        await ctx.send('Canal errado, bobinho(a)!')







@client.command()
async def myfarm(ctx):
    channel = ctx.channel
    if channel.name == '🌱┃fazenda' or channel.name == 'jujuba-8h' or channel.name == 'algodão-doce-12h' or channel.name == 'marshmallow-24h':
        conn = db.connect(dbname=db_name, user=db_user, host=db_host, password=db_pass)
        cur = conn.cursor()

        cur.execute("SELECT s_j, s_ad, s_m FROM fazenda WHERE iduser = %s AND loteid = 'A' ", (ctx.author.id, ))
        sementes = cur.fetchmany()
        
        cur.execute("SELECT loteid FROM fazenda WHERE iduser=%s AND loteid='B'", (ctx.author.id, ))
        loteB = cur.fetchmany()
        
        cur.execute("SELECT loteid FROM fazenda WHERE iduser=%s AND loteid='C'", (ctx.author.id, ))
        loteC = cur.fetchmany()
        
        #LOTE A
        if loteB == [] and loteC == []:
            
            cur.execute("SELECT lotes FROM fazenda WHERE iduser=%s AND loteid='A'", (ctx.author.id, ))
            planted = cur.fetchone()
            
            if planted[0] == 1:

                emb = discord.Embed(
                title = 'PROPRIEDADE DE',
                description = f'''
        {ctx.author.mention}

        **SEMENTES:**
        > Jujuba: `{sementes[0][0]} semente(s)`
        > Algodão-doce: `{sementes[0][1]} semente(s)`
        > Marshmallow: `{sementes[0][2]} semente(s)`

        **LOTES:**
        > Lote A `adquirido`

        **PLANTAÇÕES:**
        > Lote A: `nada foi plantado aqui`

                ''',
                colour = 65280
                )

                
                emb.set_thumbnail(url="https://cdn.discordapp.com/attachments/831946320200728577/840368724748795934/fazenda1.png")
                await ctx.send(embed = emb)

            else:
                cur.execute("SELECT dataa, horaa FROM fazenda WHERE iduser = %s AND loteid='A'", (ctx.author.id, ))
                resultado_datas = cur.fetchmany()
                dataa = resultado_datas[0][0]
                horaa = resultado_datas[0][1]
                
                dia = dataa[:2]
                mes = dataa[3:5]
                ano = dataa[6:]
                
                horas = horaa[:2]
                minutos = horaa[3:]

                insec = datetime.datetime(int(ano), int(mes), int(dia), int(horas), int(minutos))
                cur.execute("SELECT plantedid FROM fazenda WHERE iduser=%s AND loteid='A'", (ctx.author.id, ))
                plantedidA = cur.fetchone()
                
                if plantedidA[0] == 'j':
                    colheita = insec + datetime.timedelta(hours=8)
                elif plantedidA[0] == 'ad':
                    colheita = insec + datetime.timedelta(hours=12)
                elif plantedidA[0] == 'm':
                    colheita = insec + datetime.timedelta(hours=24)
                
                

                result = colheita - datetime.datetime.now()
                formatar = ':'.join(str(result).split(':')[:2])
                if result < datetime.timedelta(hours=10):
                    formatar = f'0{formatar}'


                emb = discord.Embed(
                title = 'PROPRIEDADE DE',
                description = f'''
        {ctx.author.mention}

        **SEMENTES:**
        > Jujuba: `{sementes[0][0]} semente(s)`
        > Algodão-doce: `{sementes[0][1]} semente(s)`
        > Marshmallow: `{sementes[0][2]} semente(s)`

        **LOTES:**
        > Lote A `adquirido`

        **PLANTAÇÕES:**
        > Lote A: `em uso`
        > Tempo que falta: `{formatar}`

                ''',
                colour = 65280
                )

                
                emb.set_thumbnail(url="https://cdn.discordapp.com/attachments/831946320200728577/840368724748795934/fazenda1.png")
                await ctx.send(embed = emb)






        #DOIS LOTES (LOTE A E LOTE B)
        elif loteB[0][0] == 'B' and loteC == []:
            cur.execute("SELECT lotes FROM fazenda WHERE iduser=%s AND loteid='A'", (ctx.author.id, ))
            plantedA = cur.fetchone()
            
            cur.execute("SELECT lotes FROM fazenda WHERE iduser=%s AND loteid='B'", (ctx.author.id, ))
            plantedB = cur.fetchone()

            if plantedA[0] == 1 and plantedB[0] == 1:

                emb = discord.Embed(
                title = 'PROPRIEDADE DE',
                description = f'''
        {ctx.author.mention}

        **SEMENTES:**
        > Jujuba: `{sementes[0][0]} semente(s)`
        > Algodão-doce: `{sementes[0][1]} semente(s)`
        > Marshmallow: `{sementes[0][2]} semente(s)`

        **LOTES:**
        > Lote A `adquirido`
        > Lote B `adquirido`

        **PLANTAÇÕES:**
        > Lote A: `nada foi plantado aqui`
        > Lote B: `nada foi plantado aqui`
                ''',
                colour = 65280
                )

                
                emb.set_thumbnail(url="https://cdn.discordapp.com/attachments/831946320200728577/840368724748795934/fazenda1.png")
                await ctx.send(embed = emb)

            elif plantedA[0] == 0 and plantedB[0] == 1:
                cur.execute("SELECT dataa, horaa FROM fazenda WHERE iduser = %s AND loteid='A'", (ctx.author.id, ))
                resultado_datas = cur.fetchmany()
                dataa = resultado_datas[0][0]
                horaa = resultado_datas[0][1]
                
                dia = dataa[:2]
                mes = dataa[3:5]
                ano = dataa[6:]
                
                horas = horaa[:2]
                minutos = horaa[3:]

                insec = datetime.datetime(int(ano), int(mes), int(dia), int(horas), int(minutos))
                cur.execute("SELECT plantedid FROM fazenda WHERE iduser=%s AND loteid='A'", (ctx.author.id, ))
                plantedidA = cur.fetchone()
                
                if plantedidA[0] == 'j':
                    colheita = insec + datetime.timedelta(hours=8)
                elif plantedidA[0] == 'ad':
                    colheita = insec + datetime.timedelta(hours=12)
                elif plantedidA[0] == 'm':
                    colheita = insec + datetime.timedelta(hours=24)
                

                result = colheita - datetime.datetime.now()
                formatar = ':'.join(str(result).split(':')[:2])
                if result < datetime.timedelta(hours=10):
                    formatar = f'0{formatar}'


                emb = discord.Embed(
                title = 'PROPRIEDADE DE',
                description = f'''
        {ctx.author.mention}

        **SEMENTES:**
        > Jujuba: `{sementes[0][0]} semente(s)`
        > Algodão-doce: `{sementes[0][1]} semente(s)`
        > Marshmallow: `{sementes[0][2]} semente(s)`

        **LOTES:**
        > Lote A `adquirido`
        > Lote B `adquirido`

        **PLANTAÇÕES:**
        > Lote A: `em uso`
        > Tempo que falta: `{formatar}`
        > Lote B: `nada foi plantado aqui`

                ''',
                colour = 65280
                )

                
                emb.set_thumbnail(url="https://cdn.discordapp.com/attachments/831946320200728577/840368724748795934/fazenda1.png")
                await ctx.send(embed = emb)

            elif plantedA[0] == 1 and plantedB[0] == 0:
                cur.execute("SELECT dataa, horaa FROM fazenda WHERE iduser = %s AND loteid='B'", (ctx.author.id, ))
                resultado_datas = cur.fetchmany()
                dataa = resultado_datas[0][0]
                horaa = resultado_datas[0][1]
                
                dia = dataa[:2]
                mes = dataa[3:5]
                ano = dataa[6:]
                
                horas = horaa[:2]
                minutos = horaa[3:]

                insec = datetime.datetime(int(ano), int(mes), int(dia), int(horas), int(minutos))
                cur.execute("SELECT plantedid FROM fazenda WHERE iduser=%s AND loteid='B'", (ctx.author.id, ))
                plantedidB = cur.fetchone()
                
                if plantedidA[0] == 'j':
                    colheita = insec + datetime.timedelta(hours=8)
                elif plantedidA[0] == 'ad':
                    colheita = insec + datetime.timedelta(hours=12)
                elif plantedidA[0] == 'm':
                    colheita = insec + datetime.timedelta(hours=24)
                
                
              

                result = colheita - datetime.datetime.now()
                formatar = ':'.join(str(result).split(':')[:2])
                if result < datetime.timedelta(hours=10):
                    formatar = f'0{formatar}'


                emb = discord.Embed(
                title = 'PROPRIEDADE DE',
                description = f'''
        {ctx.author.mention}

        **SEMENTES:**
        > Jujuba: `{sementes[0][0]} semente(s)`
        > Algodão-doce: `{sementes[0][1]} semente(s)`
        > Marshmallow: `{sementes[0][2]} semente(s)`

        **LOTES:**
        > Lote A `adquirido`
        > Lote B `adquirido`

        **PLANTAÇÕES:**
        > Lote A: `nada foi plantado aqui`
        > Lote B: `em uso`
        > Tempo que falta: `{formatar}`


                ''',
                colour = 65280
                )

                
                emb.set_thumbnail(url="https://cdn.discordapp.com/attachments/831946320200728577/840368724748795934/fazenda1.png")
                await ctx.send(embed = emb)

            elif plantedA[0] == 0 and plantedB[0] == 0:
                cur.execute("SELECT dataa, horaa FROM fazenda WHERE iduser = %s AND loteid='A'", (ctx.author.id, ))
                resultado_datasA = cur.fetchmany()
                cur.execute("SELECT dataa, horaa FROM fazenda WHERE iduser = %s AND loteid='B'", (ctx.author.id, ))
                resultado_datasB = cur.fetchmany()
                dataa = resultado_datasA[0][0]
                horaa = resultado_datasA[0][1]
                dataB = resultado_datasB[0][0]
                horaB = resultado_datasB[0][1]
                
                dia = dataa[:2]
                mes = dataa[3:5]
                ano = dataa[6:]
                diaB = dataB[:2]
                mesB = dataB[3:5]
                anoB = dataB[6:]
                
                horas = horaa[:2]
                minutos = horaa[3:]
                horasB = horaB[:2]
                minutosB = horaB[3:]

                insec = datetime.datetime(int(ano), int(mes), int(dia), int(horas), int(minutos))
                insecB = datetime.datetime(int(anoB), int(mesB), int(diaB), int(horasB), int(minutosB))
                cur.execute("SELECT plantedid FROM fazenda WHERE iduser=%s AND loteid='A'", (ctx.author.id, ))
                plantedidA = cur.fetchone()
                
                if plantedidA[0] == 'j':
                    colheita = insec + datetime.timedelta(hours=8)
                elif plantedidA[0] == 'ad':
                    colheita = insec + datetime.timedelta(hours=12)
                elif plantedidA[0] == 'm':
                    colheita = insec + datetime.timedelta(hours=24)

                cur.execute("SELECT plantedid FROM fazenda WHERE iduser=%s AND loteid='B'", (ctx.author.id, ))
                plantedidB = cur.fetchone()

                if plantedidB[0] == 'j':
                    colheitaB = insecB + datetime.timedelta(hours=8)
                elif plantedidB[0] == 'ad':
                    colheitaB = insecB + datetime.timedelta(hours=12)
                elif plantedidB[0] == 'm':
                    colheitaB = insecB + datetime.timedelta(hours=24)

                resultA = colheita - datetime.datetime.now()
                resultB = colheitaB - datetime.datetime.now()
                formatarA = ':'.join(str(resultA).split(':')[:2])
                formatarB = ':'.join(str(resultB).split(':')[:2])

                if resultA < datetime.timedelta(hours=10):
                    formatarA = f'0{formatar}'

                if resultB < datetime.timedelta(hours=10):
                    formatarB = f'0{formatar}'

                emb = discord.Embed(
                title = 'PROPRIEDADE DE',
                description = f'''
        {ctx.author.mention}

        **SEMENTES:**
        > Jujuba: `{sementes[0][0]} semente(s)`
        > Algodão-doce: `{sementes[0][1]} semente(s)`
        > Marshmallow: `{sementes[0][2]} semente(s)`

        **LOTES:**
        > Lote A `adquirido`
        > Lote B `adquirido`

        **PLANTAÇÕES:**
        > Lote A: `em uso`
        > Tempo que falta: `{formatarA}`
        > Lote B: `em uso`
        > Tempo que falta: `{formatarB}`


                ''',
                colour = 65280
                )

                
                emb.set_thumbnail(url="https://cdn.discordapp.com/attachments/831946320200728577/840368724748795934/fazenda1.png")
                await ctx.send(embed = emb)


        #PARTE 3 (LOTE A, LOTE B E LOTE C)
        elif loteC[0][0] == 'C':
            cur.execute("SELECT lotes FROM fazenda WHERE iduser=%s AND loteid='A'", (ctx.author.id, ))
            plantedA = cur.fetchone()
            
            cur.execute("SELECT lotes FROM fazenda WHERE iduser=%s AND loteid='B'", (ctx.author.id, ))
            plantedB = cur.fetchone()

            cur.execute("SELECT lotes FROM fazenda WHERE iduser=%s AND loteid='C'", (ctx.author.id, ))
            plantedC = cur.fetchone()

            if plantedA[0] == 1 and plantedB[0] == 1 and plantedC[0] == 1:

                emb = discord.Embed(
                title = 'PROPRIEDADE DE',
                description = f'''
        {ctx.author.mention}

        **SEMENTES:**
        > Jujuba: `{sementes[0][0]} semente(s)`
        > Algodão-doce: `{sementes[0][1]} semente(s)`
        > Marshmallow: `{sementes[0][2]} semente(s)`

        **LOTES:**
        > Lote A `adquirido`
        > Lote B `adquirido`
        > Lote C `adquirido`

        **PLANTAÇÕES:**
        > Lote A: `nada foi plantado aqui`
        > Lote B: `nada foi plantado aqui`
        > Lote C: `nada foi plantado aqui`
                ''',
                colour = 65280
                )

                
                emb.set_thumbnail(url="https://cdn.discordapp.com/attachments/831946320200728577/840368724748795934/fazenda1.png")
                await ctx.send(embed = emb)

            elif plantedA[0] == 0 and plantedB[0] == 1 and plantedC[0] == 1:
                cur.execute("SELECT dataa, horaa FROM fazenda WHERE iduser = %s AND loteid='A'", (ctx.author.id, ))
                resultado_datas = cur.fetchmany()
                dataa = resultado_datas[0][0]
                horaa = resultado_datas[0][1]
                
                dia = dataa[:2]
                mes = dataa[3:5]
                ano = dataa[6:]
                
                horas = horaa[:2]
                minutos = horaa[3:]

                insec = datetime.datetime(int(ano), int(mes), int(dia), int(horas), int(minutos))
                cur.execute("SELECT plantedid FROM fazenda WHERE iduser=%s AND loteid='A'", (ctx.author.id, ))
                plantedidA = cur.fetchone()
                
                if plantedidA[0] == 'j':
                    colheita = insec + datetime.timedelta(hours=8)
                elif plantedidA[0] == 'ad':
                    colheita = insec + datetime.timedelta(hours=12)
                elif plantedidA[0] == 'm':
                    colheita = insec + datetime.timedelta(hours=24)
                

                result = colheita - datetime.datetime.now()
                formatar = ':'.join(str(result).split(':')[:2])
                if result < datetime.timedelta(hours=10):
                    formatar = f'0{formatar}'


                emb = discord.Embed(
                title = 'PROPRIEDADE DE',
                description = f'''
        {ctx.author.mention}

        **SEMENTES:**
        > Jujuba: `{sementes[0][0]} semente(s)`
        > Algodão-doce: `{sementes[0][1]} semente(s)`
        > Marshmallow: `{sementes[0][2]} semente(s)`

        **LOTES:**
        > Lote A `adquirido`
        > Lote B `adquirido`
        > Lote C `adquirido`

        **PLANTAÇÕES:**
        > Lote A: `em uso`
        > Tempo que falta: `{formatar}`
        > Lote B: `nada foi plantado aqui`
        > Lote C: `nada foi plantado aqui`

                ''',
                colour = 65280
                )

                
                emb.set_thumbnail(url="https://cdn.discordapp.com/attachments/831946320200728577/840368724748795934/fazenda1.png")
                await ctx.send(embed = emb)

            elif plantedA[0] == 1 and plantedB[0] == 0 and plantedC[0] == 1:
                cur.execute("SELECT dataa, horaa FROM fazenda WHERE iduser = %s AND loteid='B'", (ctx.author.id, ))
                resultado_datas = cur.fetchmany()
                dataa = resultado_datas[0][0]
                horaa = resultado_datas[0][1]
                
                dia = dataa[:2]
                mes = dataa[3:5]
                ano = dataa[6:]
                
                horas = horaa[:2]
                minutos = horaa[3:]

                insec = datetime.datetime(int(ano), int(mes), int(dia), int(horas), int(minutos))
                cur.execute("SELECT plantedid FROM fazenda WHERE iduser=%s AND loteid='B'", (ctx.author.id, ))
                plantedidB = cur.fetchone()
                
                if plantedidA[0] == 'j':
                    colheita = insec + datetime.timedelta(hours=8)
                elif plantedidA[0] == 'ad':
                    colheita = insec + datetime.timedelta(hours=12)
                elif plantedidA[0] == 'm':
                    colheita = insec + datetime.timedelta(hours=24)
                
                
              

                result = colheita - datetime.datetime.now()
                formatar = ':'.join(str(result).split(':')[:2])
                if result < datetime.timedelta(hours=10):
                    formatar = f'0{formatar}'


                emb = discord.Embed(
                title = 'PROPRIEDADE DE',
                description = f'''
        {ctx.author.mention}

        **SEMENTES:**
        > Jujuba: `{sementes[0][0]} semente(s)`
        > Algodão-doce: `{sementes[0][1]} semente(s)`
        > Marshmallow: `{sementes[0][2]} semente(s)`

        **LOTES:**
        > Lote A `adquirido`
        > Lote B `adquirido`
        > Lote C `adquirido`

        **PLANTAÇÕES:**
        > Lote A: `nada foi plantado aqui`
        > Lote B: `em uso`
        > Tempo que falta: `{formatar}`
        > Lote C: `nada foi plantado aqui`


                ''',
                colour = 65280
                )

                
                emb.set_thumbnail(url="https://cdn.discordapp.com/attachments/831946320200728577/840368724748795934/fazenda1.png")
                await ctx.send(embed = emb)

            elif plantedA[0] == 0 and plantedB[0] == 0 and plantedC[0] == 1:
                cur.execute("SELECT dataa, horaa FROM fazenda WHERE iduser = %s AND loteid='A'", (ctx.author.id, ))
                resultado_datasA = cur.fetchmany()
                cur.execute("SELECT dataa, horaa FROM fazenda WHERE iduser = %s AND loteid='B'", (ctx.author.id, ))
                resultado_datasB = cur.fetchmany()
                dataa = resultado_datasA[0][0]
                horaa = resultado_datasA[0][1]
                dataB = resultado_datasB[0][0]
                horaB = resultado_datasB[0][1]
                
                dia = dataa[:2]
                mes = dataa[3:5]
                ano = dataa[6:]
                diaB = dataB[:2]
                mesB = dataB[3:5]
                anoB = dataB[6:]
                
                horas = horaa[:2]
                minutos = horaa[3:]
                horasB = horaB[:2]
                minutosB = horaB[3:]

                insec = datetime.datetime(int(ano), int(mes), int(dia), int(horas), int(minutos))
                insecB = datetime.datetime(int(anoB), int(mesB), int(diaB), int(horasB), int(minutosB))
                cur.execute("SELECT plantedid FROM fazenda WHERE iduser=%s AND loteid='A'", (ctx.author.id, ))
                plantedidA = cur.fetchone()
                
                if plantedidA[0] == 'j':
                    colheita = insec + datetime.timedelta(hours=8)
                elif plantedidA[0] == 'ad':
                    colheita = insec + datetime.timedelta(hours=12)
                elif plantedidA[0] == 'm':
                    colheita = insec + datetime.timedelta(hours=24)

                cur.execute("SELECT plantedid FROM fazenda WHERE iduser=%s AND loteid='B'", (ctx.author.id, ))
                plantedidB = cur.fetchone()

                if plantedidB[0] == 'j':
                    colheitaB = insecB + datetime.timedelta(hours=8)
                elif plantedidB[0] == 'ad':
                    colheitaB = insecB + datetime.timedelta(hours=12)
                elif plantedidB[0] == 'm':
                    colheitaB = insecB + datetime.timedelta(hours=24)

                resultA = colheita - datetime.datetime.now()
                resultB = colheitaB - datetime.datetime.now()
                formatarA = ':'.join(str(resultA).split(':')[:2])
                formatarB = ':'.join(str(resultB).split(':')[:2])

                if resultA < datetime.timedelta(hours=10):
                    formatarA = f'0{formatar}'

                if resultB < datetime.timedelta(hours=10):
                    formatarB = f'0{formatar}'

                emb = discord.Embed(
                title = 'PROPRIEDADE DE',
                description = f'''
        {ctx.author.mention}

        **SEMENTES:**
        > Jujuba: `{sementes[0][0]} semente(s)`
        > Algodão-doce: `{sementes[0][1]} semente(s)`
        > Marshmallow: `{sementes[0][2]} semente(s)`

        **LOTES:**
        > Lote A `adquirido`
        > Lote B `adquirido`
        > Lote C `adquirido`

        **PLANTAÇÕES:**
        > Lote A: `em uso`
        > Tempo que falta: `{formatarA}`
        > Lote B: `em uso`
        > Tempo que falta: `{formatarB}`
        > Lote C: `nada foi plantado aqui`


                ''',
                colour = 65280
                )

                
                emb.set_thumbnail(url="https://cdn.discordapp.com/attachments/831946320200728577/840368724748795934/fazenda1.png")
                await ctx.send(embed = emb)




        elif plantedA[0] == 1 and plantedB[0] == 1 and plantedC[0] == 0:
                cur.execute("SELECT dataa, horaa FROM fazenda WHERE iduser = %s AND loteid='C'", (ctx.author.id, ))
                resultado_datas = cur.fetchmany()
                dataa = resultado_datas[0][0]
                horaa = resultado_datas[0][1]
                
                dia = dataa[:2]
                mes = dataa[3:5]
                ano = dataa[6:]
                
                horas = horaa[:2]
                minutos = horaa[3:]

                insec = datetime.datetime(int(ano), int(mes), int(dia), int(horas), int(minutos))
                cur.execute("SELECT plantedid FROM fazenda WHERE iduser=%s AND loteid='C'", (ctx.author.id, ))
                plantedidC = cur.fetchone()
                
                if plantedidC[0] == 'j':
                    colheita = insec + datetime.timedelta(hours=8)
                elif plantedidC[0] == 'ad':
                    colheita = insec + datetime.timedelta(hours=12)
                elif plantedidC[0] == 'm':
                    colheita = insec + datetime.timedelta(hours=24)
                

                result = colheita - datetime.datetime.now()
                formatar = ':'.join(str(result).split(':')[:2])
                if result < datetime.timedelta(hours=10):
                    formatar = f'0{formatar}'


                emb = discord.Embed(
                title = 'PROPRIEDADE DE',
                description = f'''
        {ctx.author.mention}

        **SEMENTES:**
        > Jujuba: `{sementes[0][0]} semente(s)`
        > Algodão-doce: `{sementes[0][1]} semente(s)`
        > Marshmallow: `{sementes[0][2]} semente(s)`

        **LOTES:**
        > Lote A `adquirido`
        > Lote B `adquirido`
        > Lote C `adquirido`

        **PLANTAÇÕES:**
        > Lote A: `nada foi plantado aqui`
        > Lote B: `nada foi plantado aqui`
        > Lote C: `em uso`
        > Tempo que falta: `{formatar}`

                ''',
                colour = 65280
                )

                
                emb.set_thumbnail(url="https://cdn.discordapp.com/attachments/831946320200728577/840368724748795934/fazenda1.png")
                await ctx.send(embed = emb)

        
        elif plantedA[0] == 0 and plantedB[0] == 1 and plantedC[0] == 0:
                cur.execute("SELECT dataa, horaa FROM fazenda WHERE iduser = %s AND loteid='A'", (ctx.author.id, ))
                resultado_datasA = cur.fetchmany()
                cur.execute("SELECT dataa, horaa FROM fazenda WHERE iduser = %s AND loteid='C'", (ctx.author.id, ))
                resultado_datasC = cur.fetchmany()
                
                dataa = resultado_datasA[0][0]
                horaa = resultado_datasA[0][1]
                dataC = resultado_datasC[0][0]
                horaC = resultado_datasC[0][1]
                
                dia = dataa[:2]
                mes = dataa[3:5]
                ano = dataa[6:]
                diaC = dataC[:2]
                mesC = dataC[3:5]
                anoC = dataC[6:]
                
                horas = horaa[:2]
                minutos = horaa[3:]
                horasC = horaC[:2]
                minutosC = horaC[3:]

                insec = datetime.datetime(int(ano), int(mes), int(dia), int(horas), int(minutos))
                insecC = datetime.datetime(int(anoC), int(mesC), int(diaC), int(horasC), int(minutosC))
                cur.execute("SELECT plantedid FROM fazenda WHERE iduser=%s AND loteid='A'", (ctx.author.id, ))
                plantedidA = cur.fetchone()
                
                if plantedidA[0] == 'j':
                    colheita = insec + datetime.timedelta(hours=8)
                elif plantedidA[0] == 'ad':
                    colheita = insec + datetime.timedelta(hours=12)
                elif plantedidA[0] == 'm':
                    colheita = insec + datetime.timedelta(hours=24)

                cur.execute("SELECT plantedid FROM fazenda WHERE iduser=%s AND loteid='C'", (ctx.author.id, ))
                plantedidC = cur.fetchone()

                if plantedidC[0] == 'j':
                    colheitaC = insecC + datetime.timedelta(hours=8)
                elif plantedidC[0] == 'ad':
                    colheitaC = insecC + datetime.timedelta(hours=12)
                elif plantedidC[0] == 'm':
                    colheitaC = insecC + datetime.timedelta(hours=24)

                resultA = colheita - datetime.datetime.now()
                resultC = colheitaC - datetime.datetime.now()
                formatarA = ':'.join(str(resultA).split(':')[:2])
                formatarC = ':'.join(str(resultC).split(':')[:2])

                if resultA < datetime.timedelta(hours=10):
                    formatarA = f'0{formatar}'

                if resultC < datetime.timedelta(hours=10):
                    formatarC = f'0{formatar}'

                emb = discord.Embed(
                title = 'PROPRIEDADE DE',
                description = f'''
        {ctx.author.mention}

        **SEMENTES:**
        > Jujuba: `{sementes[0][0]} semente(s)`
        > Algodão-doce: `{sementes[0][1]} semente(s)`
        > Marshmallow: `{sementes[0][2]} semente(s)`

        **LOTES:**
        > Lote A `adquirido`
        > Lote B `adquirido`
        > Lote C `adquirido`

        **PLANTAÇÕES:**
        > Lote A: `em uso`
        > Tempo que falta: `{formatarA}`
        > Lote B: `nada foi plantado aqui`
        > Lote C: `em uso`
        > Tempo que falta: `{formatarC}`


                ''',
                colour = 65280
                )

                
                emb.set_thumbnail(url="https://cdn.discordapp.com/attachments/831946320200728577/840368724748795934/fazenda1.png")
                await ctx.send(embed = emb)

        elif plantedA[0] == 0 and plantedB[0] == 1 and plantedC[0] == 0:
                cur.execute("SELECT dataa, horaa FROM fazenda WHERE iduser = %s AND loteid='B'", (ctx.author.id, ))
                resultado_datasB = cur.fetchmany()
                cur.execute("SELECT dataa, horaa FROM fazenda WHERE iduser = %s AND loteid='C'", (ctx.author.id, ))
                resultado_datasC = cur.fetchmany()
                
                dataa = resultado_datasB[0][0]
                horaa = resultado_datasB[0][1]
                dataC = resultado_datasC[0][0]
                horaC = resultado_datasC[0][1]
                
                dia = dataa[:2]
                mes = dataa[3:5]
                ano = dataa[6:]
                diaC = dataC[:2]
                mesC = dataC[3:5]
                anoC = dataC[6:]
                
                horas = horaa[:2]
                minutos = horaa[3:]
                horasC = horaC[:2]
                minutosC = horaC[3:]

                insec = datetime.datetime(int(ano), int(mes), int(dia), int(horas), int(minutos))
                insecC = datetime.datetime(int(anoC), int(mesC), int(diaC), int(horasC), int(minutosC))
                cur.execute("SELECT plantedid FROM fazenda WHERE iduser=%s AND loteid='B'", (ctx.author.id, ))
                plantedidB = cur.fetchone()
                
                if plantedidB[0] == 'j':
                    colheita = insec + datetime.timedelta(hours=8)
                elif plantedidB[0] == 'ad':
                    colheita = insec + datetime.timedelta(hours=12)
                elif plantedidB[0] == 'm':
                    colheita = insec + datetime.timedelta(hours=24)

                cur.execute("SELECT plantedid FROM fazenda WHERE iduser=%s AND loteid='C'", (ctx.author.id, ))
                plantedidC = cur.fetchone()

                if plantedidC[0] == 'j':
                    colheitaC = insecC + datetime.timedelta(hours=8)
                elif plantedidC[0] == 'ad':
                    colheitaC = insecC + datetime.timedelta(hours=12)
                elif plantedidC[0] == 'm':
                    colheitaC = insecC + datetime.timedelta(hours=24)

                resultB = colheita - datetime.datetime.now()
                resultC = colheitaC - datetime.datetime.now()
                formatarB = ':'.join(str(resultB).split(':')[:2])
                formatarC = ':'.join(str(resultC).split(':')[:2])

                if resultA < datetime.timedelta(hours=10):
                    formatarB = f'0{formatar}'

                if resultC < datetime.timedelta(hours=10):
                    formatarC = f'0{formatar}'

                emb = discord.Embed(
                title = 'PROPRIEDADE DE',
                description = f'''
        {ctx.author.mention}

        **SEMENTES:**
        > Jujuba: `{sementes[0][0]} semente(s)`
        > Algodão-doce: `{sementes[0][1]} semente(s)`
        > Marshmallow: `{sementes[0][2]} semente(s)`

        **LOTES:**
        > Lote A `adquirido`
        > Lote B `adquirido`
        > Lote C `adquirido`

        **PLANTAÇÕES:**
        > Lote A: `nada foi plantado aqui`
        > Lote B: `em uso`
        > Tempo que falta: `{formatarB}`
        > Lote C: `em uso`
        > Tempo que falta: `{formatarC}`


                ''',
                colour = 65280
                )

                
                emb.set_thumbnail(url="https://cdn.discordapp.com/attachments/831946320200728577/840368724748795934/fazenda1.png")
                await ctx.send(embed = emb)
        
        
        elif plantedA[0] == 0 and plantedB[0] == 0 and plantedC[0] == 0:
                cur.execute("SELECT dataa, horaa FROM fazenda WHERE iduser = %s AND loteid='A'", (ctx.author.id, ))
                resultado_datasA = cur.fetchmany()
                cur.execute("SELECT dataa, horaa FROM fazenda WHERE iduser = %s AND loteid='B'", (ctx.author.id, ))
                resultado_datasB = cur.fetchmany()
                cur.execute("SELECT dataa, horaa FROM fazenda WHERE iduser = %s AND loteid='C'", (ctx.author.id, ))
                resultado_datasC = cur.fetchmany()
                
                dataa = resultado_datasA[0][0]
                horaa = resultado_datasA[0][1]
                dataB = resultado_datasB[0][0]
                horaB = resultado_datasB[0][1]
                dataC = resultado_datasC[0][0]
                horaC = resultado_datasC[0][1]
                
                dia = dataa[:2]
                mes = dataa[3:5]
                ano = dataa[6:]
                diaB = dataB[:2]
                mesB = dataB[3:5]
                anoB = dataB[6:]
                diaC = dataC[:2]
                mesC = dataC[3:5]
                anoC = dataC[6:]
                
                horas = horaa[:2]
                minutos = horaa[3:]
                horasB = horaB[:2]
                minutosB = horaB[3:]
                horasC = horaC[:2]
                minutosC = horaC[3:]

                insec = datetime.datetime(int(ano), int(mes), int(dia), int(horas), int(minutos))
                insecB = datetime.datetime(int(anoB), int(mesB), int(diaB), int(horasB), int(minutosB))
                insecC = datetime.datetime(int(anoC), int(mesC), int(diaC), int(horasC), int(minutosC))

                cur.execute("SELECT plantedid FROM fazenda WHERE iduser=%s AND loteid='A'", (ctx.author.id, ))
                plantedidA = cur.fetchone()
                
                if plantedidA[0] == 'j':
                    colheita = insec + datetime.timedelta(hours=8)
                elif plantedidA[0] == 'ad':
                    colheita = insec + datetime.timedelta(hours=12)
                elif plantedidA[0] == 'm':
                    colheita = insec + datetime.timedelta(hours=24)

                cur.execute("SELECT plantedid FROM fazenda WHERE iduser=%s AND loteid='B'", (ctx.author.id, ))
                plantedidB = cur.fetchone()

                if plantedidB[0] == 'j':
                    colheitaB = insecB + datetime.timedelta(hours=8)
                elif plantedidC[0] == 'ad':
                    colheitaB = insecB + datetime.timedelta(hours=12)
                elif plantedidB[0] == 'm':
                    colheitaB = insecB + datetime.timedelta(hours=24)

                cur.execute("SELECT plantedid FROM fazenda WHERE iduser=%s AND loteid='C'", (ctx.author.id, ))
                plantedidC = cur.fetchone()

                if plantedidC[0] == 'j':
                    colheitaC = insecC + datetime.timedelta(hours=8)
                elif plantedidC[0] == 'ad':
                    colheitaC = insecC + datetime.timedelta(hours=12)
                elif plantedidC[0] == 'm':
                    colheitaC = insecC + datetime.timedelta(hours=24)

                resultA = colheita - datetime.datetime.now()
                resultB = colheitaB - datetime.datetime.now()
                resultC = colheitaC - datetime.datetime.now()
                formatarA = ':'.join(str(resultA).split(':')[:2])
                formatarB = ':'.join(str(resultB).split(':')[:2])
                formatarC = ':'.join(str(resultC).split(':')[:2])

                if resultA < datetime.timedelta(hours=10):
                    formatarA = f'0{formatar}'
                
                if resultB < datetime.timedelta(hours=10):
                    formatarB = f'0{formatar}'

                if resultC < datetime.timedelta(hours=10):
                    formatarC = f'0{formatar}'

                emb = discord.Embed(
                title = 'PROPRIEDADE DE',
                description = f'''
        {ctx.author.mention}

        **SEMENTES:**
        > Jujuba: `{sementes[0][0]} semente(s)`
        > Algodão-doce: `{sementes[0][1]} semente(s)`
        > Marshmallow: `{sementes[0][2]} semente(s)`

        **LOTES:**
        > Lote A `adquirido`
        > Lote B `adquirido`
        > Lote C `adquirido`

        **PLANTAÇÕES:**
        > Lote A: `em uso`
        > Tempo que falta: `{formatarA}`
        > Lote B: `em uso`
        > Tempo que falta: `{formatarB}`
        > Lote C: `em uso`
        > Tempo que falta: `{formatarC}`


                ''',
                colour = 65280
                )

                
                emb.set_thumbnail(url="https://cdn.discordapp.com/attachments/831946320200728577/840368724748795934/fazenda1.png")
                await ctx.send(embed = emb)
            




    else:
        await ctx.send('Canal errado, bobinho(a)!')

@client.command()
async def buyb(ctx):
    conn = db.connect(dbname=db_name, user=db_user, host=db_host, password=db_pass)
    cur = conn.cursor()

    cur.execute("INSERT INTO fazenda (iduser, lotes, loteid, nome) VALUES (%s, 1, 'B', %s)", (ctx.author.id, ctx.author.name))
    conn.commit()
    cur.close()
    conn.close()
    await ctx.send('Compra realizada com sucesso!')


        






@client.command()
async def plantar(ctx, quant, lote):
    channel = ctx.channel
    if channel.name == 'jujuba-8h':
        conn = db.connect(dbname=db_name, user=db_user, host=db_host, password=db_pass)
        cur = conn.cursor()

        cur.execute("SELECT lotes FROM fazenda WHERE iduser = %s AND loteid=%s", (ctx.author.id, lote.upper()))
        resultado = cur.fetchone()
        
        if resultado[0] == 0:
            await ctx.send(f'{ctx.author.mention}, você não tem lotes de terra disponiveis para plantar')
        elif resultado[0] == 1:

            cur.execute("SELECT s_j FROM fazenda WHERE iduser = %s", (ctx.author.id,))
            resultado2 = cur.fetchone()
            if resultado2[0] != 0 and resultado2[0] >= int(quant) and 50 <= int(quant) <= 1000:

                await ctx.send(f'{ctx.author.mention} | plantando...')
                total = resultado[0] - 1
                total2 = resultado2[0] - int(quant)
                cur.execute("UPDATE fazenda SET lotes=%s, plantedid='j', s_j=%s WHERE iduser=%s AND loteid=%s", (total, total2, ctx.author.id, lote.upper()))

                datanow = datetime.datetime.now()
                soma = datanow + datetime.timedelta(hours=8)
                dataa = datanow.strftime("%d/%m/%Y")
                horaa = datanow.strftime("%H:%M")

                cur.execute("UPDATE fazenda SET planted=%s, dataa=%s, horaa=%s WHERE iduser=%s AND loteid=%s", (int(quant), dataa, horaa, ctx.author.id, lote.upper()))
                conn.commit()

                cur.close()
                conn.close()

            elif resultado2[0] == 0:
                await ctx.send(f'{ctx.author.mention}, você não tem sementes!')
            elif int(quant) < 50:
                await ctx.send(f'{ctx.author.mention}, você precisa de pelo menos 50 sementes para plantar!')
            elif int(quant) > 1000:
                await ctx.send(f'{ctx.author.mention}, você pode plantar até 1000 sementes nesse lote!')

            else:
                await ctx.send(f'{ctx.author.mention}, você não tem essa quantidade toda de sementes!')



    elif channel.name == 'algodão-doce-12h':
        pass


    elif channel.name == 'marshmallow-24h':
        pass

    else:
        await ctx.send('Canal errado, bobinho(a)!')
    
    cur.close()
    conn.close()

@client.command()
async def colher(ctx, lote):
    channel = ctx.channel
    if channel.name == 'jujuba-8h':
        conn = db.connect(dbname=db_name, user=db_user, host=db_host, password=db_pass)
        cur = conn.cursor()

        cur.execute("SELECT lotes FROM fazenda WHERE iduser = %s AND loteid=%s", (ctx.author.id, lote.upper()))
        resultado_lotes = cur.fetchone()


        if resultado_lotes[0] == 1:
            await ctx.send(f'{ctx.author.mention}, você não plantou nada nesse lote!')
        

        
        elif resultado_lotes[0] == 0:
            cur.execute("SELECT dataa, horaa FROM fazenda WHERE iduser = %s AND loteid=%s", (ctx.author.id, lote.upper()))
            resultado_datas = cur.fetchmany()
            dataa = resultado_datas[0][0]
            horaa = resultado_datas[0][1]
            
            dia = dataa[:2]
            mes = dataa[3:5]
            ano = dataa[6:]
            
            horas = horaa[:2]
            minutos = horaa[3:]

            insec = datetime.datetime(int(ano), int(mes), int(dia), int(horas), int(minutos))
            colheita = insec + datetime.timedelta(hours=8)
            datenow = datetime.datetime.now()
           
            if datenow > colheita:
                cur.execute("UPDATE fazenda SET lotes=1 WHERE iduser = %s AND loteid=%s", (ctx.author.id, lote.upper()))
                cur.execute("SELECT planted FROM fazenda WHERE iduser=%s AND loteid=%s", (ctx.author.id, lote.upper()))
                planted = cur.fetchone()

                colheita_valor = ceil(planted[0] / random.randint(10, 25)) + (planted[0] * 0.1)
                
                cur.execute("SELECT cookies FROM bank WHERE iduser=%s", (ctx.author.id, ))
                cookie_antg = cur.fetchone()

                total = colheita_valor + cookie_antg[0]
                
                cur.execute("UPDATE bank SET cookies=%s WHERE iduser = %s", (total, ctx.author.id))
                cur.execute("UPDATE fazenda SET planted=0 WHERE iduser=%s AND loteid=%s", (ctx.author.id, lote.upper()))

                await ctx.send(f'{ctx.author.mention}, você ganhou {colheita_valor:.0f} cookies nessa colheita!')

                conn.commit()
                
            elif datenow < colheita:
                result = colheita - datetime.datetime.now()
                formatar = ':'.join(str(result).split(':')[:2])
                await ctx.send(f'{ctx.author.mention}, ainda não está na hora de colher!')
                """ if result < datetime.timedelta(hours=10):
                    await ctx.send(f'Tempo que falta para colher: `0{formatar}`')
                else:
                    await ctx.send(f'Tempo que falta para colher: `{formatar}`') """

    elif channel.name == 'algodão-doce-12h':
        pass
    elif channel.name == 'marshmallow-24h':
        pass

    else:
        await ctx.send('Canal errado, bobinho(a)!')
    
    
    cur.close()
    conn.close()

@client.command()
async def loja(ctx):
    emb = discord.Embed(
        title = 'LOJA DOÇURAS:',
        description = """Vendemos sementes e lotes de terra!

**SEMENTES:**

**Sementes de jujuba:**
> Pacote com 50 sementes  
> 5 cookies ...... `!buy 50j`
> 
> Pacote com 100 sementes  
> 10 cookies ...... `!buy 100j`
> 
> Pacote com 500 sementes 
> 50 cookies ...... `!buy 500j`
> 
> Pacote com 1000 sementes  
> 100 cookies ...... `!buy 1000j`
        


**Sementes de algodão-doce:**
> Pacote com 50 sementes  
> 10 cookies ...... `!buy 50ad`
> 
> Pacote com 100 sementes 
> 20 cookies ...... `!buy 100ad`
> 
> Pacote com 500 sementes 
> 100 cookies ...... `!buy 500ad`
> 
> Pacote com 1000 sementes  
> 200 cookies ...... `!buy 1000ad`




**Sementes de marshmallow:**
> Pacote com 50 sementes 
> 100 cookies ...... `!buy 50m`
> 
> Pacote com 100 sementes 
> 200 cookies ...... `!buy 100m`
> 
> Pacote com 500 sementes 
> 1000 cookies ...... `!buy 500m`
> 
> Pacote com 1000 sementes  
> 2000 cookies ...... `!buy 1000m`




**LOTES DE TERRA:**

**Lote A:**
> Lote com limite máximo de 1000  
> `Adquirido.`

**Lote B:**
> Lote com limite máximo de 5000  
> 25000 cookies ...... `!buy loteb`

**Lote C:**
> Lote com limite máximo de 15000 
> 100000 cookies ...... `!buy lotec`
        
        

        
        """,
        colour = 65280
    )

    """ emb.set_author(name='BMO') """
    #icon_url='https://cdn.discordapp.com/attachments/831946320200728577/836261314837741619/bmopng.png')

    emb.set_thumbnail(url='https://cdn.discordapp.com/attachments/831946320200728577/840316972255281232/lojinha222.png')

    
    await ctx.send(embed=emb)






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
async def rpg(ctx):
    guild = ctx.guild
    rpgRole = discord.utils.get(guild.roles, name='RPG')
    
    cargo_adicionado = False
    for role in ctx.author.roles: #pra cada role no total de cargos da pessoa...
        if role == rpgRole: #se a role for a rpgRole...
            await ctx.author.remove_roles(rpgRole) #remove o cargo
            await ctx.send(f'{ctx.author.mention} agora você não tem mais acesso à categoria RPG!') #manda a msg
            cargo_adicionado = True #redefine a var
            break #quebra o for 

    #fora do for
    if cargo_adicionado == False: #se cargo_adicionado for verdadeiro...
        await ctx.author.add_roles(rpgRole) #adicionar a role
        await ctx.send(f"{ctx.author.mention} agora você tem acesso à categoria RPG!")





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
async def ajudarpg(ctx):
    emb = discord.Embed(
        title = 'Comandos RPG:',
        description = '''
`!d [número]` 
BMO roda um dado com um número de lados escolhido

`!rodar [quantidade de dados]d[número de lados do dado]` 
BMO roda uma quantidade de dados com um número de lados escolhido e mostra o total
EX: `!rodar 3d20`
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

`!farm`
Você recebe cargo de Camponês e libera a categoria FAZENDA

`!ping`
BMO mostra sua latência em ms

`!userinfo`
BMO mostra suas informações

`!ficha [@user]`
BMO mostra a ficha de @user

`!economia`
BMO lista todos os comandos sobre a economia

`!ajudarpg`
BMO mostra os comandos específicos da Categoria RPG. Só funciona no canal {canal2.mention}

`!rpg`
Liga/Desliga a categoria RPG

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


""" data = member.created_at - datetime.timedelta(hours = -3)               # << USAR DEPOIS
 """

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
        mutedRole = discord.utils.get(guild.roles, name='Presidiário')

        if not mutedRole:
            mutedRole = await guild.create_role(name='Presidiário')

            for channel in guild.channels:
                await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True, read_messages=True)

        
        channel = client.get_channel(831197248884703283)
        emb = discord.Embed(
        title = 'PRESO(A)!!',
        description = f'{member.mention} foi algemado(a) e levado(a) para a prisão.',
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
        """ await member.send(f'Você foi silenciado(a) no {guild.name} por {reason}') """
        await member.add_roles(mutedRole, reason=reason)
        await asyncio.sleep(1800)
        await channel.send(f'{member.mention} você está solto(a) agora!')
        await member.remove_roles(mutedRole)

@client.command(description='Mutes the specified user.')
@commands.has_permissions(manage_messages=True)
async def mute1(ctx, member: discord.Member, *, reason=None):
    channel = ctx.channel
    if channel.name == 'punições-comandos':
        guild = ctx.guild
        mutedRole = discord.utils.get(guild.roles, name='Presidiário')

        if not mutedRole:
            mutedRole = await guild.create_role(name='Presidiário')

            for channel in guild.channels:
                await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True, read_messages=True)

        
        channel = client.get_channel(831197248884703283)
        emb = discord.Embed(
        title = 'PRESO(A)!!',
        description = f'{member.mention} foi algemado(a) e levado(a) para a prisão.',
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
        """ await member.send(f'Você foi silenciado(a) no {guild.name} por {reason}') """
        await member.add_roles(mutedRole, reason=reason)
        await asyncio.sleep(3600)
        await channel.send(f'{member.mention} você está solto(a) agora!')
        await member.remove_roles(mutedRole)

@client.command(description='Mutes the specified user.')
@commands.has_permissions(manage_messages=True)
async def mute2(ctx, member: discord.Member, *, reason=None):
    channel = ctx.channel
    if channel.name == 'punições-comandos':
        guild = ctx.guild
        mutedRole = discord.utils.get(guild.roles, name='Presidiário')

        if not mutedRole:
            mutedRole = await guild.create_role(name='Presidiário')

            for channel in guild.channels:
                await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True, read_messages=True)

        
        channel = client.get_channel(831197248884703283)
        emb = discord.Embed(
        title = 'PRESO(A)!!',
        description = f'{member.mention} foi algemado(a) e levado(a) para a prisão.',
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
        """ await member.send(f'Você foi silenciado(a) no {guild.name} por {reason}') """
        await member.add_roles(mutedRole, reason=reason)
        await asyncio.sleep(7200)
        await channel.send(f'{member.mention} você está solto(a) agora!')
        await member.remove_roles(mutedRole)

@client.command(description='Mutes the specified user.')
@commands.has_permissions(manage_messages=True)
async def mute3(ctx, member: discord.Member, *, reason=None):
    channel = ctx.channel
    if channel.name == 'punições-comandos':
        guild = ctx.guild
        mutedRole = discord.utils.get(guild.roles, name='Presidiário')

        if not mutedRole:
            mutedRole = await guild.create_role(name='Presidiário')

            for channel in guild.channels:
                await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True, read_messages=True)

        
        channel = client.get_channel(831197248884703283)
        emb = discord.Embed(
        title = 'PRESO(A)!!',
        description = f'{member.mention} foi algemado(a) e levado(a) para a prisão.',
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
        """ await member.send(f'Você foi silenciado(a) no {guild.name} por {reason}') """
        await member.add_roles(mutedRole, reason=reason)
        await asyncio.sleep(10800)
        await channel.send(f'{member.mention} você está solto(a) agora!')
        await member.remove_roles(mutedRole)

@client.command(description='Mutes the specified user.')
@commands.has_permissions(manage_messages=True)
async def mute10(ctx, member: discord.Member, *, reason=None):
    channel = ctx.channel
    if channel.name == 'punições-comandos':
        guild = ctx.guild
        mutedRole = discord.utils.get(guild.roles, name='Presidiário')

        if not mutedRole:
            mutedRole = await guild.create_role(name='Presidiário')

            for channel in guild.channels:
                await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True, read_messages=True)

        
        channel = client.get_channel(831197248884703283)
        emb = discord.Embed(
        title = 'PRESO(A)!!',
        description = f'{member.mention} foi algemado(a) e levado(a) para a prisão.',
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
        """ await member.send(f'Você foi silenciado(a) no {guild.name} por {reason}') """
        await member.add_roles(mutedRole, reason=reason)
        await asyncio.sleep(36000)
        await channel.send(f'{member.mention} você está solto(a) agora!')
        await member.remove_roles(mutedRole)




@client.command(description='Unmutes a specified user.')
@commands.has_permissions(manage_messages=True)
async def unmute(ctx, member: discord.Member):
    mutedRole = discord.utils.get(ctx.guild.roles, name='Presidiário')

    channel = client.get_channel(831197248884703283)
    await member.remove_roles(mutedRole)
    await channel.send(f'{member.mention} você está solto(a) agora.')
    #await member.send(f'You were unmuted in the server {ctx.guild.name}')







client.run(TOKEN)
