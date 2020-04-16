import discord
from discord.ext import commands
import json
import os
import pandas as pd
import random

TOKEN = ''
bot = commands.Bot(command_prefix = '.')
os.chdir(r'D:\Bot\github')


#this block is temporary testing gregsan
# df = pd.read_json('users.json') #creates a dataframe out of the json
# df = df.T
# df['names'] = df.index
# df = df.set_index('cones')
# df['nicknames'] = df['names']
# df['cones'] = df.index
# df.index = range(len(df.names))
# df = df[['cones', 'names', 'nicknames']]
# print(df)
# df.to_json(r'D:\Bot\github\users_test.json')


@bot.event
async def on_ready():
    print('Bot is ready.')



@bot.command(aliases=['gib'])
@commands.has_role('Cone of Dunshire')
#adds a cone to the target
async def add_cone(ctx, target, num=1):
    words = ['The magnanimous',
             'The awesome',
             'The incredible',
             'The fortuitous',
             'The flabbergasted',
             'The GOAT',
             'The rebelious',
             'The emperor',
             'The genius',
             'The conqueror',
             'The one who is better than all things,',
             'The one who excedes expectations,',
             'The shiny',
             'The enthralling',
             'The bewitching',
             'The stunning',
             'The elegant',
             'The popular',
             'The intelligent',
             'The capable',
             'The confident',
             'The extremely tall',
             'The super well endowed',
             'The highly sought after',
             'The charming',
             'The one who lights up a room,',
             'The hyper-1337',
             'The one made of carbon and some other stuff too',
             'The jedi']
    with open('users.json', 'r') as f:
        users = json.load(f)            #read the json
    if not f'{target}' in users:        #create a entry for the user if one doesn't already exist
        users[f'{target}'] = {}
        users[f'{target}']['cones'] = 0
    users[f'{target}']['cones'] += num      #modify the number of cones
    with open('users.json', 'w') as f:      #write the changes to the json
        json.dump(users, f)
    await ctx.send('{0} {1} has {2} cones to their name!'.format(random.choice(words) ,f'{target}',users[f'{target}']['cones']))

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
#@commands.has_role('Cone of Dunshire')
async def change_nickname(ctx, *, nickname):
    with open('users.json', 'r') as f:
        users = json.load(f)            #read the json
    users['<@!{}>'.format(ctx.author.id)]['nickname'] = nickname
    with open('users.json', 'w') as f:      #write the changes to the json
        json.dump(users, f)
    await ctx.send('{0} has changed their nickname to {1}!'.format('<@!{}>'.format(ctx.author.id),users['<@!{}>'.format(ctx.author.id)]['nickname']))

@bot.command()
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
        users[f'{target}'] = {}
        users[f'{target}']['cones'] = 0
    users[f'{target}']['cones'] -= num  #modify the number of cones
    with open('users.json', 'w') as f:  #write the changes to the json
        json.dump(users, f)
    await ctx.send('{0} {1} only has {2} cones left to their name! ROFLMFAO'.format(random.choice(words) ,f'{target}',users[f'{target}']['cones']))

@bot.command()
#give cones
async def give_cone(ctx, target, num=1):
    with open('users.json', 'r') as f:
        users = json.load(f)            #read the json
    if users['<@!{}>'.format(ctx.author.id)]['cones'] >= num:
        users[f'{target}']['cones'] += num      #add the number of cones to target
        await ctx.send('{0} now has {1} cones to their name!'.format(f'{target}',users[f'{target}']['cones']))
        users['<@!{}>'.format(ctx.author.id)]['cones'] -= num  #subtract number of cones from author
        await ctx.send('{0} now has {1} cones to their name!'.format(f'<@!{ctx.author.id}>',users['<@!{}>'.format(ctx.author.id)]['cones']))
    else:
        await ctx.send('{0} only has {1} cones to their name, that isn\'t enough for this transaction!'.format(f'<@!{ctx.author.id}>',users['<@!{}>'.format(ctx.author.id)]['cones']))
    with open('users.json', 'w') as f:  #write the changes to the json
        json.dump(users, f)

@bot.command()
#shows how many cones the target has, if no target then self
async def show_cones(ctx,target=None):
    target = target
    with open('users.json', 'r') as f:
        users = json.load(f)
    if target == None:
        target = '<@!{}>'.format(ctx.author.id)
    if f'{target}' in users:
        await ctx.send('{0} has {1} cones.'.format(f'{target}', users[f'{target}']['cones']))
    else:
         await ctx.send('This user has no cones yet.')

@bot.command()
#shows the leaderboard
async def show_leader(ctx):
    with open('users.json', 'r') as f:
        users = json.load(f)
        df = pd.read_json('users.json') #creates a dataframe out of the json
        df = df.T
        df['names'] = df.index
        df.cones = df.cones.astype(int)
        df = df.set_index('cones')
        df = df.drop(columns='names')
    await ctx.send(df.sort_values(by=['cones'], ascending=False)) #sends the dataframe sorted by cones

@bot.command()
#shows a list of available bot commands
async def commands(ctx):
    df_t = pd.DataFrame()
    df_t['commands'] = ['.8ball',
                       '.card',
                       '.insult',
                       '.compliment',
                       '.ping',
                       '.show_cones',
                       '.show_leader',
                       '.change_nickname',
                       '.give_cone',
                       '.comfort',
                       '.unsettle']
    df_t['function'] = ['answers a yes or no question',
                       'pulls a random card',
                       'insults your target',
                       'compliments your target',
                       'will pong the latency',
                       'shows your or your targets cone count',
                       'shows the leaderboard',
                       'changes your nickname',
                       'gives a cone to your target',
                       'comforts the target',
                       'da fuq you think it does']
    df_t = df_t.set_index('commands')
    await ctx.send(df_t)

@bot.command()
#gets the latency of the bot
async def ping(ctx):
    await ctx.send(f'Pong! {round(bot.latency * 1000)}ms')

@bot.command()
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
                "{}, take a moment to focus on the small happy things in the world: there are constalations of stars that we gazed at and gave them names, there are old books full of stories and nice smells, there is hot chocolate with marshmellows, someone is falling in love for the first time right now, there will be mornings where you wake up feeling safe and snuggled in your warm bed and realize that you've become the person you wanted to be your whole life, after it rains the scent of the pavemnet and the sense of the world is that it's all new and anything can happen, there will be moments when you walk into a room and everyone will light up in cheer because your presence brings them so much joy, bread and cheese both exist, {} isn't even close to finished kicking ass, sometimes your favorite song will come on when you're driving in your car just when you need it most and maybe thats coincidence and maybe that's kismet but either way it's a nice moment. ",
                "Is {} Deathwing? Because they're unstoppable!"]
    await ctx.send(random.choice(comforts).format(f'{target}'))

@bot.command()
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

@bot.command()
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
