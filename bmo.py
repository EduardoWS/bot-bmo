import discord

from discord.ext import commands, tasks
import random

from time import sleep
import datetime

from math import ceil, floor
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

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = '**Vai com Calma!!** \nVocê poderá usar esse comando de novo em `{:.2f}s`' .format(error.retry_after)
        await ctx.send(msg)














@client.listen('on_message')
async def on_message(message):
    channel = message.channel
    if message.guild:

        if channel.name == '💸┃loja' or channel.name == '🎫┃recepção':
            if message.author == client.user:
                await asyncio.sleep(20) 
                await message.delete()
            else:
                await asyncio.sleep(20) 
                await message.delete()
        elif channel.name == '🎨┃galeria':
            if message.author:
                guild = message.guild
                tRole = discord.utils.get(guild.roles, name='Ticket Galeria')
                await message.author.remove_roles(tRole)
        elif channel.name == '💲┃obras-à-venda':
            if message.author:
                guild = message.guild
                tRole = discord.utils.get(guild.roles, name='Ticket Obras à Venda')
                await message.author.remove_roles(tRole)
            
            if 'Continue apoiando seus artistas favoritos' in message.content and message.author.bot:
                await asyncio.sleep(20)
                await message.delete()


            if message.author == client.user:
                pass
            else:
                await asyncio.sleep(20)
                await message.delete()
        elif channel.name == '💡┃ideias-desenhos':
            if message.author:
                guild = message.guild
                tRole = discord.utils.get(guild.roles, name='Ticket Ideias Desenhos')
                await message.author.remove_roles(tRole)




# VV ====================== BANCO DE DADOS Postgres ====================== VV

db_host = ""
db_user = ""
db_name = ""
db_pass = ""




# VV ====================== ECONOMIA ====================== VV

