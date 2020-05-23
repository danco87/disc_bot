import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
import json
import os
import pandas as pd
import random
import scipy
from scipy import stats
import datetime


pd.set_option('display.max_columns', None)

TOKEN = ''
bot = commands.Bot(command_prefix = '.')
os.chdir(r'D:\Bot\github')

#betting multipliers
low = 1.25
medium = 2
high = 2.5
higher = 4
highest = 6

#cone images in url format
bronze_cone = 'https://i.imgur.com/yHO3bsl.png'
silver_cone = 'https://i.imgur.com/ePD2lkm.png'
gold_cone = 'https://i.imgur.com/P5xtXBb.png'

#minimum number of cones someone can have
minimum_cones = 4

#bet max multiplier (rewards players for betting all of their cones)
bet_max = 1.25

#percentile brackets
higher_bracket = 95
high_bracket = 75
medium_bracket = 50
low_bracket = 25


#This is an all-purpose bot for The Cone Zone
@bot.event
async def on_ready():
    print('Bot is ready.')

@bot.event
#creates an account in our system when a user joins the server
async def on_member_join(member):
    with open('users.json', 'r') as f:
        users = json.load(f)            #read the json
    target = member.id
    if not f'{target}' in users:        #create a entry for the user if one doesn't already exist
        users[f'{target}'] = {}
        users[f'{target}']['cones'] = minimum_cones
        users[f'{target}']['multiplier'] = higher
        users[f'{target}']['bet'] = 0
        users[f'{target}']['team'] = 0
        users[f'{target}']['nickname'] = member.mention
        users[f'{target}']['admin'] = 0
        users[f'{target}']['bid'] = 0
        users[f'{target}']['points'] = 0
        role = discord.utils.get(member.guild.roles, name = "Agility Cone")
        await member.add_roles(role)
    with open('users.json', 'w') as f:  #write the changes to the json
        json.dump(users, f)

@bot.event
@has_permissions(manage_messages=True)
#restricts use of specific emojis to specific roles
async def on_message(message):
    if ':agility_cone:' in message.content:
        role = discord.utils.get(message.author.guild.roles, name="Agility Cone")
        if role not in message.author.roles:
             await message.delete()
             await message.channel.send('{} just tried to use an emoji they aren\'t allowed to use!'.format(message.author))
    if ':cinder_cone:' in message.content:
        role = discord.utils.get(message.author.guild.roles, name="Cinder Cone")
        if role not in message.author.roles:
             await message.delete()
             await message.channel.send('{} just tried to use an emoji they aren\'t allowed to use!'.format(message.author))
    if ':sugar_cone:' in message.content:
        role = discord.utils.get(message.author.guild.roles, name="Sugar Cone")
        if role not in message.author.roles:
             await message.delete()
             await message.channel.send('{} just tried to use an emoji they aren\'t allowed to use!'.format(message.author))
    await bot.process_commands(message)

@bot.command()
@commands.has_role('Cone of Dunshire')
async def tableflip(ctx):
    await ctx.send('(ノಠ益ಠ)ノ彡┻━┻')

@bot.command()
async def cone_emojis(ctx, target):
    with open('users.json', 'r') as f:
        users = json.load(f)            #read the json
    if users[target]['points'] == 'admin':
        #admin_cone
        return bronze_cone
    if users[target]['points'] >= 6:
        #obsidian
        pass
    elif users[target]['points'] >= 4:
        #diamond
        pass
    elif users[target]['points'] >= 2:
        return gold_cone
    elif users[target]['points'] >= 1:
        return silver_cone
    else:
        return bronze_cone

@bot.command()
async def testembed(ctx):
    test_embed = discord.Embed(
        title = 'Title',
        description = 'This is a description.',
        color = discord.Color.blue()
    )

    test_embed.set_footer(text='This is a footer.')
    test_embed.set_image(url='https://i.imgur.com/fCK5I1s.jpg')
    test_embed.set_thumbnail(url='https://i.imgur.com/fCK5I1s.jpg')
    test_embed.set_author(name='Author Name', icon_url='https://imgur.com/a/x2uYN8i')
    test_embed.add_field(name='Field Name', value='Field Value', inline=False)
    test_embed.add_field(name='Field Name', value='Field Value', inline=True)
    test_embed.add_field(name='Field Name', value='Field Value', inline=True)

    await ctx.send(embed=test_embed)

@bot.command()
@commands.has_role('Cone of Dunshire')
#as the name suggests, this will reset all cone values to the minimum cones value.
async def firesail(ctx):
    with open('users.json', 'r') as f:
        users = json.load(f)            #read the json
    for user in users:
        users[user]['cones'] = minimum_cones
    with open('users.json', 'w') as f:  #write the changes to the json
        json.dump(users, f)
    await ctx.send('Everything has been burnt to the ground. When the going gets tough, the tough get going.')

@bot.command()
#function for placing bids for dictatorship
async def bid(ctx, bid):
    with open('users.json', 'r') as f:
        users = json.load(f)
    bids = int(bid)
    if 0 < bids <= int(users['<@!{}>'.format(ctx.author.id)]['cones']):
        users['<@!{}>'.format(ctx.author.id)]['bid'] = bids
        await ctx.send('You have placed a bid to become the next Dictator. How bold.')
    else:
        await ctx.send('Your ambition is greater than your reality. Try bidding within your means.')
    with open('users.json', 'w') as f:  #write the changes to the json
        json.dump(users, f)

@bot.command()
@commands.has_role('Cone of Dunshire')
#resets all bids to 0
async def reset_bids(ctx):
    with open('users.json', 'r') as f:
        users = json.load(f)
    for user in users:
        users[user]['bid'] = 0
    with open('users.json', 'w') as f:  #write the changes to the json
        json.dump(users, f)
    await ctx.send('All bids to become The Dictator have been reset.')

