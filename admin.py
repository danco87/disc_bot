import discord
from discord.ext import commands
import json
import os
import pandas as pd

TOKEN = 'NjkxMDQzMzg0MzgyNDU1ODA5.Xngzfw.L-4N3I-kto-KdYP9mK0A8201xWQ'
bot = commands.Bot(command_prefix = '!')
os.chdir(r'D:\Bot\github')

# df = pd.read_json('users.json')
# df2 = df.T




@bot.event
async def on_ready():
    print('Bot is ready.')



@bot.command()
@commands.has_role('Cone of Dunshire')

async def add_cone(ctx, target, num=1):
    with open('users.json', 'r') as f:
        users = json.load(f)            #read the json
    if not f'{target}' in users:        #create a entry for the user if one doesn't already exist
        users[f'{target}'] = {}
        users[f'{target}']['cones'] = 0
    users[f'{target}']['cones'] += num      #modify the number of cones
    with open('users.json', 'w') as f:      #write the changes to the json
        json.dump(users, f)
    await ctx.send('The awesome {0} has {1} cones to their name!'.format(f'{target}',users[f'{target}']['cones']))

@bot.command()
@commands.has_role('Cone of Dunshire')

async def remove_cone(ctx, target, num=1):
    with open('users.json', 'r') as f:
        users = json.load(f)            #read the json
    if not f'{target}' in users:        #create a entry for the user if one doesn't already exist
        users[f'{target}'] = {}
        users[f'{target}']['cones'] = 0
    users[f'{target}']['cones'] -= num  #modify the number of cones
    with open('users.json', 'w') as f:  #write the changes to the json
        json.dump(users, f)
    await ctx.send('The awesome {0} has {1} cones to their name!'.format(f'{target}',users[f'{target}']['cones']))

@bot.command()
async def show_cones(ctx,target=None):
    target = target
    with open('users.json', 'r') as f:
        users = json.load(f)
    if target == None:
        target = '<@!{}>'.format(ctx.author.id)
    elif target == 'leader':
        df = pd.read_json('users.json')
        df2 = df.T
        await ctx.send(df2.sort_values(by=['cones'], ascending=False))
    elif f'{target}' in users:
        await ctx.send('{0} has {1} cones.'.format(f'{target}', users[f'{target}']['cones']))
    else:
         await ctx.send('This user has no cones yet.')


bot.run(TOKEN)
