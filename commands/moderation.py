import discord
from discord.ext import commands
import json
import os
from datetime import datetime, timedelta

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.warns_file = 'data/warns.json'
        self.blacklist_file = 'data/blacklist.json'
        self.muted_users = {}
        
        # Créer le dossier data s'il n'existe pas
        if not os.path.exists('data'):
            os.makedirs('data')
            
        # Initialiser les fichiers JSON s'ils n'existent pas
        if not os.path.exists(self.warns_file):
            with open(self.warns_file, 'w') as f:
                json.dump({}, f)
                
        if not os.path.exists(self.blacklist_file):
            with open(self.blacklist_file, 'w') as f:
                json.dump({}, f)

    def load_data(self, file):
        with open(file, 'r') as f:
            return json.load(f)

    def save_data(self, file, data):
        with open(file, 'w') as f:
            json.dump(data, f, indent=4)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason="Aucune raison spécifiée"):
        """Bannir un membre du serveur"""
        try:
            await member.ban(reason=reason)
            embed = discord.Embed(
                title="🔨 Membre banni",
                description=f"{member.mention} a été banni du serveur.",
                color=discord.Color.red()
            )
            embed.add_field(name="Raison", value=reason)
            embed.add_field(name="Modérateur", value=ctx.author.mention)
            await ctx.send(embed=embed)
        except discord.Forbidden:
            await ctx.send("Je n'ai pas les permissions nécessaires pour bannir ce membre.")

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member_id: int):
        """Débannir un membre du serveur"""
        try:
            user = await self.bot.fetch_user(member_id)
            await ctx.guild.unban(user)
            embed = discord.Embed(
                title="🔓 Membre débanni",
                description=f"{user.mention} a été débanni du serveur.",
                color=discord.Color.green()
            )
            await ctx.send(embed=embed)
        except discord.NotFound:
            await ctx.send("Utilisateur non trouvé.")
        except discord.Forbidden:
            await ctx.send("Je n'ai pas les permissions nécessaires pour débannir ce membre.")

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def warn(self, ctx, member: discord.Member, *, reason="Aucune raison spécifiée"):
        """Avertir un membre"""
        warns = self.load_data(self.warns_file)
        if str(member.id) not in warns:
            warns[str(member.id)] = []
        
        warn_data = {
            "reason": reason,
            "moderator": ctx.author.id,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        warns[str(member.id)].append(warn_data)
        self.save_data(self.warns_file, warns)
        
        embed = discord.Embed(
            title="⚠️ Avertissement",
            description=f"{member.mention} a reçu un avertissement.",
            color=discord.Color.orange()
        )
        embed.add_field(name="Raison", value=reason)
        embed.add_field(name="Modérateur", value=ctx.author.mention)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def warns(self, ctx, member: discord.Member):
        """Voir les avertissements d'un membre"""
        warns = self.load_data(self.warns_file)
        if str(member.id) not in warns or not warns[str(member.id)]:
            await ctx.send(f"{member.mention} n'a aucun avertissement.")
            return

        embed = discord.Embed(
            title=f"⚠️ Avertissements de {member.name}",
            color=discord.Color.orange()
        )
        
        for i, warn in enumerate(warns[str(member.id)], 1):
            embed.add_field(
                name=f"Avertissement #{i}",
                value=f"Raison: {warn['reason']}\nDate: {warn['date']}",
                inline=False
            )
        
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def mute(self, ctx, member: discord.Member, duration: int = 10):
        """Mettre en sourdine un membre (durée en minutes)"""
        muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
        if not muted_role:
            muted_role = await ctx.guild.create_role(name="Muted")
            for channel in ctx.guild.channels:
                await channel.set_permissions(muted_role, speak=False, send_messages=False)

        await member.add_roles(muted_role)
        self.muted_users[member.id] = datetime.now() + timedelta(minutes=duration)
        
        embed = discord.Embed(
            title="🔇 Membre mis en sourdine",
            description=f"{member.mention} a été mis en sourdine pour {duration} minutes.",
            color=discord.Color.orange()
        )
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def unmute(self, ctx, member: discord.Member):
        """Retirer la sourdine d'un membre"""
        muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
        if muted_role in member.roles:
            await member.remove_roles(muted_role)
            if member.id in self.muted_users:
                del self.muted_users[member.id]
            
            embed = discord.Embed(
                title="🔊 Sourdine retirée",
                description=f"{member.mention} n'est plus en sourdine.",
                color=discord.Color.green()
            )
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"{member.mention} n'est pas en sourdine.")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def blacklist(self, ctx, member: discord.Member, *, reason="Aucune raison spécifiée"):
        """Mettre un membre sur liste noire"""
        blacklist = self.load_data(self.blacklist_file)
        blacklist[str(member.id)] = {
            "reason": reason,
            "moderator": ctx.author.id,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.save_data(self.blacklist_file, blacklist)
        
        embed = discord.Embed(
            title="⛔ Membre mis sur liste noire",
            description=f"{member.mention} a été mis sur liste noire.",
            color=discord.Color.red()
        )
        embed.add_field(name="Raison", value=reason)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def unblacklist(self, ctx, member: discord.Member):
        """Retirer un membre de la liste noire"""
        blacklist = self.load_data(self.blacklist_file)
        if str(member.id) in blacklist:
            del blacklist[str(member.id)]
            self.save_data(self.blacklist_file, blacklist)
            
            embed = discord.Embed(
                title="✅ Membre retiré de la liste noire",
                description=f"{member.mention} a été retiré de la liste noire.",
                color=discord.Color.green()
            )
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"{member.mention} n'est pas sur la liste noire.")

async def setup(bot):
    await bot.add_cog(Moderation(bot)) 