@bot.command()
#shows curent bids
async def show_bids(ctx):
    with open('users.json', 'r') as f:
        users = json.load(f)
    df = pd.read_json('users.json') #creates a dataframe out of the json
    df = df.T
    df['names'] = df.index
    df = df.set_index('bid')
    df = df.drop(columns=['names', 'cones', 'team', 'admin', 'bet', 'multiplier', 'points'])
    df = df.drop(0)
    await ctx.send(df.to_string(index=False)) #sends the dataframe, exluding index to keep the bids secret
    with open('users.json', 'w') as f:  #write the changes to the json
        json.dump(users, f)

@bot.command()
#shows curent points
async def show_points(ctx):
    with open('users.json', 'r') as f:
        users = json.load(f)
    df = pd.read_json('users.json') #creates a dataframe out of the json
    df = df.T
    df['names'] = df.index
    df = df.set_index('points')
    df = df.drop(columns=['names', 'cones', 'team', 'admin', 'bet', 'multiplier', 'bid'])
    df = df.drop(0)
    await ctx.send(df.sort_values(by=['points'], ascending=False))
    with open('users.json', 'w') as f:  #write the changes to the json
        json.dump(users, f)

@bot.command()
@commands.has_role('Cone of Dunshire')
#collect the bids
async def collect_bids(ctx):
    with open('users.json', 'r') as f:
        users = json.load(f)
    df = pd.read_json('users.json') #creates a dataframe out of the json
    df = df.T
    df['names'] = df.index
    df['bid'] = df.bid.astype(int)
    df = df.sort_values(by=['bid'], ascending=False)
    winner = df.names.iloc[0] #selects the highest bid, if a tie occurs it will randomly select one
    temp = users[winner]['cones']
    users[winner]['cones'] -= users[winner]['bid'] #removes a cone from the top bidders stash
    if users[winner]['cones'] < minimum_cones:
        users[winner]['cones'] = minimum_cones
    await ctx.send('The new dictator is {}!'.format(winner))
    with open('users.json', 'w') as f:  #write the changes to the json
        json.dump(users, f)
    await reset_bids(ctx)

@bot.command(aliases=['cancel_bets'])
@commands.has_role('Cone of Dunshire')
#sets all bets to 0, refunding the bet
async def bet_cancel(ctx):
    with open('users.json', 'r') as f:
        users = json.load(f)            #read the json
    for user in users:
        users[user]['cones'] += users[user]['bet']
        users[user]['bet'] = 0
    with open('users.json', 'w') as f:  #write the changes to the json
        json.dump(users, f)
    await ctx.send('The Cone House has returned all the bets.')
    await set_odds(ctx)

@bot.command()
@commands.has_role('Cone of Dunshire')
#sets all bets to 0, refunding the bet
async def rising_tide(ctx):
    with open('users.json', 'r') as f:
        users = json.load(f)            #read the json
    for user in users:
        if users[user]['cones'] < minimum_cones:
            users[user]['cones'] = minimum_cones
    with open('users.json', 'w') as f:  #write the changes to the json
        json.dump(users, f)
    await ctx.send('Confucius says: A rising tide raises all ships.')

@bot.command()
@has_permissions(manage_roles=True)
@commands.has_role('Cone of Dunshire')
#sets all roles according to the users standing on the cone leaderboard
async def set_roles(ctx):
    with open('users.json', 'r') as f:
        users = json.load(f)            #read the json
    df = pd.read_json('users.json') #creates a dataframe out of the json
    df = df.T #transposes the dataframe
    df['names'] = df.index #sets the value of names to be equal to the index (which is the user ID)
    df.cones = df.cones.astype(int)
    df = df.drop(columns=['nickname', 'team', 'bet', 'multiplier']) #drops useless columns
    df = df[df.admin != 1] #removes admins from the dataframe (admins dont get ranked)
    df = df.sort_values(by=['cones'], ascending=False) #sorts the users by how many cones they have
    df_sugar = df.iloc[0:3]  #creates a new dataframe for each role
    df_cinder = df.iloc[3:8]
    df_agility = df.iloc[8:]
    sugar = discord.utils.get(ctx.guild.roles, name = "Sugar Cone")  #creates an object for each role
    cinder = discord.utils.get(ctx.guild.roles, name = "Cinder Cone")
    agility = discord.utils.get(ctx.guild.roles, name = "Agility Cone")
    for id in df_sugar.index:
        try:
            user = id.strip('<>@!')
            member_id = ctx.guild.get_member(user_id=int(user)) #pulls a member object from the user id, allows me to add and remove roles from the member in discord
            users[id]['points'] += 1
            await member_id.add_roles(sugar, cinder, agility)
        except:
            pass
    for id in df_cinder.index:
        try:
            user = id.strip('<>@!')
            member_id = ctx.guild.get_member(user_id=int(user))
            await member_id.add_roles(cinder, agility)
            await member_id.remove_roles(sugar)
        except:
            pass
    for id in df_agility.index:
        try:
            user = id.strip('<>@!')
            member_id = ctx.guild.get_member(user_id=int(user))
            await member_id.add_roles(agility)
            await member_id.remove_roles(sugar, cinder)
        except:
            pass
    await ctx.send('The roles have been updated for the week! Better luck next time. Remember: Cone\'s will set you free, So keep on betting!')
    with open('users.json', 'w') as f:  #write the changes to the json
        json.dump(users, f)

@bot.command(aliases=['collect'])
@commands.has_role('Cone of Dunshire')
#sets all bets to 0, doesnt refund
async def bet_collect(ctx):
    with open('users.json', 'r') as f:
        users = json.load(f)            #read the json
    for user in users:
        if users[user]['cones'] < minimum_cones:
            users[user]['cones'] = minimum_cones
        users[user]['bet'] = 0
    with open('users.json', 'w') as f:  #write the changes to the json
        json.dump(users, f)
    await ctx.send('The Cone House has collected all the bets. Thanks for playing please come again.')
    await set_odds(ctx)