@client.command()
async def criarconta(ctx):
    channel = ctx.channel
    if channel.name == '🤖┃servos':
        conn = db.connect(dbname=db_name, user=db_user, host=db_host, password=db_pass)
        cur = conn.cursor()
        
        
        
        cur.execute("SELECT iduser FROM bank WHERE iduser = %s", (ctx.author.id,))
        resultado = cur.fetchone()

        if resultado == None:
            cur.execute("INSERT INTO bank (cookies, iduser, nome) VALUES (5, %s, %s)", (ctx.author.id, ctx.author.name))
            conn.commit()
            await ctx.send(f'{ctx.author.mention}, conta criada com sucesso! Use o comando `!mybank` para ver mais informações')
            

        else:
            await ctx.send('Você já tem uma conta! Use o comando `!mybank` para ver mais informações')
    else:
        await ctx.send('Canal errado, bobinho(a)!')

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
        await ctx.send(f'{ctx.author.mention}, você não tem uma conta criada! Crie uma conta com `!criarconta`')

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

                
                await ctx.send(f'{ctx.author.mention}, transação realizada com sucesso! Novo saldo: `{total2} cookies`')
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
> Você só poderá plantar jujubas no canal `jujuba-8h` e no `lote A`
> Você só poderá plantar algodão doce no canal `algodão-doce-12h` e no `lote B`
> Você só poderá plantar marshmallow no canal `marshmallow-24h` e no `lote C`
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
> Use `!lucrof` para ver os lucros de cada semente


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
async def buy(ctx, produto):
    channel = ctx.channel
    if channel.name == '💸┃loja':
        conn = db.connect(dbname=db_name, user=db_user, host=db_host, password=db_pass)
        cur = conn.cursor()


        #JUJUBAS============
        if produto == '50j':
            cur.execute("SELECT cookies FROM bank WHERE iduser = %s", (ctx.author.id,))
            da = cur.fetchone()
            cur.execute("SELECT s_j FROM fazenda WHERE iduser = %s AND loteid='A'", (ctx.author.id,))
            sa = cur.fetchone()
            
            if da[0] >= 5:
                totald = da[0] - 5
                totals = sa[0] + 50
                cur.execute("UPDATE fazenda SET s_j=%s WHERE iduser=%s AND loteid='A'", (totals, ctx.author.id))
                cur.execute("UPDATE bank SET cookies=%s WHERE iduser=%s", (totald, ctx.author.id))
                await ctx.send(f'''{ctx.author.mention}, compra realizada com sucesso!!
Você comprou `50 sementes de jujuba`
                ''')
                conn.commit()
            else:
                await ctx.send(f'{ctx.author.mention}, você não tem cookies suficientes para realizar essa compra!')

        elif produto == '100j':
            cur.execute("SELECT cookies FROM bank WHERE iduser = %s", (ctx.author.id,))
            da = cur.fetchone()
            cur.execute("SELECT s_j FROM fazenda WHERE iduser = %s AND loteid='A'", (ctx.author.id,))
            sa = cur.fetchone()
            
            if da[0] >= 10:
                totald = da[0] - 10
                totals = sa[0] + 100
                cur.execute("UPDATE fazenda SET s_j=%s WHERE iduser=%s AND loteid='A'", (totals, ctx.author.id))
                cur.execute("UPDATE bank SET cookies=%s WHERE iduser=%s", (totald, ctx.author.id))
                await ctx.send(f'''{ctx.author.mention}, compra realizada com sucesso!!
Você comprou `100 sementes de jujuba`
                ''')
                conn.commit()
            else:
                await ctx.send(f'{ctx.author.mention}, você não tem cookies suficientes para realizar essa compra!')
        
        elif produto == '500j':
            cur.execute("SELECT cookies FROM bank WHERE iduser = %s", (ctx.author.id,))
            da = cur.fetchone()
            cur.execute("SELECT s_j FROM fazenda WHERE iduser = %s AND loteid='A'", (ctx.author.id,))
            sa = cur.fetchone()
            
            if da[0] >= 50:
                totald = da[0] - 50
                totals = sa[0] + 500
                cur.execute("UPDATE fazenda SET s_j=%s WHERE iduser=%s AND loteid='A'", (totals, ctx.author.id))
                cur.execute("UPDATE bank SET cookies=%s WHERE iduser=%s", (totald, ctx.author.id))
                await ctx.send(f'''{ctx.author.mention}, compra realizada com sucesso!!
Você comprou `500 sementes de jujuba`
                ''')
                conn.commit()
            else:
                await ctx.send(f'{ctx.author.mention}, você não tem cookies suficientes para realizar essa compra!')

        elif produto == '1000j':
            cur.execute("SELECT cookies FROM bank WHERE iduser = %s", (ctx.author.id,))
            da = cur.fetchone()
            cur.execute("SELECT s_j FROM fazenda WHERE iduser = %s AND loteid='A'", (ctx.author.id,))
            sa = cur.fetchone()
            
            if da[0] >= 100:
                totald = da[0] - 100
                totals = sa[0] + 1000
                cur.execute("UPDATE fazenda SET s_j=%s WHERE iduser=%s AND loteid='A'", (totals, ctx.author.id))
                cur.execute("UPDATE bank SET cookies=%s WHERE iduser=%s", (totald, ctx.author.id))
                await ctx.send(f'''{ctx.author.mention}, compra realizada com sucesso!!
Você comprou `1000 sementes de jujuba`
                ''')
                conn.commit()
            else:
                await ctx.send(f'{ctx.author.mention}, você não tem cookies suficientes para realizar essa compra!')
        

        #ALGODÃO-DOCE============
        elif produto == '50ad':
            cur.execute("SELECT cookies FROM bank WHERE iduser = %s", (ctx.author.id,))
            da = cur.fetchone()
            cur.execute("SELECT s_ad FROM fazenda WHERE iduser = %s AND loteid='A'", (ctx.author.id,))
            sa = cur.fetchone()
            
            if da[0] >= 10:
                totald = da[0] - 10
                totals = sa[0] + 50
                cur.execute("UPDATE fazenda SET s_ad=%s WHERE iduser=%s AND loteid='A'", (totals, ctx.author.id))
                cur.execute("UPDATE bank SET cookies=%s WHERE iduser=%s", (totald, ctx.author.id))
                await ctx.send(f'''{ctx.author.mention}, compra realizada com sucesso!!
Você comprou `50 sementes de algodão-doce`
                ''')
                conn.commit()
            else:
                await ctx.send(f'{ctx.author.mention}, você não tem cookies suficientes para realizar essa compra!')

        elif produto == '100ad':
            cur.execute("SELECT cookies FROM bank WHERE iduser = %s", (ctx.author.id,))
            da = cur.fetchone()
            cur.execute("SELECT s_ad FROM fazenda WHERE iduser = %s AND loteid='A'", (ctx.author.id,))
            sa = cur.fetchone()
            
            if da[0] >= 20:
                totald = da[0] - 20
                totals = sa[0] + 100
                cur.execute("UPDATE fazenda SET s_ad=%s WHERE iduser=%s AND loteid='A'", (totals, ctx.author.id))
                cur.execute("UPDATE bank SET cookies=%s WHERE iduser=%s", (totald, ctx.author.id))
                await ctx.send(f'''{ctx.author.mention}, compra realizada com sucesso!!
Você comprou `100 sementes de algodão-doce`
                ''')
                conn.commit()
            else:
                await ctx.send(f'{ctx.author.mention}, você não tem cookies suficientes para realizar essa compra!')
        
        elif produto == '500ad':
            cur.execute("SELECT cookies FROM bank WHERE iduser = %s", (ctx.author.id,))
            da = cur.fetchone()
            cur.execute("SELECT s_ad FROM fazenda WHERE iduser = %s AND loteid='A'", (ctx.author.id,))
            sa = cur.fetchone()
            
            if da[0] >= 100:
                totald = da[0] - 100
                totals = sa[0] + 500
                cur.execute("UPDATE fazenda SET s_ad=%s WHERE iduser=%s AND loteid='A'", (totals, ctx.author.id))
                cur.execute("UPDATE bank SET cookies=%s WHERE iduser=%s", (totald, ctx.author.id))
                await ctx.send(f'''{ctx.author.mention}, compra realizada com sucesso!!
Você comprou `500 sementes de algodão-doce`
                ''')
                conn.commit()
            else:
                await ctx.send(f'{ctx.author.mention}, você não tem cookies suficientes para realizar essa compra!')

        elif produto == '1000ad':
            cur.execute("SELECT cookies FROM bank WHERE iduser = %s", (ctx.author.id,))
            da = cur.fetchone()
            cur.execute("SELECT s_ad FROM fazenda WHERE iduser = %s AND loteid='A'", (ctx.author.id,))
            sa = cur.fetchone()
            
            if da[0] >= 200:
                totald = da[0] - 200
                totals = sa[0] + 1000
                cur.execute("UPDATE fazenda SET s_ad=%s WHERE iduser=%s AND loteid='A'", (totals, ctx.author.id))
                cur.execute("UPDATE bank SET cookies=%s WHERE iduser=%s", (totald, ctx.author.id))
                await ctx.send(f'''{ctx.author.mention}, compra realizada com sucesso!!
Você comprou `1000 sementes de algodão-doce`
                ''')
                conn.commit()
            else:
                await ctx.send(f'{ctx.author.mention}, você não tem cookies suficientes para realizar essa compra!')

        elif produto == '1500ad':
            cur.execute("SELECT cookies FROM bank WHERE iduser = %s", (ctx.author.id,))
            da = cur.fetchone()
            cur.execute("SELECT s_ad FROM fazenda WHERE iduser = %s AND loteid='A'", (ctx.author.id,))
            sa = cur.fetchone()
            
            if da[0] >= 300:
                totald = da[0] - 300
                totals = sa[0] + 1500
                cur.execute("UPDATE fazenda SET s_ad=%s WHERE iduser=%s AND loteid='A'", (totals, ctx.author.id))
                cur.execute("UPDATE bank SET cookies=%s WHERE iduser=%s", (totald, ctx.author.id))
                await ctx.send(f'''{ctx.author.mention}, compra realizada com sucesso!!
Você comprou `1000 sementes de algodão-doce`
                ''')
                conn.commit()
            else:
                await ctx.send(f'{ctx.author.mention}, você não tem cookies suficientes para realizar essa compra!')
        
        #MARSHMALLOW============
        elif produto == '50m':
            cur.execute("SELECT cookies FROM bank WHERE iduser = %s", (ctx.author.id,))
            da = cur.fetchone()
            cur.execute("SELECT s_m FROM fazenda WHERE iduser = %s AND loteid='A'", (ctx.author.id,))
            sa = cur.fetchone()
            
            if da[0] >= 100:
                totald = da[0] - 100
                totals = sa[0] + 50
                cur.execute("UPDATE fazenda SET s_m=%s WHERE iduser=%s AND loteid='A'", (totals, ctx.author.id))
                cur.execute("UPDATE bank SET cookies=%s WHERE iduser=%s", (totald, ctx.author.id))
                await ctx.send(f'''{ctx.author.mention}, compra realizada com sucesso!!
Você comprou `50 sementes de marshmallow`
                ''')
                conn.commit()
            else:
                await ctx.send(f'{ctx.author.mention}, você não tem cookies suficientes para realizar essa compra!')

        elif produto == '100m':
            cur.execute("SELECT cookies FROM bank WHERE iduser = %s", (ctx.author.id,))
            da = cur.fetchone()
            cur.execute("SELECT s_m FROM fazenda WHERE iduser = %s AND loteid='A'", (ctx.author.id,))
            sa = cur.fetchone()
            
            if da[0] >= 200:
                totald = da[0] - 200
                totals = sa[0] + 100
                cur.execute("UPDATE fazenda SET s_m=%s WHERE iduser=%s AND loteid='A'", (totals, ctx.author.id))
                cur.execute("UPDATE bank SET cookies=%s WHERE iduser=%s", (totald, ctx.author.id))
                await ctx.send(f'''{ctx.author.mention}, compra realizada com sucesso!!
Você comprou `100 sementes de marshmallow`
                ''')
                conn.commit()
            else:
                await ctx.send(f'{ctx.author.mention}, você não tem cookies suficientes para realizar essa compra!')
        
        elif produto == '500m':
            cur.execute("SELECT cookies FROM bank WHERE iduser = %s", (ctx.author.id,))
            da = cur.fetchone()
            cur.execute("SELECT s_m FROM fazenda WHERE iduser = %s AND loteid='A'", (ctx.author.id,))
            sa = cur.fetchone()
            
            if da[0] >= 1000:
                totald = da[0] - 1000
                totals = sa[0] + 500
                cur.execute("UPDATE fazenda SET s_m=%s WHERE iduser=%s AND loteid='A'", (totals, ctx.author.id))
                cur.execute("UPDATE bank SET cookies=%s WHERE iduser=%s", (totald, ctx.author.id))
                await ctx.send(f'''{ctx.author.mention}, compra realizada com sucesso!!
Você comprou `500 sementes de marshmallow`
                ''')
                conn.commit()
            else:
                await ctx.send(f'{ctx.author.mention}, você não tem cookies suficientes para realizar essa compra!')

        elif produto == '1000m':
            cur.execute("SELECT cookies FROM bank WHERE iduser = %s", (ctx.author.id,))
            da = cur.fetchone()
            cur.execute("SELECT s_m FROM fazenda WHERE iduser = %s AND loteid='A'", (ctx.author.id,))
            sa = cur.fetchone()
            
            if da[0] >= 2000:
                totald = da[0] - 2000
                totals = sa[0] + 1000
                cur.execute("UPDATE fazenda SET s_m=%s WHERE iduser=%s AND loteid='A'", (totals, ctx.author.id))
                cur.execute("UPDATE bank SET cookies=%s WHERE iduser=%s", (totald, ctx.author.id))
                await ctx.send(f'''{ctx.author.mention}, compra realizada com sucesso!!
Você comprou `1000 sementes de marshmallow`
                ''')
                conn.commit()
            else:
                await ctx.send(f'{ctx.author.mention}, você não tem cookies suficientes para realizar essa compra!')
        
        elif produto == '2000m':
            cur.execute("SELECT cookies FROM bank WHERE iduser = %s", (ctx.author.id,))
            da = cur.fetchone()
            cur.execute("SELECT s_m FROM fazenda WHERE iduser = %s AND loteid='A'", (ctx.author.id,))
            sa = cur.fetchone()
            
            if da[0] >= 4000:
                totald = da[0] - 4000
                totals = sa[0] + 2000
                cur.execute("UPDATE fazenda SET s_m=%s WHERE iduser=%s AND loteid='A'", (totals, ctx.author.id))
                cur.execute("UPDATE bank SET cookies=%s WHERE iduser=%s", (totald, ctx.author.id))
                await ctx.send(f'''{ctx.author.mention}, compra realizada com sucesso!!
Você comprou `2000 sementes de marshmallow`
                ''')
                conn.commit()
            else:
                await ctx.send(f'{ctx.author.mention}, você não tem cookies suficientes para realizar essa compra!')
        

        #LOTES
        elif produto == 'loteb':
            cur.execute("SELECT loteid FROM fazenda WHERE iduser = %s AND loteid = 'B'", (ctx.author.id,))
            lote = cur.fetchone()

            if lote == None:
                cur.execute("SELECT cookies FROM bank WHERE iduser = %s", (ctx.author.id,))
                da = cur.fetchone()
                if da[0] >= 5890:
                    totald = da[0] - 5890
                    cur.execute("INSERT INTO fazenda (iduser, lotes, loteid, nome) VALUES (%s, 1, 'B', %s)", (ctx.author.id, ctx.author.name))
                    cur.execute("UPDATE bank SET cookies=%s WHERE iduser=%s", (totald, ctx.author.id))
                    await ctx.send(f'{ctx.author.mention}, compra realizada com sucesso!!')
                    conn.commit()

            else:
                await ctx.send(f'{ctx.author.mention}, você já possui o `lote B`')

        elif produto == 'lotec':
            cur.execute("SELECT loteid FROM fazenda WHERE iduser = %s AND loteid = 'B'", (ctx.author.id,))
            loteB = cur.fetchone()

            if loteB == None:
                await ctx.send(f'{ctx.author.mention}, você precisa ter o `lote B` antes de comprar o `lote C`')

            else:
                cur.execute("SELECT loteid FROM fazenda WHERE iduser = %s AND loteid = 'C'", (ctx.author.id,))
                loteC = cur.fetchone()

                if loteC == None:
                    cur.execute("SELECT cookies FROM bank WHERE iduser = %s", (ctx.author.id,))
                    da = cur.fetchone()
                    if da[0] >= 47390:
                        totald = da[0] - 47390
                        cur.execute("INSERT INTO fazenda (iduser, lotes, loteid, nome) VALUES (%s, 1, 'C', %s)", (ctx.author.id, ctx.author.name))
                        cur.execute("UPDATE bank SET cookies=%s WHERE iduser=%s", (totald, ctx.author.id))
                        await ctx.send(f'{ctx.author.mention}, compra realizada com sucesso!!')
                        conn.commit()

                else:
                    await ctx.send(f'{ctx.author.mention}, você já possui o `lote C`')


    else:
        await ctx.send('Canal errado, bobinho(a)!')

    cur.close()
    conn.close()

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
                    planta = 'Jujubas plantadas'
                elif plantedidA[0] == 'ad':
                    colheita = insec + datetime.timedelta(hours=12)
                    planta = 'Algodão-doce plantado'
                elif plantedidA[0] == 'm':
                    colheita = insec + datetime.timedelta(hours=24)
                    planta = 'Marshmallow plantado'
                
                

                result = colheita - datetime.datetime.now()
                formatar = ':'.join(str(result).split(':')[:2])
                if result < datetime.timedelta(hours=10):
                    if result > datetime.timedelta(hours=0):
                        formatar = f'0{formatar}'
                    else:
                        formatar = f'Pronto para colher!'
                
            
                    
                

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
> Lote A: `{planta}`
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
               
                    planta = 'Jujubas plantadas'
                elif plantedidA[0] == 'ad':
                    colheita = insec + datetime.timedelta(hours=12)
                 
                    planta = 'Algodão-doce plantado'
                elif plantedidA[0] == 'm':
                    colheita = insec + datetime.timedelta(hours=24)
                  
                    planta = 'Marshmallow plantado'
                

                result = colheita - datetime.datetime.now()
                formatar = ':'.join(str(result).split(':')[:2])
                if result < datetime.timedelta(hours=10):
                    if result > datetime.timedelta(hours=0):
                        formatar = f'0{formatar}'
                    else:
                        formatar = f'Pronto para colher!'
                


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
> Lote A: `{planta}`
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
                
 
                if plantedidB[0] == 'j':
                    colheita = insec + datetime.timedelta(hours=8)
                    
                    planta = 'Jujubas plantadas'
                elif plantedidB[0] == 'ad':
                    colheita = insec + datetime.timedelta(hours=12)
                   
                    planta = 'Algodão-doce plantado'
                elif plantedidB[0] == 'm':
                    colheita = insec + datetime.timedelta(hours=24)
                   
                    planta = 'Marshmallow plantado'
              

                result = colheita - datetime.datetime.now()
                formatar = ':'.join(str(result).split(':')[:2])
                if result < datetime.timedelta(hours=10):
                    if result > datetime.timedelta(hours=0):
                        formatar = f'0{formatar}'
                    else:
                        formatar = f'Pronto para colher!'


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
> Lote B: `{planta}`
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
                  
                    planta = 'Jujubas plantadas'
                elif plantedidA[0] == 'ad':
                    colheita = insec + datetime.timedelta(hours=12)
                    
                    planta = 'Algodão-doce plantado'
                elif plantedidA[0] == 'm':
                    colheita = insec + datetime.timedelta(hours=24)
                    
                    planta = 'Marshmallow plantado'

                cur.execute("SELECT plantedid FROM fazenda WHERE iduser=%s AND loteid='B'", (ctx.author.id, ))
                plantedidB = cur.fetchone()

                if plantedidB[0] == 'j':
                    colheitaB = insec + datetime.timedelta(hours=8)
                    plantaB = 'Jujubas plantadas'
                elif plantedidB[0] == 'ad':
                    colheitaB = insec + datetime.timedelta(hours=12)
                    plantaB = 'Algodão-doce plantado'
                elif plantedidB[0] == 'm':
                    colheitaB = insec + datetime.timedelta(hours=24)
                    plantaB = 'Marshmallow plantado'

                resultA = colheita - datetime.datetime.now()
                resultB = colheitaB - datetime.datetime.now()
                formatarA = ':'.join(str(resultA).split(':')[:2])
                formatarB = ':'.join(str(resultB).split(':')[:2])

                if resultA < datetime.timedelta(hours=10):
                    if resultA > datetime.timedelta(hours=0):
                        formatarA = f'0{formatarA}'
                    else:
                        formatarA = f'Pronto para colher!'

                if resultB < datetime.timedelta(hours=10):
                    if resultB > datetime.timedelta(hours=0):
                        formatarB = f'0{formatarB}'
                    else:
                        formatarB = f'Pronto para colher!'

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
> Lote A: `{planta}`
> Tempo que falta: `{formatarA}`
> Lote B: `{plantaB}`
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
                    planta = 'Jujubas plantadas'
                elif plantedidA[0] == 'ad':
                    colheita = insec + datetime.timedelta(hours=12)
                    planta = 'Algodão-doce plantado'
                elif plantedidA[0] == 'm':
                    colheita = insec + datetime.timedelta(hours=24)
                    planta = 'Marshmallow plantado'
                

                result = colheita - datetime.datetime.now()
                formatar = ':'.join(str(result).split(':')[:2])
                if result < datetime.timedelta(hours=10):
                    if result > datetime.timedelta(hours=0):
                        formatar = f'0{formatar}'
                    else:
                        formatar = f'Pronto para colher!'


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
> Lote A: `{planta}`
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
                
                if plantedidB[0] == 'j':
                    colheita = insec + datetime.timedelta(hours=8)
                    plantaB = 'Jujubas plantadas'
                elif plantedidB[0] == 'ad':
                    colheita = insec + datetime.timedelta(hours=12)
                    plantaB = 'Algodão-doce plantado'
                elif plantedidB[0] == 'm':
                    colheita = insec + datetime.timedelta(hours=24)
                    plantaB = 'Marshmallow plantado'
                
                
              

                result = colheita - datetime.datetime.now()
                formatar = ':'.join(str(result).split(':')[:2])
                if result < datetime.timedelta(hours=10):
                    if result > datetime.timedelta(hours=0):
                        formatar = f'0{formatar}'
                    else:
                        formatar = f'Pronto para colher!'


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
> Lote B: `{plantaB}`
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
                    planta = 'Jujubas plantadas'
                elif plantedidA[0] == 'ad':
                    colheita = insec + datetime.timedelta(hours=12)
                    planta = 'Algodão-doce plantado'
                elif plantedidA[0] == 'm':
                    colheita = insec + datetime.timedelta(hours=24)
                    planta = 'Marshmallow plantado'

                cur.execute("SELECT plantedid FROM fazenda WHERE iduser=%s AND loteid='B'", (ctx.author.id, ))
                plantedidB = cur.fetchone()

                if plantedidB[0] == 'j':
                    colheitaB = insec + datetime.timedelta(hours=8)
                    plantaB = 'Jujubas plantadas'
                elif plantedidB[0] == 'ad':
                    colheitaB = insec + datetime.timedelta(hours=12)
                    plantaB = 'Algodão-doce plantado'
                elif plantedidB[0] == 'm':
                    colheitaB = insec + datetime.timedelta(hours=24)
                    plantaB = 'Marshmallow plantado'

                resultA = colheita - datetime.datetime.now()
                resultB = colheitaB - datetime.datetime.now()
                formatarA = ':'.join(str(resultA).split(':')[:2])
                formatarB = ':'.join(str(resultB).split(':')[:2])

                if resultA < datetime.timedelta(hours=10):
                    if resultA > datetime.timedelta(hours=0):
                        formatarA = f'0{formatarA}'
                    else:
                        formatarA = f'Pronto para colher!'

                if resultB < datetime.timedelta(hours=10):
                    if resultB > datetime.timedelta(hours=0):
                        formatarB = f'0{formatarB}'
                    else:
                        formatarB = f'Pronto para colher!'

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
> Lote A: `{planta}`
> Tempo que falta: `{formatarA}`
> Lote B: `{plantaB}`
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
                        planta = 'Jujubas plantadas'
                    elif plantedidC[0] == 'ad':
                        colheita = insec + datetime.timedelta(hours=12)
                        planta = 'Algodão-doce plantado'
                    elif plantedidC[0] == 'm':
                        colheita = insec + datetime.timedelta(hours=24)
                        planta = 'Marshmallow plantado'
                    

                    result = colheita - datetime.datetime.now()
                    formatar = ':'.join(str(result).split(':')[:2])
                    if result < datetime.timedelta(hours=10):
                        if result > datetime.timedelta(hours=0):
                            formatar = f'0{formatar}'
                        else:
                            formatar = f'Pronto para colher!'


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
> Lote C: `{planta}`
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
                        planta = 'Jujubas plantadas'
                    elif plantedidA[0] == 'ad':
                        colheita = insec + datetime.timedelta(hours=12)
                        planta = 'Algodão-doce plantado'
                    elif plantedidA[0] == 'm':
                        colheita = insec + datetime.timedelta(hours=24)
                        planta = 'Marshmallow plantado'

                    cur.execute("SELECT plantedid FROM fazenda WHERE iduser=%s AND loteid='C'", (ctx.author.id, ))
                    plantedidC = cur.fetchone()

                    if plantedidC[0] == 'j':
                        colheitaC = insec + datetime.timedelta(hours=8)
                        plantaC = 'Jujubas plantadas'
                    elif plantedidC[0] == 'ad':
                        colheitaC = insec + datetime.timedelta(hours=12)
                        plantaC = 'Algodão-doce plantado'
                    elif plantedidC[0] == 'm':
                        colheitaC = insec + datetime.timedelta(hours=24)
                        plantaC = 'Marshmallow plantado'

                    resultA = colheita - datetime.datetime.now()
                    resultC = colheitaC - datetime.datetime.now()
                    formatarA = ':'.join(str(resultA).split(':')[:2])
                    formatarC = ':'.join(str(resultC).split(':')[:2])

                    if resultA < datetime.timedelta(hours=10):
                        if resultA > datetime.timedelta(hours=0):
                            formatarA = f'0{formatarA}'
                        else:
                            formatarA = f'Pronto para colher!'

                    if resultC < datetime.timedelta(hours=10):
                        if resultC > datetime.timedelta(hours=0):
                            formatarC = f'0{formatarC}'
                        else:
                            formatarC = f'Pronto para colher!'

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
> Lote A: `{planta}`
> Tempo que falta: `{formatarA}`
> Lote B: `nada foi plantado aqui`
> Lote C: `{plantaC}`
> Tempo que falta: `{formatarC}`


                    ''',
                    colour = 65280
                    )

                    
                    emb.set_thumbnail(url="https://cdn.discordapp.com/attachments/831946320200728577/840368724748795934/fazenda1.png")
                    await ctx.send(embed = emb)

            elif plantedA[0] == 1 and plantedB[0] == 0 and plantedC[0] == 0:
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
                        plantaB = 'Jujubas plantadas'
                    elif plantedidB[0] == 'ad':
                        colheita = insec + datetime.timedelta(hours=12)
                        plantaB = 'Algodão-doce plantado'
                    elif plantedidB[0] == 'm':
                        colheita = insec + datetime.timedelta(hours=24)
                        plantaB = 'Marshmallow plantado'

                    cur.execute("SELECT plantedid FROM fazenda WHERE iduser=%s AND loteid='C'", (ctx.author.id, ))
                    plantedidC = cur.fetchone()

                    if plantedidC[0] == 'j':
                        colheitaC = insec + datetime.timedelta(hours=8)
                        plantaC = 'Jujubas plantadas'
                    elif plantedidC[0] == 'ad':
                        colheitaC = insec + datetime.timedelta(hours=12)
                        plantaC = 'Algodão-doce plantado'
                    elif plantedidC[0] == 'm':
                        colheitaC = insec + datetime.timedelta(hours=24)
                        plantaC = 'Marshmallow plantado'

                    resultB = colheita - datetime.datetime.now()
                    resultC = colheitaC - datetime.datetime.now()
                    formatarB = ':'.join(str(resultB).split(':')[:2])
                    formatarC = ':'.join(str(resultC).split(':')[:2])

                    if resultB < datetime.timedelta(hours=10):
                        if resultB > datetime.timedelta(hours=0):
                            formatarB = f'0{formatarB}'
                        else:
                            formatarB = f'Pronto para colher!'

                    if resultC < datetime.timedelta(hours=10):
                        if resultC > datetime.timedelta(hours=0):
                            formatarC = f'0{formatarC}'
                        else:
                            formatarC = f'Pronto para colher!'

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
> Lote B: `{plantaB}`
> Tempo que falta: `{formatarB}`
> Lote C: `{plantaC}`
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
                        planta = 'Jujubas plantadas'
                    elif plantedidA[0] == 'ad':
                        colheita = insec + datetime.timedelta(hours=12)
                        planta = 'Algodão-doce plantado'
                    elif plantedidA[0] == 'm':
                        colheita = insec + datetime.timedelta(hours=24)
                        planta = 'Marshmallow plantado'

                    cur.execute("SELECT plantedid FROM fazenda WHERE iduser=%s AND loteid='B'", (ctx.author.id, ))
                    plantedidB = cur.fetchone()

                    if plantedidB[0] == 'j':
                        colheitaB = insec + datetime.timedelta(hours=8)
                        plantaB = 'Jujubas plantadas'
                    elif plantedidB[0] == 'ad':
                        colheitaB = insec + datetime.timedelta(hours=12)
                        plantaB = 'Algodão-doce plantado'
                    elif plantedidB[0] == 'm':
                        colheitaB = insec + datetime.timedelta(hours=24)
                        plantaB = 'Marshmallow plantado'

                    cur.execute("SELECT plantedid FROM fazenda WHERE iduser=%s AND loteid='C'", (ctx.author.id, ))
                    plantedidC = cur.fetchone()

                    if plantedidC[0] == 'j':
                        colheitaC = insec + datetime.timedelta(hours=8)
                        plantaC = 'Jujubas plantadas'
                    elif plantedidC[0] == 'ad':
                        colheitaC = insec + datetime.timedelta(hours=12)
                        plantaC = 'Algodão-doce plantado'
                    elif plantedidC[0] == 'm':
                        colheitaC = insec + datetime.timedelta(hours=24)
                        plantaC = 'Marshmallow plantado'

                    resultA = colheita - datetime.datetime.now()
                    resultB = colheitaB - datetime.datetime.now()
                    resultC = colheitaC - datetime.datetime.now()
                    formatarA = ':'.join(str(resultA).split(':')[:2])
                    formatarB = ':'.join(str(resultB).split(':')[:2])
                    formatarC = ':'.join(str(resultC).split(':')[:2])

                    if resultA < datetime.timedelta(hours=10):
                        if resultA > datetime.timedelta(hours=0):
                            formatarA = f'0{formatarA}'
                        else:
                            formatarA = f'Pronto para colher!'
                    
                    if resultB < datetime.timedelta(hours=10):
                        if resultB > datetime.timedelta(hours=0):
                            formatarB = f'0{formatarB}'
                        else:
                            formatarB = f'Pronto para colher!'

                    if resultC < datetime.timedelta(hours=10):
                        if resultC > datetime.timedelta(hours=0):
                            formatarC = f'0{formatarC}'
                        else:
                            formatarC = f'Pronto para colher!'

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
> Lote A: `{planta}`
> Tempo que falta: `{formatarA}`
> Lote B: `{plantaB}`
> Tempo que falta: `{formatarB}`
> Lote C: `{plantaC}`
> Tempo que falta: `{formatarC}`


                    ''',
                    colour = 65280
                    )

                    
                    emb.set_thumbnail(url="https://cdn.discordapp.com/attachments/831946320200728577/840368724748795934/fazenda1.png")
                    await ctx.send(embed = emb)
            




    else:
        await ctx.send('Canal errado, bobinho(a)!')




    




