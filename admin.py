import discord
from discord.ext import commands
import random

bot = commands.Bot(command_prefix = '!')



@bot.event
async def on_ready():
    print('Bot is ready.')

@bot.event
async def on_member_join(member):
    print(f'(member) has joined the server.')

@bot.event
async def on_member_remove(member):
    print(f'(member) has left the server.')



bot.run('NjkxMDQzMzg0MzgyNDU1ODA5.XnaOrw.LCV7jNZWabjZ9Gw4HOFCt6HMQ3g')
