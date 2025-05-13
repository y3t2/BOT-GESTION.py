import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True  
intents.guilds = True   
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} est connecté à Discord!')
    await bot.load_extension('commands.moderation')
    await bot.load_extension('commands.fun')
    await bot.load_extension('commands.security')
    await bot.load_extension('commands.embed')
    await bot.load_extension('commands.management')

@bot.command(name='hello')
async def hello(ctx):
    """Répond avec un message de bienvenue"""
    await ctx.send(f'Bonjour {ctx.author.name}!')

@bot.command(name='ping')
async def ping(ctx):
    """Vérifie la latence du bot"""
    latency = round(bot.latency * 1000)
    await ctx.send(f'Pong! Latence: {latency}ms')

@bot.command(name='info')
async def info(ctx):
    """Affiche des informations sur le serveur"""
    server = ctx.guild
    await ctx.send(f'''
**Informations du serveur:**
Nom: {server.name}
Nombre de membres: {server.member_count}
Créé le: {server.created_at.strftime('%d/%m/%Y')}
''')

bot.run(os.getenv('BOT_TOKEN')) 