@client.command()
async def plantar(ctx, quant):
    channel = ctx.channel

    if channel.name == 'jujuba-8h':
        
        conn = db.connect(dbname=db_name, user=db_user, host=db_host, password=db_pass)
        cur = conn.cursor()
        

        cur.execute("SELECT lotes FROM fazenda WHERE iduser = %s AND loteid='A'", (ctx.author.id, ))
        resultado = cur.fetchone()
        
        if resultado[0] == 0:
            await ctx.send(f'{ctx.author.mention}, esse lote não está disponível para plantar!')

        elif resultado[0] == 1:

            cur.execute("SELECT s_j FROM fazenda WHERE iduser = %s AND loteid='A'", (ctx.author.id, ))
            resultado2 = cur.fetchone()

           

            if resultado2[0] != 0 and resultado2[0] >= int(quant) and 50 <= int(quant) <= 1000:

                await ctx.send(f'**{ctx.author.mention}, está PLANTANDO...**')
                

                total = resultado[0] - 1
                total2 = resultado2[0] - int(quant)
                cur.execute("UPDATE fazenda SET lotes=%s, plantedid='j' WHERE iduser=%s AND loteid='A'", (total, ctx.author.id, ))
                cur.execute("UPDATE fazenda SET s_j=%s WHERE iduser=%s AND loteid='A'", (total2, ctx.author.id))

                datanow = datetime.datetime.now()
                
                dataa = datanow.strftime("%d/%m/%Y")
                horaa = datanow.strftime("%H:%M")

                cur.execute("UPDATE fazenda SET planted=%s, dataa=%s, horaa=%s WHERE iduser=%s AND loteid='A'", (int(quant), dataa, horaa, ctx.author.id))
                conn.commit()
                await asyncio.sleep(10)
                emb = discord.Embed(
                title = 'VOCÊ PLANTOU JUJUBAS',
                description = f'''
🌱🌱🌱🌱🌱🌱🌱🌱🌱🌱🌱🌱🌱

{ctx.author.mention},
    
> Você plantou `{quant}` sementes de jujuba no seu lote `A`
> 
> Use o comando `!myfarm` para mais informações.


**Boa sorte na colheita!!**

🌱🌱🌱🌱🌱🌱🌱🌱🌱🌱🌱🌱🌱
                    ''',
                colour = 65280
                )

                

                emb.set_thumbnail(url="https://cdn.discordapp.com/attachments/831946320200728577/840330089525805096/pngwing.com_1.png")
                emb.set_image(url="https://cdn.discordapp.com/attachments/831946320200728577/841407984353280040/terra_arada2.png")
                await ctx.send(embed = emb)
                

                

            elif resultado2[0] == 0:
                await ctx.send(f'{ctx.author.mention}, você não tem sementes!')
            elif int(quant) < 50:
                await ctx.send(f'{ctx.author.mention}, você precisa de pelo menos 50 sementes para plantar!')
            elif int(quant) > 1000:
                await ctx.send(f'{ctx.author.mention}, você pode plantar até 1000 sementes no `lote A`!')
            

            else:
                await ctx.send(f'{ctx.author.mention}, você não tem essa quantidade toda de sementes!')



    elif channel.name == 'algodão-doce-12h':
        

        conn = db.connect(dbname=db_name, user=db_user, host=db_host, password=db_pass)
        cur = conn.cursor()

        cur.execute("SELECT lotes FROM fazenda WHERE iduser = %s AND loteid='B'", (ctx.author.id, ))
        resultado = cur.fetchone()
        

        if resultado == None:
                await ctx.send(f'{ctx.author.mention}, você não tem o `lote B`! Compre-o na loja.')
            
        elif resultado[0] == 0:
            await ctx.send(f'{ctx.author.mention}, esse lote não está disponível para plantar!')

        elif resultado[0] == 1:

            cur.execute("SELECT s_ad FROM fazenda WHERE iduser = %s AND loteid='A'", (ctx.author.id, ))
            resultado2 = cur.fetchone()

            

            if resultado2[0] != 0 and resultado2[0] >= int(quant) and 50 <= int(quant) <= 1500:

                await ctx.send(f'**{ctx.author.mention}, está PLANTANDO...**')
                total = resultado[0] - 1
                total2 = resultado2[0] - int(quant)
                cur.execute("UPDATE fazenda SET lotes=%s, plantedid='ad' WHERE iduser=%s AND loteid='B'", (total, ctx.author.id))
                cur.execute("UPDATE fazenda SET s_ad=%s WHERE iduser=%s AND loteid='A'", (total2, ctx.author.id))

                datanow = datetime.datetime.now()
                
                dataa = datanow.strftime("%d/%m/%Y")
                horaa = datanow.strftime("%H:%M")

                cur.execute("UPDATE fazenda SET planted=%s, dataa=%s, horaa=%s WHERE iduser=%s AND loteid='B'", (int(quant), dataa, horaa, ctx.author.id))
                conn.commit()
                await asyncio.sleep(10)
                emb = discord.Embed(
                title = 'VOCÊ PLANTOU ALGODÕES-DOCES',
                description = f'''
🌱🌱🌱🌱🌱🌱🌱🌱🌱🌱🌱🌱🌱

{ctx.author.mention},
    
> Você plantou `{quant}` sementes de algodão-doce no seu lote `B`
> 
> Use o comando `!myfarm` para mais informações.


**Boa sorte na colheita!!**

🌱🌱🌱🌱🌱🌱🌱🌱🌱🌱🌱🌱🌱
                    ''',
                colour = 65280
                )

                

                emb.set_thumbnail(url="https://cdn.discordapp.com/attachments/831946320200728577/840330089525805096/pngwing.com_1.png")
                emb.set_image(url="https://cdn.discordapp.com/attachments/831946320200728577/841407984353280040/terra_arada2.png")
                await ctx.send(embed = emb)

                

            elif resultado2[0] == 0:
                await ctx.send(f'{ctx.author.mention}, você não tem sementes!')
            elif int(quant) < 50:
                await ctx.send(f'{ctx.author.mention}, você precisa de pelo menos 50 sementes para plantar!')
            
            elif int(quant) > 1500:
                await ctx.send(f'{ctx.author.mention}, você pode plantar até 1500 sementes no `lote B`!')
            
            

            else:
                await ctx.send(f'{ctx.author.mention}, você não tem essa quantidade toda de sementes!')


    elif channel.name == 'marshmallow-24h':
        
        conn = db.connect(dbname=db_name, user=db_user, host=db_host, password=db_pass)
        cur = conn.cursor()

        cur.execute("SELECT lotes FROM fazenda WHERE iduser = %s AND loteid='C'", (ctx.author.id, ))
        resultado = cur.fetchone()
        
        if resultado == None:
                await ctx.send(f'{ctx.author.mention}, você não tem o `lote C`! Compre-o na loja.')


        elif resultado[0] == 0:
            await ctx.send(f'{ctx.author.mention}, esse lote não está disponível para plantar!')
        elif resultado[0] == 1:

            cur.execute("SELECT s_m FROM fazenda WHERE iduser = %s AND loteid='A'", (ctx.author.id, ))
            resultado2 = cur.fetchone()

            

            if resultado2[0] != 0 and resultado2[0] >= int(quant) and 50 <= int(quant) <= 2000:

                await ctx.send(f'**{ctx.author.mention}, está PLANTANDO...**')
                total = resultado[0] - 1
                total2 = resultado2[0] - int(quant)
                cur.execute("UPDATE fazenda SET lotes=%s, plantedid='m' WHERE iduser=%s AND loteid='C'", (total, ctx.author.id))
                cur.execute("UPDATE fazenda SET s_m=%s WHERE iduser=%s AND loteid='A'", (total2, ctx.author.id))

                datanow = datetime.datetime.now()
                
                dataa = datanow.strftime("%d/%m/%Y")
                horaa = datanow.strftime("%H:%M")

                cur.execute("UPDATE fazenda SET planted=%s, dataa=%s, horaa=%s WHERE iduser=%s AND loteid='C'", (int(quant), dataa, horaa, ctx.author.id))
                conn.commit()
                await asyncio.sleep(10)
                emb = discord.Embed(
                title = 'VOCÊ PLANTOU MARSHMALLOWS',
                description = f'''
🌱🌱🌱🌱🌱🌱🌱🌱🌱🌱🌱🌱🌱

{ctx.author.mention},
    
> Você plantou `{quant}` sementes de marshmallow no seu lote `C`
> 
> Use o comando `!myfarm` para mais informações.


**Boa sorte na colheita!!**

🌱🌱🌱🌱🌱🌱🌱🌱🌱🌱🌱🌱🌱
                    ''',
                colour = 65280
                )

                

                emb.set_thumbnail(url="https://cdn.discordapp.com/attachments/831946320200728577/840330089525805096/pngwing.com_1.png")
                emb.set_image(url="https://cdn.discordapp.com/attachments/831946320200728577/841407984353280040/terra_arada2.png")
                await ctx.send(embed = emb)

                

            elif resultado2[0] == 0:
                await ctx.send(f'{ctx.author.mention}, você não tem sementes!')
            elif int(quant) < 50:
                await ctx.send(f'{ctx.author.mention}, você precisa de pelo menos 50 sementes para plantar!')
            
            
            elif int(quant) > 2000:
                await ctx.send(f'{ctx.author.mention}, você pode plantar até 2000 sementes no `lote C`!')

            else:
                await ctx.send(f'{ctx.author.mention}, você não tem essa quantidade toda de sementes!')

    else:
        await ctx.send('Canal errado, bobinho(a)!')
    
    cur.close()
    conn.close()