@bot.command()
@commands.has_role('Cone of Dunshire')
#sets all of the odds
async def set_odds(ctx):
    with open('users.json', 'r') as f:
        users = json.load(f)            #read the json
    df = pd.read_json('users.json') #creates a dataframe out of the json
    df = df.T
    df['names'] = df.index
    df.cones = df.cones.astype(int)
    df = df.drop(columns=['names', 'team'])
    for user in users:  #adjusts the multiplier for betting based on percentile position
        cones = users[user]['cones']
        percentile = scipy.stats.percentileofscore(df.cones, cones)
        if users[user]['bet'] < 1:
            if percentile < low_bracket:
                users[user]['multiplier'] = highest
            elif percentile < medium_bracket:
                users[user]['multiplier'] = higher
            elif percentile < high_bracket:
                users[user]['multiplier'] = high
            elif percentile < higher_bracket:
                users[user]['multiplier'] = medium
            else:
                users[user]['multiplier'] = low
    await ctx.send('All multipliers have been reset.')
    with open('users.json', 'w') as f:  #write the changes to the json
        json.dump(users, f)

@bot.command()
#allows players to set their bet
async def bet(ctx, num):
    with open('users.json', 'r') as f:
        users = json.load(f)            #read the json
    if num == 'random': #allows players to place a random bet
        num = random.randint(1,int(users['<@!{}>'.format(ctx.author.id)]['cones']))
        await ctx.send('The brave {} is betting a random amount!'.format(f'<@!{ctx.author.id}>'))
    if num == 'max':
        num = users['<@!{}>'.format(ctx.author.id)]['cones']
    num = int(num) #changes everything passed in to an int to avoid breaking
    df = pd.read_json('users.json') #creates a dataframe out of the json
    df = df.T
    df['names'] = df.index
    df.cones = df.cones.astype(int)
    df = df.drop(columns=['names', 'team'])
    target = '<@!{}>'.format(ctx.author.id)
    cones = users[f'{target}']['cones']
    emoji = await cone_emojis(ctx, target=target)
    nickname = users[f'{target}']['nickname']
    percentile = scipy.stats.percentileofscore(df.cones, cones) #gets the percentil placement of each player
    if num <= 0: #prevents negatives or zero bets
        await ctx.send('Make a better bet.')
    else:
        if users['<@!{}>'.format(ctx.author.id)]['bet'] == 0: #players can only place bets if their bet is at 0 to prevent double bets.
            if num <= users['<@!{}>'.format(ctx.author.id)]['cones']: #makes sure the player has enough cones to pay for the bet
                users['<@!{}>'.format(ctx.author.id)]['bet'] = num
                users['<@!{}>'.format(ctx.author.id)]['cones'] -= num
                if int(cones) == num: #check to see if the player is betting all of their cones
                    users[f'{target}']['multiplier'] = users[f'{target}']['multiplier'] * bet_max
                    potential_gain = int(1 + (users[f'{target}']['multiplier'] * users[f'{target}']['bet']) - users[f'{target}']['bet'])
                    bet_embed = discord.Embed(
                        title = 'The Cones Have Been Bet',
                        color = discord.Color(0x001FFF)
                    )
                    bet_embed.set_author(name=nickname, icon_url=emoji)
                    bet_embed.add_field(name='Cones bet:', value=num, inline=True)
                    bet_embed.add_field(name='Potential gain:', value=potential_gain, inline=True)
                    await ctx.send(embed=bet_embed)
                elif percentile < low_bracket:  #checks what percentile the player is in to adjust the multiplier
                    users[f'{target}']['multiplier'] = highest
                    potential_gain = int(1 + (users[f'{target}']['multiplier'] * users[f'{target}']['bet']) - users[f'{target}']['bet'])
                    bet_embed = discord.Embed(
                        title = 'The Cones Have Been Bet',
                        color = discord.Color(0x001FFF)
                    )
                    bet_embed.set_author(name=nickname, icon_url=emoji)
                    bet_embed.add_field(name='Cones bet:', value=num, inline=True)
                    bet_embed.add_field(name='Potential gain:', value=potential_gain, inline=True)
                    await ctx.send(embed=bet_embed)
                elif percentile < medium_bracket:
                    users[f'{target}']['multiplier'] = higher
                    potential_gain = int(1 + (users[f'{target}']['multiplier'] * users[f'{target}']['bet']) - users[f'{target}']['bet'])
                    bet_embed = discord.Embed(
                        title = 'The Cones Have Been Bet',
                        color = discord.Color(0x001FFF)
                    )
                    bet_embed.set_author(name=nickname, icon_url=emoji)
                    bet_embed.add_field(name='Cones bet:', value=num, inline=True)
                    bet_embed.add_field(name='Potential gain:', value=potential_gain, inline=True)
                    await ctx.send(embed=bet_embed)
                elif percentile < high_bracket:
                    users[f'{target}']['multiplier'] = high
                    potential_gain = int(1 + (users[f'{target}']['multiplier'] * users[f'{target}']['bet']) - users[f'{target}']['bet'])
                    bet_embed = discord.Embed(
                        title = 'The Cones Have Been Bet',
                        color = discord.Color(0x001FFF)
                    )
                    bet_embed.set_author(name=nickname, icon_url=emoji)
                    bet_embed.add_field(name='Cones bet:', value=num, inline=True)
                    bet_embed.add_field(name='Potential gain:', value=potential_gain, inline=True)
                    await ctx.send(embed=bet_embed)
                elif percentile < higher_bracket:
                    users[f'{target}']['multiplier'] = medium
                    potential_gain = int(1 + (users[f'{target}']['multiplier'] * users[f'{target}']['bet']) - users[f'{target}']['bet'])
                    bet_embed = discord.Embed(
                        title = 'The Cones Have Been Bet',
                        color = discord.Color(0x001FFF)
                    )
                    bet_embed.set_author(name=nickname, icon_url=emoji)
                    bet_embed.add_field(name='Cones bet:', value=num, inline=True)
                    bet_embed.add_field(name='Potential gain:', value=potential_gain, inline=True)
                    await ctx.send(embed=bet_embed)
                else:
                    users[f'{target}']['multiplier'] = low
                    potential_gain = int(1 + (users[f'{target}']['multiplier'] * users[f'{target}']['bet']) - users[f'{target}']['bet'])
                    bet_embed = discord.Embed(
                        title = 'The Cones Have Been Bet',
                        color = discord.Color(0x001FFF)
                    )
                    bet_embed.set_author(name=nickname, icon_url=emoji)
                    bet_embed.add_field(name='Cones bet:', value=num, inline=True)
                    bet_embed.add_field(name='Potential gain:', value=potential_gain, inline=True)
                    await ctx.send(embed=bet_embed)
            else:
                bet_embed = discord.Embed(
                    title = 'You are too broke to make that bet.',
                    color = discord.Color(0xFF0000)
                )
                bet_embed.set_author(name=nickname, icon_url=emoji)
                await ctx.send(embed=bet_embed)
        else:
            bet_embed = discord.Embed(
                title = 'You already placed a bet.',
                color = discord.Color(0xFFB200)
            )
            bet_embed.set_author(name=nickname, icon_url=emoji)
            await ctx.send(embed=bet_embed)
    with open('users.json', 'w') as f:  #write the changes to the json
        json.dump(users, f)

