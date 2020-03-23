import discord
from discord.ext import commands
import random
import json
import os
TOKEN = 'NjkxMDQzMzg0MzgyNDU1ODA5.XngagA.gpVO4yURYqCkPcalLbtPJh8wNXA'
bot = commands.Bot(command_prefix = '!')
os.chdir(r'D:\Bot\github')
#

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


@bot.command()
@commands.has_role('Cone of Dunshire')

async def add_cone(ctx, target, num=1):
    with open('users.json', 'r') as f:
        users = json.load(f)
    if not f'{target}' in users:
        users[f'{target}'] = {}
        users[f'{target}']['cones'] = 0
    users[f'{target}']['cones'] += num
    with open('users.json', 'w') as f:
        json.dump(users, f)
    await ctx.send('The awesome {0} has {1} cones to their name!'.format(f'{target}',users[f'{target}']['cones']))


bot.run(TOKEN)