@client.command()
async def colher(ctx):
    channel = ctx.channel
    if channel.name == 'jujuba-8h':
        
        conn = db.connect(dbname=db_name, user=db_user, host=db_host, password=db_pass)
        cur = conn.cursor()

        cur.execute("SELECT lotes FROM fazenda WHERE iduser = %s AND loteid='A'", (ctx.author.id, ))
        resultado_lotes = cur.fetchone()

        

        if resultado_lotes[0] == 1:
            await ctx.send(f'{ctx.author.mention}, você não plantou nada nesse lote!')
        
 
        
        if resultado_lotes[0] == 0: 
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
            colheita = insec + datetime.timedelta(hours=8)
            datenow = datetime.datetime.now()
            vencida = colheita + datetime.timedelta(hours=72)
            if datenow >= colheita and datenow < vencida:
                await ctx.send(f'**{ctx.author.mention}, está COLHENDO...**')
                cur.execute("UPDATE fazenda SET lotes=1 WHERE iduser = %s AND loteid='A'", (ctx.author.id, ))
                cur.execute("SELECT planted FROM fazenda WHERE iduser=%s AND loteid='A'", (ctx.author.id, ))
                planted = cur.fetchone()

                colheita_valor = ceil(planted[0] / random.randint(10, 20)) + (planted[0] * 0.1)
                lucro = colheita_valor - (planted[0] * 0.1)
                
                cur.execute("SELECT cookies FROM bank WHERE iduser=%s", (ctx.author.id, ))
                cookie_antg = cur.fetchone()

                total = colheita_valor + cookie_antg[0]
                
                cur.execute("UPDATE bank SET cookies=%s WHERE iduser = %s", (total, ctx.author.id))
                cur.execute("UPDATE fazenda SET planted=0 WHERE iduser=%s AND loteid='A'", (ctx.author.id,))

                conn.commit()
                await asyncio.sleep(10)
                emb = discord.Embed(
                title = 'VOCÊ COLHEU JUJUBAS',
                description = f'''
🌱🌱🌱🌱🌱🌱🌱🌱🌱🌱🌱🌱🌱

{ctx.author.mention},
    
> Parabéns! Ganhaste `{colheita_valor:.0f} cookies`!!
> 
> Seu lucro: `{lucro:.0f} cookies`
> 
> Você havia plantado `{planted[0]}` sementes de jujubas


Use o comando `!myfarm` para mais informações.

🌱🌱🌱🌱🌱🌱🌱🌱🌱🌱🌱🌱🌱

                    ''',
                colour = 65280
                )

                

                emb.set_thumbnail(url="https://cdn.discordapp.com/attachments/831946320200728577/840330089525805096/pngwing.com_1.png")
                emb.set_image(url="https://cdn.discordapp.com/attachments/831946320200728577/841407979856855120/jujubas2.png")
                await ctx.send(embed = emb)
                
            elif datenow < colheita:
                result = colheita - datetime.datetime.now()
                formatar = ':'.join(str(result).split(':')[:2])
                await ctx.send(f'{ctx.author.mention}, ainda não está na hora de colher!')
                if result < datetime.timedelta(hours=10):
                    await ctx.send(f'Tempo que falta para colher: `0{formatar}`')
                else:
                    await ctx.send(f'Tempo que falta para colher: `{formatar}`')
            elif vencida <= datenow:
                emb = discord.Embed(
                title = ':skull_crossbones: AS JUJUBAS ESTÃO TODAS MORTAS :skull_crossbones:',
                description = f'''

{ctx.author.mention},
    
> Você demorou muito para colher e perdeu tudo o que tinha plantado no seu lote `A`
> 
> Não ganhaste cookies nessa colheita :(


**Lembre-se: `jujubas têm até 3 dias para serem colhidas`**


                    ''',
                colour = 65280
                )

                

                emb.set_thumbnail(url="https://cdn.discordapp.com/attachments/831946320200728577/840330089525805096/pngwing.com_1.png")
                await ctx.send(embed = emb)







    elif channel.name == 'algodão-doce-12h':
        
        conn = db.connect(dbname=db_name, user=db_user, host=db_host, password=db_pass)
        cur = conn.cursor()

        cur.execute("SELECT lotes FROM fazenda WHERE iduser = %s AND loteid='B'", (ctx.author.id, ))
        resultado_lotes = cur.fetchone()

        if resultado_lotes[0] == 1:
            await ctx.send(f'{ctx.author.mention}, você não plantou nada nesse lote!')
        
        
        if resultado_lotes[0] == 0: 
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
            colheita = insec + datetime.timedelta(hours=12)
            datenow = datetime.datetime.now()
            vencida = colheita + datetime.timedelta(hours=48)
            if datenow >= colheita and datenow < vencida:
                await ctx.send(f'**{ctx.author.mention}, está COLHENDO...**')
                cur.execute("UPDATE fazenda SET lotes=1 WHERE iduser = %s AND loteid='B'", (ctx.author.id, ))
                cur.execute("SELECT planted FROM fazenda WHERE iduser=%s AND loteid='B'", (ctx.author.id, ))
                planted = cur.fetchone()

                colheita_valor = ceil(planted[0] / random.randint(6, 15)) + (planted[0] * 0.2)
                lucro = colheita_valor - (planted[0] * 0.2)
                
                cur.execute("SELECT cookies FROM bank WHERE iduser=%s", (ctx.author.id, ))
                cookie_antg = cur.fetchone()

                total = colheita_valor + cookie_antg[0]
                
                cur.execute("UPDATE bank SET cookies=%s WHERE iduser = %s", (total, ctx.author.id))
                cur.execute("UPDATE fazenda SET planted=0 WHERE iduser=%s AND loteid='B'", (ctx.author.id, ))

                conn.commit()
                await asyncio.sleep(10)
                emb = discord.Embed(
                title = 'VOCÊ COLHEU ALGODÕES-DOCES',
                description = f'''
🌱🌱🌱🌱🌱🌱🌱🌱🌱🌱🌱🌱🌱

{ctx.author.mention},
    
> Parabéns! Ganhaste `{colheita_valor:.0f} cookies`!!
> 
> Seu lucro: `{lucro:.0f} cookies`
> 
> Você havia plantado `{planted[0]}` sementes de algodão-doce


Use o comando `!myfarm` para mais informações.

🌱🌱🌱🌱🌱🌱🌱🌱🌱🌱🌱🌱🌱
                    ''',
                colour = 65280
                )

                

                emb.set_thumbnail(url="https://cdn.discordapp.com/attachments/831946320200728577/840330089525805096/pngwing.com_1.png")
                emb.set_image(url="https://cdn.discordapp.com/attachments/831946320200728577/841407969652637726/algodao-doce2.png")
                await ctx.send(embed = emb)
                
            elif datenow < colheita:
                result = colheita - datetime.datetime.now()
                formatar = ':'.join(str(result).split(':')[:2])
                await ctx.send(f'{ctx.author.mention}, ainda não está na hora de colher!')
                if result < datetime.timedelta(hours=10):
                    await ctx.send(f'Tempo que falta para colher: `0{formatar}`')
                else:
                    await ctx.send(f'Tempo que falta para colher: `{formatar}`')
            elif vencida <= datenow:
                emb = discord.Embed(
                title = ':skull_crossbones: OS ALGODÕES-DOCES ESTÃO TODOS MORTOS :skull_crossbones:',
                description = f'''

{ctx.author.mention},
    
> Você demorou muito para colher e perdeu tudo o que tinha plantado no seu lote `B`
> 
> Não ganhaste cookies nessa colheita :(


**Lembre-se: `algodões-doces têm até 2 dias para serem colhidos`**


                    ''',
                colour = 65280
                )

                

                emb.set_thumbnail(url="https://cdn.discordapp.com/attachments/831946320200728577/840330089525805096/pngwing.com_1.png")
                await ctx.send(embed = emb)






    elif channel.name == 'marshmallow-24h':
      
        conn = db.connect(dbname=db_name, user=db_user, host=db_host, password=db_pass)
        cur = conn.cursor()

        cur.execute("SELECT lotes FROM fazenda WHERE iduser = %s AND loteid='C'", (ctx.author.id, ))
        resultado_lotes = cur.fetchone()



        if resultado_lotes[0] == 1:
            await ctx.send(f'{ctx.author.mention}, você não plantou nada nesse lote!')
        
        
        if resultado_lotes[0] == 0: 
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
            colheita = insec + datetime.timedelta(hours=24)
            datenow = datetime.datetime.now()
            vencida = colheita + datetime.timedelta(hours=24)
            if datenow >= colheita and datenow < vencida:
                await ctx.send(f'**{ctx.author.mention}, está COLHENDO...**')
                cur.execute("UPDATE fazenda SET lotes=1 WHERE iduser = %s AND loteid='C'", (ctx.author.id, ))
                cur.execute("SELECT planted FROM fazenda WHERE iduser=%s AND loteid='C'", (ctx.author.id, ))
                planted = cur.fetchone()

                colheita_valor = ceil(planted[0] / random.randint(3, 10)) + (planted[0] * 2)
                lucro = colheita_valor - (planted[0] * 2)
                
                cur.execute("SELECT cookies FROM bank WHERE iduser=%s", (ctx.author.id, ))
                cookie_antg = cur.fetchone()

                total = colheita_valor + cookie_antg[0]
                
                cur.execute("UPDATE bank SET cookies=%s WHERE iduser = %s", (total, ctx.author.id))
                cur.execute("UPDATE fazenda SET planted=0 WHERE iduser=%s AND loteid='C'", (ctx.author.id, ))

                conn.commit()
                await asyncio.sleep(10)
                emb = discord.Embed(
                title = 'VOCÊ COLHEU MARSHMALLOWS',
                description = f'''
🌱🌱🌱🌱🌱🌱🌱🌱🌱🌱🌱🌱🌱

{ctx.author.mention},
    
> Parabéns! Ganhaste `{colheita_valor:.0f} cookies`!!
> 
> Seu lucro: `{lucro:.0f} cookies`
> 
> Você havia plantado `{planted[0]}` sementes de marshmallow


Use o comando `!myfarm` para mais informações.

🌱🌱🌱🌱🌱🌱🌱🌱🌱🌱🌱🌱🌱
                    ''',
                colour = 65280
                )

                

                emb.set_thumbnail(url="https://cdn.discordapp.com/attachments/831946320200728577/840330089525805096/pngwing.com_1.png")
                emb.set_image(url="https://cdn.discordapp.com/attachments/831946320200728577/841407983074541610/marshmallow2.png")
                await ctx.send(embed = emb)
                
            elif datenow < colheita:
                result = colheita - datetime.datetime.now()
                formatar = ':'.join(str(result).split(':')[:2])
                await ctx.send(f'{ctx.author.mention}, ainda não está na hora de colher!')
                if result < datetime.timedelta(hours=10):
                    await ctx.send(f'Tempo que falta para colher: `0{formatar}`')
                else:
                    await ctx.send(f'Tempo que falta para colher: `{formatar}`')
            elif vencida <= datenow:
                emb = discord.Embed(
                title = ':skull_crossbones: OS MARSHMALLOWS ESTÃO TODOS MORTOS :skull_crossbones:',
                description = f'''

{ctx.author.mention},
    
> Você demorou muito para colher e perdeu tudo o que tinha plantado no seu lote `C`
> 
> Não ganhaste cookies nessa colheita :(


**Lembre-se: `marshmallows têm até 1 dia para serem colhidos`**


                    ''',
                colour = 65280
                )

                

                emb.set_thumbnail(url="https://cdn.discordapp.com/attachments/831946320200728577/840330089525805096/pngwing.com_1.png")
                await ctx.send(embed = emb)

    else:
        await ctx.send('Canal errado, bobinho(a)!')
    
    
    cur.close()
    conn.close()