@bot.command()
#shows bets
async def show_bets(ctx):
    with open('users.json', 'r') as f:
        users = json.load(f)
        df = pd.read_json('users.json') #creates a dataframe out of the json
        df = df.T
        df['names'] = df.index
        df = df.set_index('bet')
        df = df.drop(columns=['names', 'cones', 'team', 'admin', 'bid'])
    await ctx.send(df.drop(0).sort_values(by=['bet'])) #sends the dataframe sorted by bets

@bot.command(aliases=['gib', 'Gib'])
@commands.has_role('Cone of Dunshire')
#adds a cone to the target
async def add_cone(ctx, target, num=1):
    with open('users.json', 'r') as f:
        users = json.load(f)            #read the json
    if not f'{target}' in users:        #create a entry for the user if one doesn't already exist
        users[f'{target}'] = {}
        users[f'{target}']['cones'] = minimum_cones - 1
        users[f'{target}']['multiplier'] = high
        users[f'{target}']['bet'] = 0
        users[f'{target}']['bid'] = 0
        users[f'{target}']['team'] = 0
        users[f'{target}']['nickname'] = f'{target}'
        users[f'{target}']['admin'] = 0
        users[f'{target}']['points'] = 0
    df = pd.read_json('users.json') #creates a dataframe out of the json
    df = df.T
    df['names'] = df.index
    df.cones = df.cones.astype(int)
    df = df.drop(columns=['names', 'team'])
    users[f'{target}']['cones'] += num + (users[f'{target}']['bet'] * users[f'{target}']['multiplier'])      #modify the number of cones
    cones_given = num + (users[f'{target}']['bet'] * users[f'{target}']['multiplier']) - users[f'{target}']['bet']
    users[f'{target}']['bet'] = 0
    cones = users[f'{target}']['cones']
    nickname = users[f'{target}']['nickname']
    percentile = scipy.stats.percentileofscore(df.cones, cones)
    emoji = await cone_emojis(ctx, target=target)
    if percentile < low_bracket:
        users[f'{target}']['multiplier'] = highest
    elif percentile < medium_bracket:
        users[f'{target}']['multiplier'] = higher
    elif percentile < high_bracket:
        users[f'{target}']['multiplier'] = high
    elif percentile < higher_bracket:
        users[f'{target}']['multiplier'] = medium
    else:
        users[f'{target}']['multiplier'] = low
    with open('users.json', 'w') as f:      #write the changes to the json
        json.dump(users, f)
    gib_embed = discord.Embed(
        title = 'The Cones Have Been Gib',
        #description = '"Bring that one down!"',
        color = discord.Color(0x00FF23)
    )
    #gib_embed.set_footer(text='This is a footer.')
    #gib_embed.set_image(url='https://i.imgur.com/ePSB083.gif')
    #gib_embed.set_thumbnail(url='https://i.imgur.com/W6uCASf.png')
    gib_embed.set_author(name=nickname, icon_url=emoji)
    gib_embed.add_field(name='Cones given:', value=int(cones_given), inline=True)
    gib_embed.add_field(name='New number of cones:', value=int(cones), inline=True)
    #gib_embed.add_field(name='Field Name', value='Field Value', inline=True)

    await ctx.send(embed=gib_embed)

@bot.command()
@commands.has_role('Cone of Dunshire')
#creates a custom nickname for our users.json
async def give_nickname(ctx, target, *, nickname):
    with open('users.json', 'r') as f:
        users = json.load(f)            #read the json
    users[f'{target}']['nickname'] = nickname
    with open('users.json', 'w') as f:      #write the changes to the json
        json.dump(users, f)
    await ctx.send('{0}\'s nickname has been changed to {1}!'.format(f'{target}',users[f'{target}']['nickname']))

@bot.command()
#allows player to set their own nickname
async def change_nickname(ctx, *, nickname):
    with open('users.json', 'r') as f:
        users = json.load(f)            #read the json
    users['<@!{}>'.format(ctx.author.id)]['nickname'] = nickname
    with open('users.json', 'w') as f:      #write the changes to the json
        json.dump(users, f)
    await ctx.send('{0} has changed their nickname to {1}!'.format('<@!{}>'.format(ctx.author.id),users['<@!{}>'.format(ctx.author.id)]['nickname']))

