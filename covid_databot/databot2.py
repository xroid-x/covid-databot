import discord
import requests
import json
from random import seed
from random import random

# establish client connection
TOKEN = 'NzIxMTIwMjQ3NDEwNzIwNzc4.XuP5kA.5tRhKC2AtrkpdYkdhrurBCYvsHc'

client = discord.Client()
seed(4)
# get ISO 2-digit country codes from JSON
country_codes_raw = json.load(open("iso_country_codes.json"))
name_code_pair = {}
for c in country_codes_raw:
    name_code_pair[c['Name']] = c['Code']


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


@client.event
async def on_message(message):
    if message.content == 'covid help':
        await message.channel.send("i wanna help but i need it too :'(")
    if message.content.startswith('covid stats'):
        req_country = message.content.split()[3]
        r = requests.get('https://corona-api.com/countries/' + name_code_pair[req_country])
        json_data = json.loads(r.text)['data']

        if message.content.startswith('covid stats total_cases'):
            cases = json_data['latest_data']['confirmed']
            bot_msg = ('{0.author.mention} There are currently ' +
                       str(cases) + ' total confirmed **cases** in ' + req_country).format(message)
            await message.channel.send(bot_msg)
        
        elif message.content.startswith('covid stats total_deaths'):
            deaths = json_data['latest_data']['deaths']
            bot_msg = ('{0.author.mention} There are currently ' +
                       str(deaths) + ' total confirmed **deaths** in ' + req_country).format(message)
            await message.channel.send(bot_msg)

    if message.content.startswith('covid has_covid'):
        
        i = random()
        print(i)
        if i > 0.5:
            bot_msg = (message.content.split()[2] + 
                        ' has the coronavirus! Quarantine this fella fast!').format(message)
        else:
            bot_msg = (message.content.split()[2] +
                        ' has dodged a bullet! The lab results say negative for COVID-19!').format(message)
        await message.channel.send(bot_msg)

client.run(TOKEN)
