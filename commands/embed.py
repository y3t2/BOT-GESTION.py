import discord
from discord.ext import commands
import json
import os

class Embed(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.help_embeds = {}

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def embed(self, ctx, title: str, *, description: str):
        """Crée un embed simple avec un titre et une description"""
        embed = discord.Embed(
            title=title,
            description=description,
            color=discord.Color.blue()
        )
        embed.set_footer(text=f"Demandé par {ctx.author.name}")
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def embedcolor(self, ctx, color: str, title: str, *, description: str):
        """Crée un embed avec une couleur personnalisée"""
        color_map = {
            "rouge": discord.Color.red(),
            "bleu": discord.Color.blue(),
            "vert": discord.Color.green(),
            "jaune": discord.Color.gold(),
            "orange": discord.Color.orange(),
            "violet": discord.Color.purple(),
            "rose": discord.Color.magenta(),
            "gris": discord.Color.greyple()
        }
        
        color = color.lower()
        if color not in color_map:
            await ctx.send("Couleur invalide! Couleurs disponibles: " + ", ".join(color_map.keys()))
            return
            
        embed = discord.Embed(
            title=title,
            description=description,
            color=color_map[color]
        )
        embed.set_footer(text=f"Demandé par {ctx.author.name}")
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def embedimage(self, ctx, title: str, image_url: str, *, description: str = None):
        """Crée un embed avec une image"""
        embed = discord.Embed(
            title=title,
            description=description,
            color=discord.Color.blue()
        )
        embed.set_image(url=image_url)
        embed.set_footer(text=f"Demandé par {ctx.author.name}")
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def embedthumbnail(self, ctx, title: str, thumbnail_url: str, *, description: str = None):
        """Crée un embed avec une miniature"""
        embed = discord.Embed(
            title=title,
            description=description,
            color=discord.Color.blue()
        )
        embed.set_thumbnail(url=thumbnail_url)
        embed.set_footer(text=f"Demandé par {ctx.author.name}")
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def embedfield(self, ctx, title: str, name: str, value: str, *, description: str = None):
        """Crée un embed avec un champ personnalisé"""
        embed = discord.Embed(
            title=title,
            description=description,
            color=discord.Color.blue()
        )
        embed.add_field(name=name, value=value)
        embed.set_footer(text=f"Demandé par {ctx.author.name}")
        await ctx.send(embed=embed)

    @commands.command(name="aide")
    async def help_command(self, ctx, category: str = None):
        """Affiche le menu d'aide avec toutes les commandes disponibles"""
        if category:
            category = category.lower()
            if category in self.help_embeds:
                await ctx.send(embed=self.help_embeds[category])
            else:
                await ctx.send(f"Catégorie invalide! Catégories disponibles: {', '.join(self.help_embeds.keys())}")
            return

        self.help_embeds = {
            "général": discord.Embed(
                title="📚 Commandes Générales",
                description="Commandes de base du bot",
                color=discord.Color.blue()
            ).add_field(
                name="Commandes disponibles",
                value="""`!hello` - Le bot vous salue
`!ping` - Vérifie la latence du bot
`!info` - Affiche des informations sur le serveur
`!help [catégorie]` - Affiche ce menu d'aide""",
                inline=False
            ),
            
            "modération": discord.Embed(
                title="🛡️ Commandes de Modération",
                description="Commandes pour gérer le serveur",
                color=discord.Color.red()
            ).add_field(
                name="Commandes disponibles",
                value="""`!ban <membre> [raison]` - Bannir un membre
`!unban <id_membre>` - Débannir un membre
`!warn <membre> [raison]` - Avertir un membre
`!warns <membre>` - Voir les avertissements
`!mute <membre> [durée]` - Mettre en sourdine
`!unmute <membre>` - Retirer la sourdine
`!blacklist <membre> [raison]` - Mettre sur liste noire
`!unblacklist <membre>` - Retirer de la liste noire""",
                inline=False
            ),
            
            "sécurité": discord.Embed(
                title="🔒 Commandes de Sécurité",
                description="Commandes pour protéger le serveur",
                color=discord.Color.green()
            ).add_field(
                name="Commandes disponibles",
                value="""`!lockdown` - Active le mode lockdown
`!unlock` - Désactive le mode lockdown
`!raidcheck` - Vérifie les membres en quarantaine
`!config <paramètre> <valeur>` - Configure la sécurité
`!setautorole <rôle>` - Définit le rôle automatique
`!setwelcome <canal>` - Définit le canal de bienvenue""",
                inline=False
            ),
            
            "divertissement": discord.Embed(
                title="🎮 Commandes de Divertissement",
                description="Commandes pour s'amuser",
                color=discord.Color.gold()
            ).add_field(
                name="Commandes disponibles",
                value="""`!roll [NdM]` - Lance des dés
`!choose <option1, option2, ...>` - Choisit aléatoirement
`!poll <question> <option1> <option2> ...` - Crée un sondage
`!8ball <question>` - Pose une question
`!reverse <texte>` - Inverse le texte
`!ascii <texte>` - Convertit en art ASCII
`!countdown <secondes>` - Compte à rebours
`!randomcolor` - Génère une couleur
`!flip` - Lance une pièce
`!rps <pierre/papier/ciseaux>` - Pierre, Papier, Ciseaux
`!quote` - Affiche une citation""",
                inline=False
            ),
            
            "embed": discord.Embed(
                title="🎨 Commandes d'Embed",
                description="Commandes pour créer des embeds",
                color=discord.Color.purple()
            ).add_field(
                name="Commandes disponibles",
                value="""`!embed <titre> <description>` - Embed simple
`!embedcolor <couleur> <titre> <description>` - Embed coloré
`!embedimage <titre> <url_image> [description]` - Embed avec image
`!embedthumbnail <titre> <url_miniature> [description]` - Embed avec miniature
`!embedfield <titre> <nom> <valeur> [description]` - Embed avec champ""",
                inline=False
            )
        }

        main_embed = discord.Embed(
            title="🤖 Menu d'aide",
            description="Utilisez `!help <catégorie>` pour voir les commandes d'une catégorie spécifique",
            color=discord.Color.blue()
        )
        
        for category, embed in self.help_embeds.items():
            main_embed.add_field(
                name=f"📌 {embed.title}",
                value=f"`!help {category}`",
                inline=True
            )
            
        main_embed.set_footer(text=f"Demandé par {ctx.author.name}")
        await ctx.send(embed=main_embed)

async def setup(bot):
    await bot.add_cog(Embed(bot)) 