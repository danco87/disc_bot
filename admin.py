import discord
from discord.ext import commands
import random
import json
import os
TOKEN = 'NjkxMDQzMzg0MzgyNDU1ODA5.XnbVOw.QG-44nyui7icx4V8QJ3FpzbTNdU'
bot = commands.Bot(command_prefix = '!')
os.chdir(r'D:\Bot\github')


@bot.event
async def on_ready():
    print('Bot is ready.')


@bot.event
async def on_member_join(member):
    with open('users.json', 'r') as f:
        users = json.load(f)


    await update_data(users, member)


    with open('users.json', 'w') as f:
        json.dump(users, f)



@bot.event
async def on_message(message):
    #if message.author.bot == False:
    with open('users.json', 'r') as f:
        users = json.load(f)

    await update_data(users, message.author)
    await add_experience(users, message.author, 5)
    await level_up(users, message.author, message)


    with open('users.json', 'w') as f:
        json.dump(users, f)


async def update_data(users, user):
    if not f'{user.id}' in users:
        users[f'{user.id}'] = {}
        users[f'{user.id}']['experience'] = 0
        users[f'{user.id}']['level'] = 1


async def add_experience(users, user, exp):
    users[f'{user.id}']['experience'] += exp

async def level_up(users, user, message):
    experience = users[f'{user.id}']['experience']
    lvl_start = users[f'{user.id}']['level']
    lvl_end = int(experience ** (1/4))
    if lvl_start < lvl_end:
        await message.channel.send(f'{user.mention} has leveled up to level {lvl_end}')
        users[f'{user.id}']['level'] = lvl_end
bot.run(TOKEN)
