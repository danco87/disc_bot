import discord
from discord.ext import commands

bot = commands.Bot(command_prefix = '.')

@bot.event
async def on_ready():
    print('Bot is ready.')

@bot.event
async def on_member_join(member):
    print(f'(member) has joined the server.')

@bot.event
async def on_member_remove(member):
    print(f'(member) has left the server.')

bot.run('NjkwNzkyNjc3ODA1MTI5NzQ4.XnWlLw.QQIgBhLwZ5QnB_Tz8WLxdZyYSBc')
