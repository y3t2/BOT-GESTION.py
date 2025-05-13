import discord
from discord.ext import commands
import datetime

class Management(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def createchannel(self, ctx, channel_type: str, *, name: str):
        """Crée un nouveau canal (text ou voice)"""
        channel_type = channel_type.lower()
        if channel_type == "text":
            await ctx.guild.create_text_channel(name)
            await ctx.send(f"Canal texte '{name}' créé avec succès!")
        elif channel_type == "voice":
            await ctx.guild.create_voice_channel(name)
            await ctx.send(f"Canal vocal '{name}' créé avec succès!")
        else:
            await ctx.send("Type de canal invalide! Utilisez 'text' ou 'voice'.")

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def deletechannel(self, ctx, channel: discord.TextChannel):
        """Supprime un canal"""
        await channel.delete()
        await ctx.send(f"Canal '{channel.name}' supprimé avec succès!")

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def createrole(self, ctx, *, name: str):
        """Crée un nouveau rôle"""
        role = await ctx.guild.create_role(name=name)
        await ctx.send(f"Rôle '{name}' créé avec succès!")

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def deleterole(self, ctx, role: discord.Role):
        """Supprime un rôle"""
        await role.delete()
        await ctx.send(f"Rôle '{role.name}' supprimé avec succès!")

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int):
        """Supprime un nombre spécifié de messages"""
        await ctx.channel.purge(limit=amount + 1)
        msg = await ctx.send(f"{amount} messages supprimés!")
        await msg.delete(delay=3)

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def serverinfo(self, ctx):
        """Affiche des informations détaillées sur le serveur"""
        guild = ctx.guild
        embed = discord.Embed(
            title=f"📊 Informations sur {guild.name}",
            color=discord.Color.blue()
        )
        
        embed.add_field(
            name="Informations générales",
            value=f"""
            👑 Propriétaire: {guild.owner}
            🆔 ID: {guild.id}
            📅 Créé le: {guild.created_at.strftime('%d/%m/%Y')}
            🌍 Région: {guild.region if hasattr(guild, 'region') else 'N/A'}
            """,
            inline=False
        )
        
        embed.add_field(
            name="Statistiques",
            value=f"""
            👥 Membres: {guild.member_count}
            💬 Canaux: {len(guild.channels)}
            📝 Canaux texte: {len(guild.text_channels)}
            🔊 Canaux vocaux: {len(guild.voice_channels)}
            🎭 Rôles: {len(guild.roles)}
            😀 Emojis: {len(guild.emojis)}
            """,
            inline=False
        )
        
        features = [f"✅ {feature}" for feature in guild.features]
        embed.add_field(
            name="Fonctionnalités",
            value="\n".join(features) if features else "Aucune fonctionnalité spéciale",
            inline=False
        )
        
        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)
            
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def slowmode(self, ctx, seconds: int):
        """Configure le mode lent du canal"""
        if seconds < 0 or seconds > 21600:
            await ctx.send("Le délai doit être entre 0 et 21600 secondes!")
            return
        await ctx.channel.edit(slowmode_delay=seconds)
        await ctx.send(f"Mode lent configuré à {seconds} secondes!")

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def setnickname(self, ctx, member: discord.Member, *, nickname: str = None):
        """Change le surnom d'un membre"""
        await member.edit(nick=nickname)
        if nickname:
            await ctx.send(f"Surnom de {member.name} changé en '{nickname}'!")
        else:
            await ctx.send(f"Surnom de {member.name} réinitialisé!")

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def setbanner(self, ctx, url: str):
        """Change la bannière du serveur"""
        try:
            await ctx.guild.edit(banner=url)
            await ctx.send("Bannière du serveur mise à jour avec succès!")
        except:
            await ctx.send("Erreur lors de la mise à jour de la bannière. Vérifiez l'URL!")

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def seticon(self, ctx, url: str):
        """Change l'icône du serveur"""
        try:
            await ctx.guild.edit(icon=url)
            await ctx.send("Icône du serveur mise à jour avec succès!")
        except:
            await ctx.send("Erreur lors de la mise à jour de l'icône. Vérifiez l'URL!")

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def renew(self, ctx):
        """Recrée le salon actuel"""
        channel = ctx.channel
        channel_name = channel.name
        channel_position = channel.position
        channel_category = channel.category
        channel_topic = channel.topic
        channel_slowmode = channel.slowmode_delay
        channel_nsfw = channel.is_nsfw()
        
        overwrites = channel.overwrites
        
        await channel.delete()
        
        new_channel = await ctx.guild.create_text_channel(
            name=channel_name,
            position=channel_position,
            category=channel_category,
            topic=channel_topic,
            slowmode_delay=channel_slowmode,
            nsfw=channel_nsfw,
            overwrites=overwrites
        )
        
        await new_channel.send(f"{ctx.author.mention} Salon recréé avec succès! 🎉")

async def setup(bot):
    await bot.add_cog(Management(bot)) 