@client.command()
async def loja(ctx):
    emb = discord.Embed(
        title = 'LOJA DOÇURAS:',
        description = """

Vendemos sementes e lotes de terra!

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
> 
> Pacote com 1500 sementes  
> 300 cookies ...... `!buy 1500ad`




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
> 
> Pacote com 2000 sementes  
> 4000 cookies ...... `!buy 2000m`




**LOTES DE TERRA:**

**Lote A:**
> Lote com limite máximo de 1000  
> `Adquirido.`

**Lote B:**
> Lote com limite máximo de 1500  
> 5890 cookies ...... `!buy loteb`

**Lote C:**
> Lote com limite máximo de 2000 
> 47390 cookies ...... `!buy lotec`
        

        """,
        colour = 65280
    )

    """ emb.set_author(name='BMO') """
    #icon_url='https://cdn.discordapp.com/attachments/831946320200728577/836261314837741619/bmopng.png')

    emb.set_thumbnail(url='https://cdn.discordapp.com/attachments/831946320200728577/840316972255281232/lojinha222.png')

    
    await ctx.send(embed=emb)


@client.command()
async def lucrof(ctx):
    channel = ctx.channel
    if channel.name == '🤖┃servos' or channel.name == '🌱┃fazenda':
        emb = discord.Embed(
        title = 'LUCROS DE CADA SEMENTE:',
        description = """

Veja aqui os lucros das sementes!


**Sementes de jujuba:**
> Pacote de 50 sementes  
> Lucro: `3 a 5 cookies`
> 
> Pacote de 100 sementes  
> Lucro: `5 a 10 cookies`
> 
> Pacote de 500 sementes 
> Lucro: `25 a 50 cookies`
> 
> Pacote de 1000 sementes  
> Lucro: `50 a 100 cookies`
        


**Sementes de algodão-doce:**
> Pacote de 50 sementes  
> Lucro: `4 a 9 cookies`
> 
> Pacote de 100 sementes  
> Lucro: `7 a 17 cookies`
> 
> Pacote de 500 sementes 
> Lucro: `34 a 84 cookies`
> 
> Pacote de 1000 sementes  
> Lucro: `67 a 167 cookies`
> 
> Pacote de 1500 sementes  
> Lucro: `100 a 250 cookies`



**Sementes de marshmallow:**
> Pacote de 50 sementes  
> Lucro: `5 a 17 cookies`
> 
> Pacote de 100 sementes  
> Lucro: `10 a 34 cookies`
> 
> Pacote de 500 sementes 
> Lucro: `50 a 167 cookies`
> 
> Pacote de 1000 sementes  
> Lucro: `100 a 334 cookies`
> 
> Pacote de 2000 sementes  
> Lucro: `200 a 667 cookies`


        """,
        colour = 65280
    )

    

    emb.set_thumbnail(url='https://cdn.discordapp.com/attachments/831946320200728577/841432227413229599/stonks.jpg')

    
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


# VV ====================== ARTES ====================== VV


@client.command()
async def artes(ctx):
    channel = ctx.channel
    if channel.name == '🤖┃servos':
        guild = ctx.guild
        artesRole = discord.utils.get(guild.roles, name='Artes')
        
        cargo_adicionado = False
        for role in ctx.author.roles: 
            if role == artesRole: 
                await ctx.author.remove_roles(artesRole)
                await ctx.send(f'{ctx.author.mention}, agora você não tem mais acesso à categoria ARTES!') 
                cargo_adicionado = True 
                break 
        conn = db.connect(dbname=db_name, user=db_user, host=db_host, password=db_pass)
        cur = conn.cursor()
        cur.execute("SELECT iduser FROM bank WHERE iduser=%s", (ctx.author.id, ))
        resultado = cur.fetchone()
        
        if cargo_adicionado == False and resultado != None:
            
            await ctx.author.add_roles(artesRole) 
            await ctx.send(f"{ctx.author.mention}, agora você tem acesso à categoria ARTES!")

        elif resultado == None:
            await ctx.send(f'{ctx.author.mention}, você precisa ter uma conta no banco para poder entrar! \nUse `!criarconta` para criar uma.')

    else:
        await ctx.send('Canal errado, bobinho(a)!')


    cur.close()
    conn.close()

@client.command()
async def recep(ctx):
    channel = ctx.channel
    guild = ctx.guild
    nRole = discord.utils.get(guild.roles, name='Artista Novato')
    aRole = discord.utils.get(guild.roles, name='Artista Amador')
    eRole = discord.utils.get(guild.roles, name='Artista Experiente')
    canalobras = client.get_channel(841800199127302221)
    canalgaleria = client.get_channel(831196291819634709)
    if channel.name == '🎫┃recepção' and ctx.author.id == 611235322411352107:
        emb = discord.Embed(
        title = 'RECEPÇÃO:',
        description = f'''

Para colocar sua arte no canal {canalgaleria.mention} você precisa 
comprar um **Ticket Galeria**
Não é possível comprar dois tickets iguais!


**TICKETS**

> Ticket Galeria (apenas 1 uso)
> Preço ......... `10 cookies`
> Comando: `!tg`

> Ticket Obras à Venda (apenas 1 uso)
> Preço ......... `1 cookie`
> Comando: `!toav`


> Ticket Ideias Desenhos (apenas 1 uso)
> Preço ......... `5 cookies`
> Comando: `!tid`



**VENDAS**

Para colocar uma obra à venda você precisa copiar o id
da sua obra em {canalgaleria.mention}. 

Depois volte aqui e coloque
o seguinte comando **`!vender [id da obra] [preço]`**

Sua obra de arte será exposta à venda no canal {canalobras.mention}

Só é possível ter **`3 obras`** à venda ao mesmo tempo. Se colocar
uma quarta obra, a primeira será retirada e ninguém poderá 
comprá-la.


**OBS: se não souber copiar o id de uma mensagem, chame um 
membro da realeza para lhe ajudar.**



> {nRole.mention} é dado ao vender `1 obra`
> Valores de venda permitidos: `10 a 30 cookies`
> 
> {aRole.mention} é dado ao vender `100 obras`
> Valores de venda permitidos: `30 a 300 cookies`
> 
> {eRole.mention} é dado ao vender `500 obras`
> Valores de venda permitidos: `acima de 300 cookies`


        ''',
        colour = 16715320
    )
        await ctx.send(embed = emb)

@client.command()
async def tg(ctx):
    channel = ctx.channel
    if channel.name == '🎫┃recepção':
        conn = db.connect(dbname=db_name, user=db_user, host=db_host, password=db_pass)
        cur = conn.cursor()
        
        
        cur.execute("SELECT cookies FROM bank WHERE iduser = %s", (ctx.author.id,))
        da = cur.fetchone()
    
        if da[0] >= 10:
            guild = ctx.guild
            tgRole = discord.utils.get(guild.roles, name='Ticket Galeria')
        
            cargo_adicionado = False
            for role in ctx.author.roles:
                if role == tgRole: 
                    
                    await ctx.send(f'{ctx.author.mention}, você já tem um Ticket Galeria!')
                    cargo_adicionado = True
                    break 

            
            if cargo_adicionado == True:
                pass 

            elif cargo_adicionado == False:
                
                totald = da[0] - 10     
                cur.execute("UPDATE bank SET cookies=%s WHERE iduser=%s", (totald, ctx.author.id))
                await ctx.send(f'''{ctx.author.mention}, compra realizada com sucesso!!
Você comprou `1 Ticket Galeria` e já pode colocar uma obra sua na Galeria!
                    ''')
                conn.commit()
                guild = ctx.guild
                gRole = discord.utils.get(guild.roles, name='Ticket Galeria')
                await ctx.author.add_roles(gRole)

        else:
            await ctx.send(f'{ctx.author.mention}, você não tem cookies suficientes para realizar essa compra!')
        
        cur.close()
        conn.close()

    else:
        await ctx.send('Canal errado, bobinho(a)!')

