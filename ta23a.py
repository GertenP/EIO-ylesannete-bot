import discord
from discord.ext import commands
from discord.ext.commands import MissingPermissions
import datetime
import requests
from bs4 import BeautifulSoup
import re
import random

client = commands.Bot(command_prefix="!", intents=discord.Intents.all())
värv = 0xFFA800 # oranz värv


@client.event  #ütleb et bot on online
async def on_ready():
    print('Töötan :P!')
    await client.change_presence(activity=discord.CustomActivity(name='🖥️ EIO ülesanded :) !ylesanne' ,emoji='🖥️'))

@client.command()
async def ylesanne(ctx):
    def asenda_mustrid(tekst):
        tekst = re.sub(r'\$\$\$', '', tekst)
        tekst = re.sub(r'\s\\ldots\s', '...', tekst)
        tekst = re.sub(r'\s\\ldots,\s', '...', tekst)
        tekst = re.sub(r'\s\\le\s', '<', tekst)
        return tekst
    kursused = [523943,524235,524347,524351,524691,524690,524688,524687,525211,525199]
    url = f'https://codeforces.com/group/RzG3uwfRM6/contest/{random.choice(kursused)}/problem/{random.randint(1,6)}'
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        problem_statement = soup.find('div', class_='problem-statement')
        if problem_statement:
            title = problem_statement.find('div', class_='title').text.strip()
            time_limit = problem_statement.find('div', class_='time-limit').text.strip()
            sisu = asenda_mustrid(problem_statement.find('div', class_='').text.strip())
            memory_limit = problem_statement.find('div', class_='memory-limit').text.strip()
            input_spec = asenda_mustrid(problem_statement.find_all('div', class_='input-specification')[0].text.strip())
            output_spec = asenda_mustrid(problem_statement.find_all('div', class_='output-specification')[0].text.strip())
            example = problem_statement.find_all('div', class_='sample-test')[0].text.strip()

            embed = discord.Embed(title=f"Ülesanne: {title[3:]}", description=f"**Ajalimiit**:{time_limit[19:]}\n**Mälulimiit**:{memory_limit[21:]}\n**Punkte**:{sisu[:3]}\n{sisu[10:]}\n\n**Sisend**:\n{input_spec[5:]}\n**Väljund**:\n{output_spec[6:]}",color=värv)
            naide = discord.Embed(description=f"-------------------------------------------------------------------------------------\n{example}\n-------------------------------------------------------------------------------------",color=värv)
            await ctx.send(embed=embed)
            await ctx.send(embed=naide)
        else:
            pekki = discord.Embed(description=f"Ei leia ülesannet 🙈 ", color=värv)
            await ctx.send(embed=pekki)
    else:
        pekki = discord.Embed(description=f"Status code: {response.status_code}🙈", color=värv)
        await ctx.send(embed=pekki)
@client.command()

async def tere(ctx):
    embed = discord.Embed(title="Tere", description="Tere!", color=värv)
    await ctx.send(embed=embed)

client.run("token")