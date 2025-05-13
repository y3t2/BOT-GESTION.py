import discord
from discord.ext import commands
import random
import asyncio
import aiohttp
import json
from datetime import datetime

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def roll(self, ctx, dice: str = "1d6"):
        """Lance un ou plusieurs dés (format: NdM)"""
        try:
            rolls, limit = map(int, dice.split('d'))
            if rolls > 25:
                await ctx.send("Maximum 25 dés à la fois!")
                return
            results = [random.randint(1, limit) for _ in range(rolls)]
            await ctx.send(f"🎲 Résultats: {', '.join(map(str, results))}\nTotal: {sum(results)}")
        except:
            await ctx.send("Format invalide! Utilisez NdM (ex: 2d6)")

    @commands.command()
    async def choose(self, ctx, *, choices: str):
        """Choisit aléatoirement parmi plusieurs options"""
        options = [x.strip() for x in choices.split(',')]
        if len(options) < 2:
            await ctx.send("Donnez au moins 2 options séparées par des virgules!")
            return
        await ctx.send(f"🎯 Je choisis: **{random.choice(options)}**")

    @commands.command()
    async def poll(self, ctx, question: str, *options):
        """Crée un sondage avec des réactions"""
        if len(options) > 10:
            await ctx.send("Maximum 10 options!")
            return
        
        emojis = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']
        description = []
        for idx, option in enumerate(options):
            description.append(f"{emojis[idx]} {option}")
        
        embed = discord.Embed(
            title=question,
            description='\n'.join(description),
            color=discord.Color.blue()
        )
        embed.set_footer(text=f"Sondage créé par {ctx.author.name}")
        
        poll_msg = await ctx.send(embed=embed)
        for idx in range(len(options)):
            await poll_msg.add_reaction(emojis[idx])

    @commands.command(name="8ball")
    async def eight_ball(self, ctx, *, question: str):
        """Pose une question au bot"""
        responses = [
            "C'est certain!", "C'est décidément ainsi!", "Sans aucun doute!",
            "Oui, définitivement!", "Vous pouvez compter dessus!", "Comme je le vois, oui!",
            "Probablement!", "Les perspectives sont bonnes!", "Oui!",
            "Les signes indiquent que oui!", "Réponse floue, réessayez!", "Redemandez plus tard!",
            "Mieux vaut ne pas vous le dire maintenant!", "Impossible de prédire maintenant!",
            "Concentrez-vous et redemandez!", "Ne comptez pas dessus!", "Ma réponse est non!",
            "Mes sources disent non!", "Les perspectives ne sont pas bonnes!", "Très douteux!"
        ]
        embed = discord.Embed(
            title="🎱 8ball",
            description=f"**Question:** {question}\n**Réponse:** {random.choice(responses)}",
            color=discord.Color.blue()
        )
        await ctx.send(embed=embed)

    @commands.command()
    async def reverse(self, ctx, *, text: str):
        """Inverse le texte donné"""
        await ctx.send(f"↩️ {text[::-1]}")

    @commands.command()
    async def ascii(self, ctx, *, text: str):
        """Convertit le texte en art ASCII"""
        if len(text) > 20:
            await ctx.send("Maximum 20 caractères!")
            return
        
        result = ""
        for char in text.upper():
            if char.isalpha():
                result += f"```\n{char}```"
            else:
                result += char
        await ctx.send(result)

    @commands.command()
    async def countdown(self, ctx, seconds: int):
        """Démarre un compte à rebours"""
        if seconds > 60:
            await ctx.send("Maximum 60 secondes!")
            return
        
        message = await ctx.send(f"⏰ Compte à rebours: {seconds}")
        while seconds > 0:
            await asyncio.sleep(1)
            seconds -= 1
            await message.edit(content=f"⏰ Compte à rebours: {seconds}")
        await message.edit(content="⏰ Temps écoulé!")

    @commands.command()
    async def randomcolor(self, ctx):
        """Génère une couleur aléatoire"""
        color = discord.Color.random()
        embed = discord.Embed(
            title="🎨 Couleur aléatoire",
            color=color
        )
        embed.add_field(name="Hex", value=color.to_rgb())
        await ctx.send(embed=embed)

    @commands.command()
    async def flip(self, ctx):
        """Lance une pièce"""
        result = random.choice(["Pile", "Face"])
        await ctx.send(f"🪙 {result}!")

    @commands.command()
    async def rps(self, ctx, choice: str):
        """Pierre, Papier, Ciseaux"""
        choice = choice.lower()
        if choice not in ["pierre", "papier", "ciseaux"]:
            await ctx.send("Choisissez entre pierre, papier ou ciseaux!")
            return
        
        bot_choice = random.choice(["pierre", "papier", "ciseaux"])
        
        if choice == bot_choice:
            result = "Égalité!"
        elif (choice == "pierre" and bot_choice == "ciseaux") or \
             (choice == "papier" and bot_choice == "pierre") or \
             (choice == "ciseaux" and bot_choice == "papier"):
            result = "Vous avez gagné!"
        else:
            result = "J'ai gagné!"
        
        embed = discord.Embed(
            title="✂️ Pierre, Papier, Ciseaux",
            description=f"Vous: {choice}\nMoi: {bot_choice}\n\n{result}",
            color=discord.Color.blue()
        )
        await ctx.send(embed=embed)

    @commands.command()
    async def quote(self, ctx):
        """Affiche une citation aléatoire"""
        async with aiohttp.ClientSession() as session:
            async with session.get('https://api.quotable.io/random') as response:
                if response.status == 200:
                    data = await response.json()
                    embed = discord.Embed(
                        title="💭 Citation",
                        description=f"*{data['content']}*",
                        color=discord.Color.blue()
                    )
                    embed.set_footer(text=f"- {data['author']}")
                    await ctx.send(embed=embed)
                else:
                    await ctx.send("Impossible de récupérer une citation!")

async def setup(bot):
    await bot.add_cog(Fun(bot)) 