@client.command()
async def toav(ctx):
    channel = ctx.channel
    if channel.name == '🎫┃recepção':
        conn = db.connect(dbname=db_name, user=db_user, host=db_host, password=db_pass)
        cur = conn.cursor()
        
        
        cur.execute("SELECT cookies FROM bank WHERE iduser = %s", (ctx.author.id,))
        da = cur.fetchone()
    
        if da[0] >= 1:
            
            guild = ctx.guild
            toavRole = discord.utils.get(guild.roles, name='Ticket Obras à Venda')
        
            cargo_adicionado = False
            for role in ctx.author.roles:
                if role == toavRole: 
                    
                    await ctx.send(f'{ctx.author.mention}, você já tem um Ticket Obras à Venda!')
                    cargo_adicionado = True
                    break 

            
            if cargo_adicionado == True:
                pass 

            elif cargo_adicionado == False:

                cur.execute("UPDATE bank SET cookies=cookies - 1 WHERE iduser=%s", (ctx.author.id, ))
                await ctx.send(f'''{ctx.author.mention}, compra realizada com sucesso!!
Você comprou `1 Ticket Obras à Venda` e já pode comprar uma obra!
                    ''')
                conn.commit()
                guild = ctx.guild
                gRole = discord.utils.get(guild.roles, name='Ticket Obras à Venda')
                await ctx.author.add_roles(gRole)

        else:
            await ctx.send(f'{ctx.author.mention}, você não tem cookies suficientes para realizar essa compra!')
        
        cur.close()
        conn.close()

    else:
        await ctx.send('Canal errado, bobinho(a)!')

@client.command()
async def tid(ctx):
    channel = ctx.channel
    if channel.name == '🎫┃recepção':
        conn = db.connect(dbname=db_name, user=db_user, host=db_host, password=db_pass)
        cur = conn.cursor()
        
        
        cur.execute("SELECT cookies FROM bank WHERE iduser = %s", (ctx.author.id,))
        da = cur.fetchone()
    
        if da[0] >= 5:

            guild = ctx.guild
            tidRole = discord.utils.get(guild.roles, name='Ticket Ideias Desenhos')
        
            cargo_adicionado = False
            for role in ctx.author.roles:
                if role == tidRole: 
                    
                    await ctx.send(f'{ctx.author.mention}, você já tem um Ticket Ideias Desenhos!')
                    cargo_adicionado = True
                    break 

            
            if cargo_adicionado == True:
                pass 

            elif cargo_adicionado == False:
                
                totald = da[0] - 5     
                cur.execute("UPDATE bank SET cookies=%s WHERE iduser=%s", (totald, ctx.author.id))
                await ctx.send(f'''{ctx.author.mention}, compra realizada com sucesso!!
Você comprou `1 Ticket Ideias Desenhos` e já pode pedir uma dica!
                    ''')
                conn.commit()
                guild = ctx.guild
                idRole = discord.utils.get(guild.roles, name='Ticket Ideias Desenhos')
                await ctx.author.add_roles(idRole)

        else:
            await ctx.send(f'{ctx.author.mention}, você não tem cookies suficientes para realizar essa compra!')

        cur.close()
        conn.close()
    else:
        await ctx.send('Canal errado, bobinho(a)!')


@client.command()
async def vender(ctx, idart, preço):
    channel = ctx.channel
    if channel.name == '🎫┃recepção':

        conn = db.connect(dbname=db_name, user=db_user, host=db_host, password=db_pass)
        cur = conn.cursor()
        cur.execute("SELECT idart FROM vendas WHERE iduser = %s AND idart=%s", (ctx.author.id, int(idart)))
        resultado = cur.fetchone()
        
        
        
        
        if resultado == None:
            
            channel = client.get_channel(831196291819634709)
            art = await channel.fetch_message(idart)
            
            img = art.attachments   #use img[0]
            
            if img:
                
                autor = art.author.id
                autor2 = ctx.author.id
                channelvendas = client.get_channel(841800199127302221)
                
                guild = ctx.guild
                
                amRole = discord.utils.get(guild.roles, name='Artista Amador')
                eRole = discord.utils.get(guild.roles, name='Artista Experiente')
                aRole = discord.utils.get(guild.roles, name='Artes')
                
            
                am = False
                e = False
                a = False
                for roles in ctx.author.roles:
                    if roles == aRole:
                        a = True
                        break
                    elif roles == amRole:
                        am = True
                        break
                    elif roles == eRole:
                        e = True
                        break
                if autor == autor2 and 10 <= int(preço) <= 30 and a == True:
                    

                    cur.execute("SELECT iduser FROM artistas WHERE iduser=%s", (ctx.author.id, ))
                    resultado = cur.fetchone()
                    if resultado == None:
                        cur.execute("INSERT INTO artistas (nome, iduser, totalvendas, lucro) VALUES (%s, %s, 0, 0)", (ctx.author.name, ctx.author.id))

                    cur.execute("SELECT idart FROM vendas WHERE iduser=%s", (ctx.author.id, ))
                    resultado2 = cur.fetchone()
                    if resultado2 == None:
                        cur.execute("INSERT INTO vendas (nome, iduser, vendas, preço, idart, idnum) VALUES (%s, %s, 0, %s, %s, 1)", (ctx.author.name, ctx.author.id, int(preço), int(idart)))
                    else:
                        cur.execute("SELECT idnum FROM vendas WHERE iduser=%s", (ctx.author.id, ))
                        resultado3 = cur.fetchall()
                        if len(resultado3) == 1:
                            cur.execute("INSERT INTO vendas (nome, iduser, vendas, preço, idart, idnum) VALUES (%s, %s, 0, %s, %s, 2)", (ctx.author.name, ctx.author.id, int(preço), int(idart)))
                        elif len(resultado3) == 2:
                            cur.execute("INSERT INTO vendas (nome, iduser, vendas, preço, idart, idnum) VALUES (%s, %s, 0, %s, %s, 3)", (ctx.author.name, ctx.author.id, int(preço), int(idart)))
                        elif len(resultado3) == 3:
                            cur.execute("INSERT INTO vendas (nome, iduser, vendas, preço, idart, idnum) VALUES (%s, %s, 0, %s, %s, 4)", (ctx.author.name, ctx.author.id, int(preço), int(idart)))
                            cur.execute("DELETE FROM vendas WHERE iduser=%s AND idnum=1", (ctx.author.id, ))
                            
                            cur.execute("UPDATE vendas SET idnum = 1 WHERE iduser=%s AND idnum=2", (ctx.author.id, ))
                            cur.execute("UPDATE vendas SET idnum = 2 WHERE iduser=%s AND idnum=3", (ctx.author.id, ))
                            cur.execute("UPDATE vendas SET idnum = 3 WHERE iduser=%s AND idnum=4", (ctx.author.id, ))




                    await ctx.send(f'{ctx.author.mention}, parabéns! Sua obra foi colocada à venda \nno canal {channelvendas.mention}')
                    conn.commit()

                    emb = discord.Embed(
                        title='OBRA À VENDA',
                        description=f'''

**{ctx.author.mention} está vendendo essa obra de arte!**

PREÇO: `{int(preço)} cookies`

Para comprar use `!comprar {idart}`


                        ''', colour= 15647503
                    )
                    emb.set_thumbnail(url=ctx.author.avatar_url)
                    emb.set_image(url=img[0])
                    await channelvendas.send(embed = emb)
                    cur.close()
                    conn.close()
                    
                    

                elif autor == autor2 and 30 <= int(preço) <= 300 and am == True:
                    conn = db.connect(dbname=db_name, user=db_user, host=db_host, password=db_pass)
                    cur = conn.cursor()

                    cur.execute("SELECT iduser FROM artistas WHERE iduser=%s", (ctx.author.id, ))
                    resultado = cur.fetchone()
                    if resultado == None:
                        cur.execute("INSERT INTO artistas (nome, iduser, totalvendas, lucro) VALUES (%s, %s, 0, 0)", (ctx.author.name, ctx.author.id))
                    
                    else:
                        cur.execute("SELECT idnum FROM vendas WHERE iduser=%s", (ctx.author.id, ))
                        resultado3 = cur.fetchone()
                        if len(resultado3) == 1:
                            cur.execute("INSERT INTO vendas (nome, iduser, vendas, preço, idart, idnum) VALUES (%s, %s, 0, %s, %s, 2)", (ctx.author.name, ctx.author.id, int(preço), int(idart)))
                        elif len(resultado3) == 2:
                            cur.execute("INSERT INTO vendas (nome, iduser, vendas, preço, idart, idnum) VALUES (%s, %s, 0, %s, %s, 3)", (ctx.author.name, ctx.author.id, int(preço), int(idart)))
                        elif len(resultado3) == 3:
                            cur.execute("INSERT INTO vendas (nome, iduser, vendas, preço, idart, idnum) VALUES (%s, %s, 0, %s, %s, 4)", (ctx.author.name, ctx.author.id, int(preço), int(idart)))
                            cur.execute("DELETE FROM vendas WHERE iduser=%s AND idnum=1", (ctx.author.id, ))
                            
                            cur.execute("UPDATE vendas SET idnum = 1 WHERE iduser=%s AND idnum=2", (ctx.author.id, ))
                            cur.execute("UPDATE vendas SET idnum = 2 WHERE iduser=%s AND idnum=3", (ctx.author.id, ))
                            cur.execute("UPDATE vendas SET idnum = 3 WHERE iduser=%s AND idnum=4", (ctx.author.id, ))

                    await ctx.send(f'{ctx.author.mention}, parabéns! Sua obra foi colocada à venda \nno canal {channelvendas.mention}')
                    conn.commit()

                    emb = discord.Embed(
                        title='OBRA À VENDA',
                        description=f'''

**{ctx.author.mention} está vendendo essa obra de arte!**

PREÇO: `{int(preço)} cookies`

Para comprar use `!comprar {idart}`


                        ''', colour= 15647503
                    )
                    emb.set_thumbnail(url=ctx.author.avatar_url)
                    emb.set_image(url=img[0])
                    await channelvendas.send(embed = emb)
                    cur.close()
                    conn.close()
                    
                
                elif autor == autor2 and 300 <= int(preço) and e == True:
                    conn = db.connect(dbname=db_name, user=db_user, host=db_host, password=db_pass)
                    cur = conn.cursor()

                    cur.execute("SELECT iduser FROM artistas WHERE iduser=%s", (ctx.author.id, ))
                    resultado = cur.fetchone()
                    if resultado == None:
                        cur.execute("INSERT INTO artistas (nome, iduser, totalvendas, lucro) VALUES (%s, %s, 0, 0)", (ctx.author.name, ctx.author.id))
                    
                    else:
                        cur.execute("SELECT idnum FROM vendas WHERE iduser=%s", (ctx.author.id, ))
                        resultado3 = cur.fetchone()
                        if len(resultado3) == 1:
                            cur.execute("INSERT INTO vendas (nome, iduser, vendas, preço, idart, idnum) VALUES (%s, %s, 0, %s, %s, 2)", (ctx.author.name, ctx.author.id, int(preço), int(idart)))
                        elif len(resultado3) == 2:
                            cur.execute("INSERT INTO vendas (nome, iduser, vendas, preço, idart, idnum) VALUES (%s, %s, 0, %s, %s, 3)", (ctx.author.name, ctx.author.id, int(preço), int(idart)))
                        elif len(resultado3) == 3:
                            cur.execute("INSERT INTO vendas (nome, iduser, vendas, preço, idart, idnum) VALUES (%s, %s, 0, %s, %s, 4)", (ctx.author.name, ctx.author.id, int(preço), int(idart)))
                            cur.execute("DELETE FROM vendas WHERE iduser=%s AND idnum=1", (ctx.author.id, ))
                            
                            cur.execute("UPDATE vendas SET idnum = 1 WHERE iduser=%s AND idnum=2", (ctx.author.id, ))
                            cur.execute("UPDATE vendas SET idnum = 2 WHERE iduser=%s AND idnum=3", (ctx.author.id, ))
                            cur.execute("UPDATE vendas SET idnum = 3 WHERE iduser=%s AND idnum=4", (ctx.author.id, ))

                    await ctx.send(f'{ctx.author.mention}, parabéns! Sua obra foi colocada à venda \nno canal {channelvendas.mention}')
                    conn.commit()

                    emb = discord.Embed(
                        title='OBRA À VENDA',
                        description=f'''

**{ctx.author.mention} está vendendo essa obra de arte!**

PREÇO: `{int(preço)} cookies`

Para comprar use `!comprar {idart}`


                        ''', colour= 15647503
                    )
                    emb.set_thumbnail(url=ctx.author.avatar_url)
                    emb.set_image(url=img[0])
                    await channelvendas.send(embed = emb)
                    cur.close()
                    conn.close()


                    
                elif autor != autor2:
                    await ctx.send(f'{ctx.author.mention}, ocorreu algum erro com este id da mensagem! \nCertifique-se que esse id é de sua mensagem. \nSe o erro persistir chame o Imperador.')

                elif autor == autor2 and int(preço) > 30 or int(preço) < 10 and a == True:
                    await ctx.send(f'{ctx.author.mention}, você não pode vender sua obra por esse valor! Leia o tutorial na recepção.')
                elif autor == autor2 and int(preço) > 300 or int(preço) < 30 and am == True:
                    await ctx.send(f'{ctx.author.mention}, você não pode vender sua obra por esse valor! Leia o tutorial na recepção.')
                elif autor == autor2 and int(preço) < 300 and e == True:
                    await ctx.send(f'{ctx.author.mention}, você não pode vender sua obra por esse valor! **Valorize sua arte**.')
            else:
                await ctx.send(f'{ctx.author.mention}, certifique-se que o id da mensagem que copiou tenha uma imagem.')
        
        elif resultado[0] == int(idart):
            await ctx.send(f'{ctx.author.mention}, essa obra já está à venda!!')

    else:
        await ctx.send('Canal errado, bobinho(a)!')

