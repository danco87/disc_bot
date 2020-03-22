import discord
from discord.ext import commands
import random
import json
import os

TOKEN = 'NjkwNzkyNjc3ODA1MTI5NzQ4.Xneeog.p0qV6iI1Fta_q1UUgUp2IHPKCeU'
bot = commands.Bot(command_prefix = '.')


@bot.event
async def on_ready():
    print('Bot is ready.')


@bot.event
async def on_member_remove(member):
    print(f'(member) has left the server.')

@bot.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(bot.latency * 1000)}ms')

@bot.command()
async def insult(ctx, *, target):
    insults = ["the trouble ain't there is too many fools, but that the lightning ain't distributed right.",
              "his mother should have thrown him away and kept the stork.",
              "I never forget a face, but in your case, I'll make an exception.",
              "some cause happiness wherever they go, others whenever they go.",
              "if your brains were dynamite, there wouldn't be enough to blow your hat off.",
              "only two things are infinite-- the universe and human stupidity, and I'm not so sure about the former.",
              "Greg fucked your dad.",
              "we were trying to get pregnant, but I forgot one of us had to have a penis.",
              "my opponent is a glob of snot.",
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


bot.run(TOKEN)