@bot.command(aliases=['remove_cones'])
@commands.has_role('Cone of Dunshire')
#removes a cone from the target
async def remove_cone(ctx, target, num=1):
    words = ['The soggy',
             'The sad',
             'The destroyed',
             'The stinky',
             'The Darwin Awarded',
             'The disgusting',
             'The confused',
             'The super unrelatable',
             'The befuddled',
             'The ever-smelly',
             'The one who is crunchy,',
             'The one who is sweaty,',
             'The nice',
             'The repulsive',
             'The n00b',
             'The casual',
             'The one that everyone is secretly laughing at,',
             'The butthole',
             'The cranky',
             'The poo smeller',
             'The diddly dipper',
             'The extremely loud',
             'The scrawny',
             'The ever-ignored',
             'The stinky fart',
             'The pissy,',
             'The shit lord',
             'The one who exxagerates too much, ',
             'The sith',
             'The Thanos sympathizer']
    with open('users.json', 'r') as f:
        users = json.load(f)            #read the json
    if not f'{target}' in users:        #create a entry for the user if one doesn't already exist
        await ctx.send('User is not in our system. Error detected. Eliminate this threat at your earliest convenience.')
    else:
        users[f'{target}']['cones'] -= num  #modify the number of cones
        target_cones = int(users[target]['cones'])
    with open('users.json', 'w') as f:  #write the changes to the json
        json.dump(users, f)
    await ctx.send('{0} {1} only has {2} cones left to their name! ROFLMFAO'.format(random.choice(words) ,f'{target}',target_cones))

@bot.command(aliases=['give_cones'])
#give cones
async def give_cone(ctx, target, num=1):
    with open('users.json', 'r') as f:
        users = json.load(f)            #read the json
    if users['<@!{}>'.format(ctx.author.id)]['cones'] >= num:
        users[f'{target}']['cones'] += num      #add the number of cones to target
        await ctx.send('{0} now has {1} cones to their name!'.format(f'{target}',int(users[f'{target}']['cones'])))
        users['<@!{}>'.format(ctx.author.id)]['cones'] -= num  #subtract number of cones from author
        await ctx.send('{0} now has {1} cones to their name!'.format(f'<@!{ctx.author.id}>',int(users['<@!{}>'.format(ctx.author.id)]['cones'])))
    else:
        await ctx.send('{0} only has {1} cones to their name, that isn\'t enough for this transaction!'.format(f'<@!{ctx.author.id}>',users['<@!{}>'.format(ctx.author.id)]['cones']))
    with open('users.json', 'w') as f:  #write the changes to the json
        json.dump(users, f)

@bot.command()
#sets team name
async def team(ctx, *, team):
    with open('users.json', 'r') as f:
        users = json.load(f)            #read the json
    users['<@!{}>'.format(ctx.author.id)]['team'] = team
    await ctx.send('{0} is on team \"{1}\"'.format(f'<@!{ctx.author.id}>',users['<@!{}>'.format(ctx.author.id)]['team']))
    with open('users.json', 'w') as f:  #write the changes to the json
        json.dump(users, f)

@bot.command(aliases=['show_team'])
#shows teams
async def show_teams(ctx):
    with open('users.json', 'r') as f:
        users = json.load(f)
        df = pd.read_json('users.json') #creates a dataframe out of the json
        df = df.T
        df['names'] = df.index
        df = df.set_index('team')
        df = df.drop(columns=['names', 'cones', 'multiplier', 'bet', 'admin', 'bid'])
    await ctx.send(df.drop(0).sort_values(by=['team'])) #sends the dataframe sorted by cones

@bot.command(aliases=['reset'])
@commands.has_role('Cone of Dunshire')
#sets all teams to 0
async def reset_teams(ctx):
    with open('users.json', 'r') as f:
        users = json.load(f)            #read the json
    for user in users:
        users[user]['team'] = 0
    await ctx.send('All team names have been reset. Don\'t forget to set a new team!')
    with open('users.json', 'w') as f:  #write the changes to the json
        json.dump(users, f)

@bot.command()
@commands.has_role('Cone of Dunshire')
#sets all admin to 0
async def admin(ctx):
    with open('users.json', 'r') as f:
        users = json.load(f)            #read the json
    for user in users:
        users[user]['admin'] = 0
    await ctx.send('Set')
    with open('users.json', 'w') as f:  #write the changes to the json
        json.dump(users, f)

@bot.command(aliases=['gib_team'])
@commands.has_role('Cone of Dunshire')
#adds a cone to the target team
async def team_cone(ctx, *, temp):
    with open('users.json', 'r') as f:
        users = json.load(f)            #read the json
    temp = temp.lower()
    for user in users:
        if users[user]['team'] != 0:
            users[user]['team'] = str(users[user]['team']).lower() #changes the team name to be a string and lower case
            if users[user]['team'] == temp:
                users[user]['cones'] += 1 + (users[user]['bet'] * users[user]['multiplier'])
                users[user]['bet'] = 0
        else:
            pass
    with open('users.json', 'w') as f:  #write the changes to the json
        json.dump(users, f)
    await ctx.send('Team {0} has won a cone. Every member of the team gains one (plus any bets)!'.format(temp))

@bot.command()
@commands.has_role('Cone of Dunshire')
#awards a winning team and collects lost bets
async def winner_winner(ctx, x):
    await team_cone(ctx, temp=x)
    await bet_collect(ctx)

@bot.command(aliases=['show_cone'])
#shows how many cones the target has, if no target then self
async def show_cones(ctx,target=None):
    target = target
    with open('users.json', 'r') as f:
        users = json.load(f)
    if target == None:
        target = '<@!{}>'.format(ctx.author.id)
    if f'{target}' in users:
        await ctx.send('{0} has {1} cones, and a {2} multiplier.'.format(f'{target}', int(users[f'{target}']['cones']), users[f'{target}']['multiplier']))
    else:
         await ctx.send('This user has no cones yet.')

# @bot.command(aliases=['leaderboard'])
# #shows the leaderboard
# async def show_leader(ctx):
#     with open('users.json', 'r') as f:
#         users = json.load(f)
#         df = pd.read_json('users.json') #creates a dataframe out of the json
#         df = df.T
#         df['names'] = df.index
#         df.cones = df.cones.astype(int)
#         df = df.set_index('cones')
#         df = df.drop(columns=['names', 'team', 'bet', 'multiplier', 'admin', 'bid', 'points'])
#     await ctx.send(df.sort_values(by=['cones'], ascending=False)) #sends the dataframe sorted by cones