@client.command()
async def comprar(ctx, idart):
    channel = ctx.channel
    
    if channel.name == '💲┃obras-à-venda':
        conn = db.connect(dbname=db_name, user=db_user, host=db_host, password=db_pass)
        cur = conn.cursor()

      
        cur.execute("SELECT iduser FROM vendas WHERE idart=%s", (int(idart), ))
        iduser = cur.fetchone()

        
    
        cur.execute("SELECT cookies FROM bank WHERE iduser=%s", (ctx.author.id, ))
        da = cur.fetchone()
        cur.execute("SELECT preço FROM vendas WHERE idart=%s", (int(idart), ))
        preço = cur.fetchone()
        

        cur.execute("SELECT idart FROM vendas WHERE idart=%s", (int(idart), ))
        resultado = cur.fetchone()
        
        if resultado == None:
            await ctx.send(f'{ctx.author.mention}, obra de arte não encontrada! Certifique-se que digitou o ID certo. \nSe o ID estiver certo então o artista não está mais vendendo essa obra.')

        elif resultado != None and da[0] >= preço[0]:

            channel = client.get_channel(831196291819634709)
            art = await channel.fetch_message(idart)
            
            img = art.attachments

            autor = art.author.id
            autor2 = ctx.author.id
            if autor == autor2:
                await ctx.send(f'{ctx.author.mention}, você não pode comprar sua própria obra, bobinho(a)')

            else:
                imposto = floor(preço[0] * 35/100)

                valor = floor(preço[0] * 30/100)
                
                cur.execute("UPDATE bank SET cookies=cookies - %s WHERE iduser=%s", (preço[0], ctx.author.id))
                
                cur.execute("UPDATE bank SET cookies=cookies + %s WHERE iduser=%s", (imposto, 611235322411352107))
                cur.execute("UPDATE bank SET cookies=cookies + %s WHERE iduser=%s", (imposto, 580804486629687306))
                
                cur.execute("UPDATE bank SET cookies=cookies + %s WHERE iduser=%s", (valor, iduser[0]))
                cur.execute("UPDATE vendas SET vendas=vendas + 1 WHERE idart=%s", (int(idart), ))
                cur.execute("UPDATE artistas SET totalvendas=totalvendas + 1 WHERE iduser=%s", (iduser[0], ))
                cur.execute("UPDATE artistas SET lucro=lucro + %s WHERE iduser=%s", (valor, iduser[0]))

                cur.execute("SELECT iduser FROM nobreza WHERE iduser=%s", (ctx.author.id, ))
                nobreza = cur.fetchone()
                if nobreza == None:
                    cur.execute("INSERT INTO nobreza (nome, iduser, obras, gasto, nobre) VALUES (%s, %s, 1, %s, 0)", (ctx.author.name, ctx.author.id, preço[0]))
                else:
                    cur.execute("UPDATE nobreza SET obras=obras + 1, gasto=gasto+%s WHERE iduser=%s", (preço[0], ctx.author.id))



                channel = client.get_channel(831196291819634709)
                art = await channel.fetch_message(idart)
                
                img = art.attachments
                artista = client.get_user(iduser[0])
                await ctx.send(f'{ctx.author.mention}, compra realizada com sucesso!! \nContinue apoiando seus artistas favoritos <:Finn:837761976020631583>')
                conn.commit()
                await asyncio.sleep(20)

                cur.execute("SELECT vendas FROM vendas WHERE idart= %s", (int(idart), ))
                hall = cur.fetchone()

                if hall[0] == 10:
                    canalhall = client.get_channel(831944832925696000)
                    emb = discord.Embed(
                            title='⭐ OBRA PRIMA ⭐',
                            description=f'''

**PARABÉNS, {ctx.author.mention}!!**

Você vendeu `10 cópias` dessa obra. 

                            ''', colour= 16715320
                        )
                    emb.set_thumbnail(url=artista.avatar_url)
                    emb.set_image(url=img[0])
                    await canalhall.send(embed = emb)




            
                edu = client.get_user(611235322411352107)
                await edu.send(f'Boa chefe! Imposto pago pela compra de uma obra! \n\n`Artista:` {artista.mention} \n`Comprador:` {ctx.author.mention} \n`Imposto:` {imposto} cookies')
                await asyncio.sleep(20)
                carol = client.get_user(580804486629687306)
                await carol.send(f'Vossa majestade, tivemos um imposto pago pela compra de uma obra! \n\n`Artista:` {artista.mention} \n`Comprador:` {ctx.author.mention} \n`Imposto:` {imposto} cookies')
                await asyncio.sleep(20)

                emb = discord.Embed(
                            title='OBRA VENDIDA',
                            description=f'''

**{ctx.author.mention} comprou sua obra!**

VALOR GANHO: `{valor} cookies`


                            ''', colour= 15647503
                        )
                emb.set_thumbnail(url=ctx.author.avatar_url)
                emb.set_image(url=img[0])
                await artista.send(embed = emb)



                cur.execute("SELECT totalvendas FROM artistas WHERE iduser=%s", (iduser[0], ))
                carg = cur.fetchone()
                

                guild = ctx.guild
                
                memberart = guild.get_member(iduser[0])
            
                amRole = discord.utils.get(guild.roles, name='Artista Amador')
                eRole = discord.utils.get(guild.roles, name='Artista Experiente')
                nRole = discord.utils.get(guild.roles, name='Artista Novato')
                
                if carg[0] == 1:
                    
                    await memberart.add_roles(nRole)
                elif carg[0] == 100:
                    await memberart.remove_roles(nRole)
                    await memberart.add_roles(amRole)
                elif carg[0] == 500:
                    await memberart.remove_roles(amRole)
                    await memberart.add_roles(eRole)







                conn.commit()

        elif da[0] < preço[0]:
            await ctx.send(f'{ctx.author.send}, você não tem cookies suficientes para comprar essa obra!')




    else:
        await ctx.send('Canal errado, bobinho(a)!')

    cur.close()
    conn.close()


# VV ====================== RANKS ====================== VV

@client.command()
async def nobreza(ctx):
    channel = ctx.channel
    if channel.name == '🤖┃servos':
        conn = db.connect(dbname=db_name, user=db_user, host=db_host, password=db_pass)
        cur = conn.cursor()

        cur.execute("SELECT iduser FROM bank WHERE iduser=%s", (ctx.author.id, ))
        bank = cur.fetchone()

        cur.execute("SELECT iduser FROM fazenda WHERE iduser=%s", (ctx.author.id, ))
        farm = cur.fetchone()

        if bank == None or farm == None:
            await ctx.send(f'{ctx.author.mention}, você precisa ter uma conta no Bank e ser um Camponês. \nUse `!criarconta` para criar sua conta no Bank \nUse `!farm` para ser um Camponês')
        
        else:
            cur.execute("SELECT iduser FROM nobreza WHERE iduser=%s", (ctx.author.id, ))
            nobreza = cur.fetchone()

            if nobreza == None:
                check = '▢'
                cur.execute("INSERT INTO nobreza (nome, iduser, obras, gasto, nobre) VALUES (%s, %s, 0, 0, 0)", (ctx.author.name, ctx.author.id ))
                cur.execute("SELECT cookies FROM bank WHERE iduser=%s", (ctx.author.id, ))
                cookie = cur.fetchone()
                if cookie[0] >= 100000:
                    check = '▣'
                cur.execute("SELECT loteid FROM fazenda WHERE iduser=%s", (ctx.author.id, ))
                lotes = cur.fetchall()
                if len(lotes[0]) == 1:
                    qntlotes = 1
                elif len(lotes[0]) == 2:
                    qntlotes = 2
                elif len(lotes[0]) == 3:
                    qntlotes = 3
                    check = '▣'
                emb = discord.Embed(
                    title='💎 ┃ RUMO À NOBREZA',
                    description=f'''
──────────────────────
{ctx.author.mention}, aqui você verá seu progresso para se tornar um **NOBRE**


{check} Cookies: ` {cookie[0]} / 100.000 `

{check} Lotes: ` {qntlotes} / 3 `

▢ Gasto com Obras: ` 0 / 10.000 `

▢ Obras compradas: ` 0 / 300 `

──────────────────────
Nobres têm mais chances de se tornar um membro da realeza 👑

                    ''', colour= 2337018
                )

                emb.set_thumbnail(url=ctx.author.avatar_url)

                await ctx.send(embed = emb)

                conn.commit()

            else:
                check = '▢'
                cur.execute("SELECT nobre FROM nobreza WHERE iduser=%s", (ctx.author.id, ))
                nobre = cur.fetchone()

                cur.execute("SELECT gasto FROM nobreza WHERE iduser=%s", (ctx.author.id, ))
                gasto = cur.fetchone()
                if gasto[0] >= 10000:
                    a = True
                    check = '▣'
                cur.execute("SELECT obras FROM nobreza WHERE iduser=%s", (ctx.author.id, ))
                obras = cur.fetchone()
                if obras[0] >= 300:
                    b = True
                    check = '▣'
                cur.execute("SELECT cookies FROM bank WHERE iduser=%s", (ctx.author.id, ))
                cookie = cur.fetchone()
                if cookie[0] >= 100000:
                    c = True
                    check = '▣'
                cur.execute("SELECT loteid FROM fazenda WHERE iduser=%s", (ctx.author.id, ))
                lotes = cur.fetchall()

                if len(lotes[0]) == 1:
                    qntlotes = 1
                elif len(lotes[0]) == 2:
                    qntlotes = 2
                elif len(lotes[0]) == 3:
                    qntlotes = 3
                    d = True
                    check = '▣'

                emb = discord.Embed(
                    title='💎 ┃ RUMO À NOBREZA',
                    description=f'''
──────────────────────
{ctx.author.mention}, aqui você verá seu progresso para se tornar um **NOBRE**


{check} Cookies: ` {cookie[0]} / 100.000 `

{check} Lotes: ` {qntlotes} / 3 `

{check} Gasto com Obras: ` {gasto[0]} / 10.000 `

{check} Obras compradas: ` {obras[0]} / 300 `

──────────────────────
Nobres têm mais chances de se tornar um membro da realeza 👑

                    ''', colour= 2337018
                )

                emb.set_thumbnail(url=ctx.author.avatar_url)

                await ctx.send(embed = emb)
                
                if a == True and b == True and c == True and d == True and nobre[0] == 0:
                    cur.execute("UPDATE nobreza SET nobre=1 WHERE iduser=%s", (ctx.author.id, ))
                    guild = ctx.guild
                    nobreRole = discord.utils.get(guild.roles, name='Nobreza')
                    await ctx.author.add_roles(nobreRole)
                    await ctx.send(f"{ctx.author.mention}, PARABÉNS!! AGORA VOCÊ FAZ PARTE DA NOBREZA.")
                    conn.commit()

    else:
        await ctx.send('Canal errado, bobinho(a)!')

    cur.close()
    conn.close()