@bot.command(aliases=['top', 'leaderboard'])
#shows the leaderboard
async def show_top(ctx):
    with open('users.json', 'r') as f:
        users = json.load(f)
        df = pd.read_json('users.json') #creates a dataframe out of the json
        df = df.T
        df['names'] = df.index
        df.cones = df.cones.astype(int)
        df = df.set_index('cones')
        df = df.drop(columns=['nickname', 'team', 'bet', 'multiplier', 'admin', 'bid', 'points'])
        df = df.sort_values(by=['cones'], ascending=False)
        df.columns = ['']
        df.index.rename('', inplace=True)
        top_embed = discord.Embed(
            title = 'Lord of The Cones',
            description = '"Bring that one down!"',
            color = discord.Color(0xFFD1DC)
        )

        #top_embed.set_footer(text='This is a footer.')
        top_embed.set_image(url='https://i.imgur.com/ePSB083.gif')
        top_embed.set_thumbnail(url='https://i.imgur.com/W6uCASf.png')
        #top_embed.set_author(name='Author Name', icon_url='https://imgur.com/a/x2uYN8i')
        top_embed.add_field(name='The Best', value=df.head(1), inline=True)
        top_embed.add_field(name='The Rest', value=df[1:6], inline=True)
        #top_embed.add_field(name='Field Name', value='Field Value', inline=True)

        await ctx.send(embed=top_embed)

@bot.command(aliases=['mults'])
#shows the leaderboard
async def show_multiplier(ctx):
    with open('users.json', 'r') as f:
        users = json.load(f)
        df = pd.read_json('users.json') #creates a dataframe out of the json
        df = df.T
        df['names'] = df.index
        #df.cones = df.cones.astype(int)
        df = df.set_index('multiplier')
        df = df.drop(columns=['names', 'team', 'bet', 'cones', 'admin', 'bid', 'points'])
    await ctx.send(df.sort_values(by=['multiplier'])) #sends the dataframe sorted by cones

@bot.command(aliases=['stats'])
#shows the players stats
async def show_stats(ctx):
    with open('users.json', 'r') as f:
        users = json.load(f)
        df = pd.read_json('users.json') #creates a dataframe out of the json
        df = df.T
        df['names'] = df.index
        df.cones = df.cones.astype(int)
        df = df.drop(columns=['names', 'team'])
        target = '<@!{}>'.format(ctx.author.id)
        nickname = users[f'{target}']['nickname']
        cones = int(users[f'{target}']['cones'])
        multiplier = users[f'{target}']['multiplier']
        emoji = await cone_emojis(ctx, target=target)
        difference_from_top = int(df.cones.max() - users[f'{target}']['cones'])
        rank = users[f'{target}']['points']
        percentile = round(scipy.stats.percentileofscore(df.cones, cones), 2)
        stats_embed = discord.Embed(
            title = 'Personal Cone Stats',
            #description = '"Bring that one down!"',
            color = discord.Color(0x0036FF)
        )

        #top_embed.set_footer(text='This is a footer.')
        #stats_embed.set_image(url='https://i.imgur.com/ePSB083.gif')
        stats_embed.set_thumbnail(url=emoji)
        stats_embed.set_author(name=nickname, icon_url=emoji)
        stats_embed.add_field(name='Number of cones:', value=cones, inline=True)
        stats_embed.add_field(name='Percentile:', value=percentile, inline=True)
        stats_embed.add_field(name='Distance from The Best:', value=difference_from_top, inline=True)
        stats_embed.add_field(name='Betting multiplier:', value=multiplier, inline=True)
        stats_embed.add_field(name='Weeks in the top 3:', value=rank, inline=True)
        #top_embed.add_field(name='Field Name', value='Field Value', inline=True)

        await ctx.send(embed=stats_embed)

@bot.command(aliases=['commands'])
#shows a list of available bot commands
async def bot_commands(ctx):
    df_t = pd.DataFrame()
    df_t['commands'] = ['.8ball',
                       '.card',
                       '.insult',
                       '.compliment',
                       '.ping',
                       '.show_cones',
                       '.leaderboard',
                       '.change_nickname',
                       '.give_cone',
                       '.comfort',
                       '.unsettle',
                       '.team',
                       '.show_teams',
                       '.stats',
                       '.bet',
                       '.show_bets',
                       '.top',
                       '.bid',
                       '.show_bids',
                       '.rules']
    df_t['function'] = ['answers a yes or no question',
                       'pulls a random card',
                       'da fuq you think it does?',
                       'compliments your target',
                       'will pong the latency',
                       'shows your or your targets cone count',
                       'shows the leaderboard',
                       'changes your nickname',
                       'gives a cone to your target',
                       'comforts the target',
                       'unsettles the target',
                       'sets your team name',
                       'shows all currently set teams',
                       'shows general stats for cones',
                       'allows you to place a bet of cones',
                       'shows all players who have placed bets',
                       'shows the people with the largest coners',
                       'places a bid to become The Dictator',
                       'shows a list of everyone who has placed a bid',
                       'lists current rules for the channel and its games']
    df_t = df_t.set_index('commands')
    await ctx.send(df_t)

@bot.command()
#shows a list of rules for various activities
async def rules(ctx, value='basic'):
    if value == 'basic':
        await ctx.send('Welcome to the rules. To access rules on specific topics for the channel you may type:\n".rules betting"\n".rules dictator"')
    elif value == 'betting':
        await ctx.send('Greetings {}. Below you will find the rules for betting your cones away.\nYou may bet any number of cones up to the number that you own (type .stats to see) while playing in a game with other members of the channel. Type .bet [# of cones you want to bet]. Example: ".bet 5". Alternatively you can bet everything you have by typing ".bet max"; betting max will reward you with an extra multiplier to your winnings.\nThe currently accepted games to bet on are: Apex Legends, Heroes Of The Storm.\nIf you do not want to play but wish to bet on someone else\'s game you may. However, you may only bet on them to win.'.format(ctx.author.mention))
    elif value == 'dictator':
        await ctx.send('Hello future Dictator {}. Below you will find the path to domination.\nAn anonymous bidding war must take place. Whoever bids the highest amount will become Dictator.\nTo place a bid you must DM me (The Oracle of Cones) the following ".bid [insert number to bid here]". Example: ".bid 5". If you fail to do this in a DM with me then everyone will see your bid, making you easy to defeat and causing you to look extremely foolish.\nIf you place a bid and are defeated by someone else, your cones will be returned to you. If you bid the highest number of cones you forfeit those cones in the pursuit of Ultimate Power.\nIn the event of a tie, I (The Oracle of Cones) will randomly select a winner from among the highest bidders.\nAt any point someone may offer to buy the dictatorship from the current Dictator. If the current Dictator accepts the buyout then the title is transferred.\nUpon recieving the title of Dictator, you must select a General to serve at your side.\nAt any point either the Dictator or General can command anyone of a lower rank to drink. The General cannot tell The Dictator to drink, but either of them can impose those drinking whims upon all plebians.\nShould The General wish to have a coup to overthrow The Dictator, they may. The requirements for this are simple- with 75% of the popular vote, The General becomes the new Dictator. At this time the new Dictator must appoint a new General and the old Dictator becomes a plebian.\nIn case it wasn\'t clear: if you are not The Dictator or The General, you are a plebian. You are a commoner. You are unremarkable, insignificant, and smelly. As such, The Dictator and General, in their insurmountable wisdom and infinite power, can command you to drink at any time.'.format(ctx.author.mention))
    else:
        await ctx.send('There are no rules for that specific subject yet. You may prostrate yourself at the feet of one of the Cone of Dunshire admins to plea with them that this situation be rememied at once. The risk of beheading is.... small.')

@bot.command()
#gets the latency of the bot
async def ping(ctx):
    await ctx.send(f'Pong! {round(bot.latency * 1000)}ms')

@bot.command()
@commands.has_role('Cinder Cone')
#insults the target
async def insult(ctx, *, target):
    insults = ["the trouble ain't there is too many fools, but that the lightning ain't distributed right.",
              "his mother should have thrown him away and kept the stork.",
              "I never forget a face, but in your case, I'll make an exception.",
              "some cause happiness wherever they go, others whenever they go.",
              "if your brains were dynamite, there wouldn't be enough to blow your hat off.",
              "only two things are infinite-- the universe and human stupidity, and I'm not so sure about the former.",
              "Greg fucked your dad.",
              "we were trying to get pregnant, but I forgot one of us had to have a penis.",
              "is a glob of snot.",
              "you are proof that God has a sense of humor.",
              "if I throw a stick, will you leave?",
              "in the land of the witless, you would be king.",
              "fuck is cool, you ain't.",
              "I'm gunna uninstall hots.",
              "you are the reason God created the middle finger.",
              "your inferiority complex is fully justified.",
              "you have delusions of adequacy.",
              "I like the way you try.",
              "it is impossible to underestimate you.",
              "I'm jealous of all the people who haven't met you.",
              "your goblin rocket is stick'n out.",
              "congradulations you played yourself!",
              "I've had a lot to drink, and you still don't look good.",
              "you're dark and handsome. When it's dark, you're handsome.",
              "your beauty would be enhanced by a burka.",
              "is your name Victoria? Cause you’re playing like shit",
              "make like a tree and fuck off.",
              "it's okay to be ugly, but aren't you over doing it?",
              "the last time you were at the beach, Greenpeace tried to drag you back into the water.",
              "Yo' mama.",
              "whatever kind of look you were going for, you missed.",
              "kudos on that camel toe.",
              "you're not yourself today. I noticed the improvement immediately!",
              "I'm guessing you haven't been diagnosed yet?",
              "kick me daddy!"]
    await ctx.send(f'{target}, {random.choice(insults)}')

@bot.command()
@commands.has_role('Sugar Cone')
#comforts the target
async def comfort(ctx, *, target):
    comforts = ["Don\'t worry {}, everything will be alright.",
                "{}, it's ok bby.",
                "The sun is shining and so are you, {}!",
                "You are a strong indepent woman, {}.",
                "Wrap your arms around yourself and pretend I'm giving you a big hug, {}.",
                "In tough times there will always be people who help. Look for the helpers, {}.",
                "{}! You got this!",
                "Ah I see you're wearing your ass-kicking outfit, {}, a good choice.",
                "The night is always darkest before the dawn, {}.",
                "Sometimes we just have to remember, 'All we have to decide is what to do with the time that is given to us.', {}.",
                "Have you given yourself a high-five today {}? Because you deserve one.",
                "Sometimes you've just gotta eat a snack, take a nap, and know that things will be better tomorrow, {}.",
                "Hey {}, drink some wine.",
                "{}, the world may be dark and scary, but having you as a friend helps.",
                "{}, there there.",
                "Shit sucks, but everyone knows that {} is kicking ass!",
                "{}, take a moment to focus on the small happy things in the world: there are constellations of stars that we gazed at and gave them names, there are old books full of stories and nice smells, there is hot chocolate with marshmellows, someone is falling in love for the first time right now, there will be mornings where you wake up feeling safe and snuggled in your warm bed and realize that you've become the person you wanted to be your whole life, after it rains the scent of the pavement and the sense of the world is that it's all new and anything can happen, there will be moments when you walk into a room and everyone will light up in cheer because your presence brings them so much joy, bread and cheese both exist, you aren't even close to finished kicking ass, sometimes your favorite song will come on when you're driving in your car just when you need it most and maybe thats coincidence and maybe that's kismet but either way it's a nice moment. ",
                "Is {} Deathwing? Because they're unstoppable!"]
    await ctx.send(random.choice(comforts).format(f'{target}'))