@client.command()
async def myart(ctx):
    channel = ctx.channel
    canal = client.get_channel(831196387969597451)
    if channel.name == '📄┃discussão-artística':
        conn = db.connect(dbname=db_name, user=db_user, host=db_host, password=db_pass)
        cur = conn.cursor()

        cur.execute("SELECT iduser FROM nobreza WHERE iduser=%s", (ctx.author.id, ))
        nobreza = cur.fetchone()
        if nobreza == None:
            cur.execute("INSERT INTO nobreza (nome, iduser, obras, gasto, nobre) VALUES (%s, %s, 0, 0, 0)", (ctx.author.name, ctx.author.id))
            conn.commit()

        cur.execute("SELECT iduser FROM artistas WHERE iduser=%s", (ctx.author.id, ))
        artistas = cur.fetchone()
        if artistas == None:
            cur.execute("INSERT INTO artistas (nome, iduser, totalvendas, lucro) VALUES (%s, %s, 0, 0)", (ctx.author.name, ctx.author.id))
            conn.commit()
        
        cur.execute("SELECT totalvendas FROM artistas WHERE iduser=%s", (ctx.author.id, ))
        totalvendas = cur.fetchone()
        cur.execute("SELECT lucro FROM artistas WHERE iduser=%s", (ctx.author.id, ))
        lucro = cur.fetchone()
        cur.execute("SELECT obras FROM nobreza WHERE iduser=%s", (ctx.author.id, ))
        obras = cur.fetchone()

        emb = discord.Embed(
            title='🎨 ┃ MY ART',
            description=f'''
──────────────────────
{ctx.author.mention}

🖼️ Obras vendidas: ` {totalvendas[0]} `

💸 Obras compradas: ` {obras[0]} `

💵 Lucro das vendas: ` {lucro[0]} cookies `

──────────────────────
            ''', colour = 15647503
        )

        emb.set_thumbnail(url=ctx.author.avatar_url)

        await ctx.send(embed = emb)




    else:
        await ctx.send(f'Canal errado, bobinho(a)! Você só pode usar esse comando no canal {canal.mention}')
    cur.close()
    conn.close()

@client.command()
async def rank(ctx):
    channel = ctx.channel
    if channel.name == '🤖┃servos':
        conn = db.connect(dbname=db_name, user=db_user, host=db_host, password=db_pass)
        cur = conn.cursor()
        
        cur.execute("SELECT iduser FROM bank WHERE iduser=%s", (ctx.author.id, ))
        bank = cur.fetchone()
        if bank == None:
            await ctx.send(f'{ctx.author.mention}, você não tem uma conta criada! Crie uma conta com `!criarconta`')
        else:
            cur.execute("SELECT cookies, iduser FROM bank ORDER BY cookies DESC LIMIT 5")
            resultado5 = cur.fetchall()
            
            nome1 = client.get_user(resultado5[0][1])
            nome2 = client.get_user(resultado5[1][1])
            nome3 = client.get_user(resultado5[2][1])
            nome4 = client.get_user(resultado5[3][1])
            nome5 = client.get_user(resultado5[4][1])

            cur.execute("SELECT cookies FROM bank WHERE iduser=%s", (ctx.author.id, ))
            cookiesuser = cur.fetchone()

            cur.execute("SELECT iduser FROM bank ORDER BY cookies DESC")
            iduser = cur.fetchall()
            
            for pos, n in enumerate(iduser):
                if n[0] == ctx.author.id:
                    autor = pos+1
                    break                
                
            
            if autor > 5:
                emb = discord.Embed(
                    title='🍪 ┃ RANK',
                    description=f'''
──────────────────────
{ctx.author.mention}

**PESSOAS MAIS RICAS DO REINO DOCE:**

🥇 **1º** ` {nome1.name} ` - ` {resultado5[0][0]} cookies ` 

🥈 **2º** ` {nome2.name} ` - ` {resultado5[1][0]} cookies ` 

🥉 **3º** ` {nome3.name} ` - ` {resultado5[2][0]} cookies ` 

🏅 **4º** ` {nome4.name} ` - ` {resultado5[3][0]} cookies ` 

🎖️ **5º** ` {nome5.name} ` - ` {resultado5[4][0]} cookies ` 


**SUA POSIÇÃO:**

**{autor}º** ` {ctx.author.name} ` - ` {cookiesuser[0]} cookies `
──────────────────────
                ''', colour = 16715320
            )

                emb.set_thumbnail(url=nome1.avatar_url)

                await ctx.send(embed = emb)
            
            elif 5 >= autor > 1:

                emb = discord.Embed(
                    title='🍪 ┃ RANK',
                    description=f'''
──────────────────────
{ctx.author.mention}

**PESSOAS MAIS RICAS DO REINO DOCE:**

🥇 **1º** ` {nome1.name} ` - ` {resultado5[0][0]} cookies ` 

🥈 **2º** ` {nome2.name} ` - ` {resultado5[1][0]} cookies ` 

🥉 **3º** ` {nome3.name} ` - ` {resultado5[2][0]} cookies ` 

🏅 **4º** ` {nome4.name} ` - ` {resultado5[3][0]} cookies ` 

🎖️ **5º** ` {nome5.name} ` - ` {resultado5[4][0]} cookies ` 



**PARABÉNS! VOCÊ ESTÁ NO TOP 5** <:stonks:837767012797251644>
──────────────────────
                    ''', colour = 16715320
                )

                emb.set_thumbnail(url=nome1.avatar_url)

                await ctx.send(embed = emb)



            elif autor == 1:
                emb = discord.Embed(
                    title='🍪 ┃ RANK',
                    description=f'''
──────────────────────
{ctx.author.mention}

**PESSOAS MAIS RICAS DO REINO DOCE:**

🥇 **1º** ` {nome1.name} ` - ` {resultado5[0][0]} cookies ` 

🥈 **2º** ` {nome2.name} ` - ` {resultado5[1][0]} cookies ` 

🥉 **3º** ` {nome3.name} ` - ` {resultado5[2][0]} cookies ` 

🏅 **4º** ` {nome4.name} ` - ` {resultado5[3][0]} cookies ` 

🎖️ **5º** ` {nome5.name} ` - ` {resultado5[4][0]} cookies ` 



**WOW, VOCÊ É O DOCINHO MAIS RICO DO REINO DOCE!!** <:Finn:837761976020631583>
──────────────────────
                    ''', colour = 16715320
                )

                emb.set_thumbnail(url=nome1.avatar_url)

                await ctx.send(embed = emb)

    else:
        await ctx.send('Canal errado, bobinho(a)!')
    
    cur.close()
    conn.close()


# VV ====================== COMANDOS EXCLUSIVOS DA CATEGORIA RPG ====================== VV

@client.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def rpg(ctx):
    channel = ctx.channel
    if channel.name == '🤖┃servos':
        guild = ctx.guild
        rpgRole = discord.utils.get(guild.roles, name='RPG')
        
        cargo_adicionado = False
        for role in ctx.author.roles: #pra cada role no total de cargos da pessoa...
            if role == rpgRole: #se a role for a rpgRole...
                await ctx.author.remove_roles(rpgRole) #remove o cargo
                await ctx.send(f'{ctx.author.mention}, agora você não tem mais acesso à categoria RPG!') #manda a msg
                cargo_adicionado = True #redefine a var
                break #quebra o for 

        #fora do for
        if cargo_adicionado == False: #se cargo_adicionado for verdadeiro...
            await ctx.author.add_roles(rpgRole) #adicionar a role
            await ctx.send(f"{ctx.author.mention}, agora você tem acesso à categoria RPG!")
    else:
        await ctx.send('Canal errado, bobinho(a)!')




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

colour = 16715320 #timestamp=datetime.utcnow()
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
async def realeza(ctx):
    channel = ctx.channel
    if channel.name == 'administração' and ctx.author.id == 611235322411352107:
        guild = ctx.guild
        princesa = discord.utils.get(guild.roles, name='PRINCESA')
        imperador = discord.utils.get(guild.roles, name='IMPERADOR')
        imperatriz = discord.utils.get(guild.roles, name='IMPERATRIZ')
        duque = discord.utils.get(guild.roles, name='DUQUE')
        duquesa = discord.utils.get(guild.roles, name='DUQUESA')
        conde = discord.utils.get(guild.roles, name='CONDE')
        condessa = discord.utils.get(guild.roles, name='CONDESSA')
        lord = discord.utils.get(guild.roles, name='LORDE')
        lady = discord.utils.get(guild.roles, name='LADY')
        guarda = discord.utils.get(guild.roles, name='GUARDA REAL')
        channel = client.get_channel(835225730471952431)
        emb = discord.Embed(
            title='👑 ┃ REALEZA',
            description=f'''
───────────────────────────
**Todos os cargos da Realeza:**

{princesa.mention} ➥ Cargo máximo do Reino Doce. Pertencente 
a nossa Majestade, Jujuba. **Único**

{imperador.mention} ➥ Cargo do dono deste servidor. **Único**
{imperatriz.mention} ➥ Cargo da dona deste servidor. **Único**

{duque.mention} ➥ Cargo dos amigos do imperador. **Vagas 1/3**
{duquesa.mention} ➥ Cargo das amigas do imperador. **Vagas 1/3**

{conde.mention} ➥ Cargo dos amigos do imperador. **Vagas 1/3**
{condessa.mention} ➥ Cargo das amigas do imperador. **Vagas 3/3**

{lord.mention} ➥ Cargo dos amigos do imperador. **Vagas 1/3**
{lady.mention} ➥ Cargo das amigas do imperador. **Vagas 3/3**

{guarda.mention} ➥ Eles que cortarão sua cabeça caso 
não siga as regras. **Vagas 4/5**

───────────────────────────
            ''', colour = 16715320)

        await channel.send(embed = emb)

    else:
        await ctx.send('Canal errado, bobinho(a)!')

@client.command()
async def cargoart(ctx):
    channel = ctx.channel
    if channel.name == 'administração' and ctx.author.id == 611235322411352107:
        guild = ctx.guild
        leo = discord.utils.get(guild.roles, name='Leonardo da Vinci')
        van = discord.utils.get(guild.roles, name='Vincent Van Gogh')
        dali = discord.utils.get(guild.roles, name='Salvador Dalí')
        mich = discord.utils.get(guild.roles, name='Michelangelo')
        picasso = discord.utils.get(guild.roles, name='Pablo Picasso')
        port = discord.utils.get(guild.roles, name='Candido Portinari')
        amaral = discord.utils.get(guild.roles, name='Tarsila do Amaral')
        sofo = discord.utils.get(guild.roles, name='Sofonisba Anguissola')
        ex = discord.utils.get(guild.roles, name='Artista Experiente')
        am = discord.utils.get(guild.roles, name='Artista Amador')
        nov = discord.utils.get(guild.roles, name='Artista Novato')
        art = discord.utils.get(guild.roles, name='Artes')
        tk1 = discord.utils.get(guild.roles, name='Ticket Galeria')
        tk2 = discord.utils.get(guild.roles, name='Ticket Obras à Venda')
        tk3 = discord.utils.get(guild.roles, name='Ticket Ideias Desenhos')
        canalservos = client.get_channel(831268231464353842)
        canalgaleria = client.get_channel(831196291819634709)
        canalvendas = client.get_channel(841800199127302221)
        canalideias = client.get_channel(831196504618172437)
        channel = client.get_channel(835225730471952431)
        emb = discord.Embed(
            title='🎨 ┃ ARTISTAS',
            description=f'''
───────────────────────────
**Cargos únicos:**

{leo.mention} ➥ Cargo de um artista famoso do Reino. **Vagas 1/1**
{van.mention} ➥ Cargo de um artista famoso do Reino. **Vagas 1/1**
{dali.mention} ➥ Cargo de um artista famoso do Reino. **Vagas 1/1**
{mich.mention} ➥ Cargo de um artista famoso do Reino. **Vagas 1/1**
{picasso.mention} ➥ Cargo de um artista famoso do Reino. **Vagas 1/1**
{port.mention} ➥ Cargo de um artista famoso do Reino. **Vagas 1/1**
{amaral.mention} ➥ Cargo de um artista famoso do Reino. **Vagas 1/1**
{sofo.mention} ➥ Cargo de um artista famoso do Reino. **Vagas 1/1**


**Cargos por experiência:**

{ex.mention} ➥ Cargo dado ao vender 500 obras
{am.mention} ➥ Cargo dado ao vender 100 obras
{nov.mention} ➥ Cargo dado ao vender 1 obra


**Outros:**

{art.mention} ➥ Cargo dado ao digitar `!artes` no canal {canalservos.mention}
Só quem tiver esse cargo poderá ver a categoria **ARTES**

Se usar o comando `!artes` novamente, você perderá o cargo e
a categoria **ARTES** ficará oculta.

{tk1.mention} ➥ Ticket para enviar uma obra 
no canal `{canalgaleria}`

{tk2.mention} ➥ Ticket para comprar uma obra 
no canal `{canalvendas}`

{tk3.mention} ➥ Ticket para pedir uma ideia 
no canal `{canalideias}`

───────────────────────────
            ''', colour = 16715320)

        await channel.send(embed = emb)

    else:
        await ctx.send('Canal errado, bobinho(a)!')






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







client.run('TOKEN')