@bot.command()
@commands.has_role('Sugar Cone')
#unsettles the target
async def unsettle(ctx, *, target):
    unsettles = ["{}, everyone that you love will die eventually.",
                "{}, you better watch out, you better watch out, you beTTER WATCH OUT-",
                "{}, realistically, everything will not be okay.",
                "{}, you will outlive your pets.",
                "Hey {}, did you know Jeff Bezos has over 100 billion dollars? He could fix world problems and chooses not to.",
                "No one would notice if you stopped posting on social media, {}.",
                "But are you SURE you locked the door, {}?",
                "It doesn’t matter how safely you drive, {}. Another driver can always hit you.",
                "Yes, {}. Everyone IS talking about you.",
                "Even nice hotels get bedbugs, {}. And they WILL follow you home.",
                "{}, you might be overwatering your plants.",
                "Hey {}, that bad dream you had was actually a premonition.",
                "Oh, {}. It’s not a matter of ‘if,’ but ‘when.’",
                "Statistically, {}, you are insignificant.",
                "When was the last time you looked at your reflection? Really looked at it? How well do you know your own face, {}?",
                "{}, every face in your dreams and your nightmares comes from faces you’ve seen in real life. Have you thought of how your face appears in other people’s dreams?",
                "At some point in the relatively near future, {} and everyone they have ever known will no longer exist.",
                "It is possible that giant squid exist and we just haven’t found them yet. When was the last time you went swimming in the ocean, {}?",
                "Some estimates are that the human body, by mass, is 50% bacteria and 50% of your own cells. How sure are you that your thoughts are your own, {}?",
                "{}, you only ever see your reflection. You never get to know what you truly look like.",
                "{}, do you know how many bones are in your body? In your hand? Have you felt them recently? Are you sure those are all bones?",
                "If there is something that lives under {}'s bed, it only comes out when they’re sleeping. It’s not necessarily malicious, but that doesn’t mean it’s friendly either.",
                "{} cannot position their tongue in their mouth in such a way that they can’t feel it.",
                "{}, because you are always wearing clothes, your laundry will never be completely done.",
                "You smell different when you're awake, {}.",
                "I know what {} did. We all know what {} did.",
                "Don't look behind you {}."]
    await ctx.send(random.choice(unsettles).format(f'{target}'))

@bot.command()
@commands.has_role('Cinder Cone')
#compliments the target
async def compliment(ctx, *, target):
    compliments = ["I bet you make babies smile.",
                    "you have the best laugh.",
                    "you light up the room.",
                    "you have a great sense of humor.",
                    "if cartoon bluebirds were real, a couple of 'em would be sitting on your shoulders singing right now.",
                    "you're like sunshine on a rainy day.",
                    "you bring out the best in other people.",
                    "I bet you sweat glitter.",
                    "colors seem brighter when you're around.",
                    "you're more fun than a ball pit filled with candy.",
                    "jokes are funnier when you tell them.",
                    "you always know how to find that silver lining.",
                    "you're a candle in the darkness.",
                    "being around you is like a happy little vacation.",
                    "you're more fun than bubble wrap.",
                    "you're like a breath of fresh air.",
                    "you're someone's reason to smile.",
                    "how do you keep being so funny and making everyone laugh?",]
    await ctx.send(f'{target}, {random.choice(compliments)}')

@bot.command(aliases=['8ball'])
#gives an 8ball prediction of a question
async def _8ball(ctx, *, question):
    responses = ["As I see it, yes.",
                "Ask again later.",
                "Better not tell you now.",
                "Cannot predict now.",
                "Concentrate and ask again.",
                "Don’t count on it.",
                "It is certain.",
                "It is decidedly so.",
                "Most likely.",
                "My reply is no.",
                "My sources say no.",
                "Outlook not so good.",
                "Outlook good.",
                "Reply hazy, try again.",
                "Signs point to yes.",
                "Very doubtful.",
                "Without a doubt.",
                "Yes.",
                "Yes – definitely.",
                "You may rely on it."]
    await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')

@bot.command(aliases=['cards'])
#generates a card from a standard deck
async def card(ctx, num=1):
    with open('users.json', 'r') as f:
        users = json.load(f)            #read the json
    cards = ["Ace of Spades", "Ace of Diamonds", "Ace of Clubs", "Ace of Hearts",
            "King of Spades", "King of Diamonds", "King of Clubs", "King of Hearts",
            "Queen of Spades", "Queen of Diamonds", "Queen of Clubs", "Queen of Hearts",
            "Jack of Spades", "Jack of Diamonds", "Jack of Clubs", "Jack of Hearts",
            "Ten of Spades", "Ten of Diamonds", "Ten of Clubs", "Ten of Hearts",
            "Nine of Spades", "Nine of Diamonds", "Nine of Clubs", "Nine of Hearts",
            "Eight of Spades", "Eight of Diamonds", "Eight of Clubs", "Eight of Hearts",
            "Seven of Spades", "Seven of Diamonds", "Seven of Clubs", "Seven of Hearts",
            "Six of Spades", "Six of Diamonds", "Six of Clubs", "Six of Hearts",
            "Five of Spades", "Five of Diamonds", "Five of Clubs", "Five of Hearts",
            "Four of Spades", "Four of Diamonds", "Four of Clubs", "Four of Hearts",
            "Three of Spades", "Three of Diamonds", "Three of Clubs", "Three of Hearts",
            "Two of Spades", "Two of Diamonds", "Two of Clubs", "Two of Hearts",
            "Six of Spades", "Six of Diamonds", "Six of Clubs", "Six of Hearts"]
    c = random.choices(cards, k=num)
    await ctx.send('{} drew a {}.'.format(users['<@!{}>'.format(ctx.author.id)]['nickname'], str(c).strip('[]')))

bot.run(TOKEN)
