import discord
from discord.ext import commands
import json
import os
from datetime import datetime, timedelta
import asyncio

class Security(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.raid_protection = {}
        self.anti_spam = {}
        self.lockdown_channels = set()
        
        if not os.path.exists('data'):
            os.makedirs('data')
            
        self.config_file = 'data/security_config.json'
        if not os.path.exists(self.config_file):
            default_config = {
                "raid_threshold": 5,  
                "raid_timeframe": 10,  
                "spam_threshold": 5,  
                "spam_timeframe": 5,   
                "max_mentions": 5,    
                "max_emojis": 10,      
                "max_caps": 70,        
                "auto_role": None,     
                "welcome_channel": None 
            }
            with open(self.config_file, 'w') as f:
                json.dump(default_config, f, indent=4)

    def load_config(self):
        with open(self.config_file, 'r') as f:
            return json.load(f)

    def save_config(self, config):
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=4)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        """Anti-raid: Surveille les nouveaux membres"""
        config = self.load_config()
        guild_id = str(member.guild.id)
        
        if guild_id not in self.raid_protection:
            self.raid_protection[guild_id] = []
        
        self.raid_protection[guild_id].append({
            'member': member.id,
            'time': datetime.now()
        })
        
        self.raid_protection[guild_id] = [
            entry for entry in self.raid_protection[guild_id]
            if datetime.now() - entry['time'] < timedelta(seconds=config['raid_timeframe'])
        ]
        
        if len(self.raid_protection[guild_id]) >= config['raid_threshold']:
            await self.handle_raid(member.guild)
            
        if config['auto_role']:
            role = member.guild.get_role(config['auto_role'])
            if role:
                await member.add_roles(role)
        
        if config['welcome_channel']:
            channel = member.guild.get_channel(config['welcome_channel'])
            if channel:
                embed = discord.Embed(
                    title="👋 Nouveau membre!",
                    description=f"Bienvenue {member.mention} sur {member.guild.name}!",
                    color=discord.Color.green()
                )
                embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
                await channel.send(embed=embed)

    async def handle_raid(self, guild):
        """Gère une situation de raid"""
        config = self.load_config()
        config['raid_mode'] = True
        self.save_config(config)
        
        quarantine_role = discord.utils.get(guild.roles, name="Quarantaine")
        if not quarantine_role:
            quarantine_role = await guild.create_role(
                name="Quarantaine",
                color=discord.Color.red(),
                reason="Protection anti-raid"
            )
            
            for channel in guild.channels:
                await channel.set_permissions(quarantine_role,
                    read_messages=False,
                    send_messages=False,
                    add_reactions=False
                )
        
        for entry in self.raid_protection[str(guild.id)]:
            member = guild.get_member(entry['member'])
            if member:
                await member.add_roles(quarantine_role)
        
        admin_channel = discord.utils.get(guild.channels, name="admin-log")
        if admin_channel:
            await admin_channel.send(
                "🚨 **ALERTE RAID DÉTECTÉE**\n"
                "Le mode raid a été activé. Les nouveaux membres ont été mis en quarantaine.\n"
                "Utilisez `!raidcheck` pour vérifier les membres en quarantaine."
            )

    @commands.Cog.listener()
    async def on_message(self, message):
        """Anti-spam et protection contre les mentions massives"""
        if message.author.bot:
            return
            
        config = self.load_config()
        guild_id = str(message.guild.id)
        
        # Anti-spam
        if guild_id not in self.anti_spam:
            self.anti_spam[guild_id] = {}
            
        if message.author.id not in self.anti_spam[guild_id]:
            self.anti_spam[guild_id][message.author.id] = []
            
        self.anti_spam[guild_id][message.author.id].append({
            'time': datetime.now(),
            'content': message.content
        })
        
        self.anti_spam[guild_id][message.author.id] = [
            msg for msg in self.anti_spam[guild_id][message.author.id]
            if datetime.now() - msg['time'] < timedelta(seconds=config['spam_timeframe'])
        ]
        
        if len(self.anti_spam[guild_id][message.author.id]) >= config['spam_threshold']:
            await self.handle_spam(message)
            return
            
        if len(message.mentions) > config['max_mentions']:
            await self.handle_mention_spam(message)
            return
            
        emoji_count = sum(1 for c in message.content if c in '😀😃😄😁😆😅😂🤣😊😇🙂🙃😉😌😍🥰😘😗😙😚😋😛😝😜🤪🤨🧐🤓😎🤩🥳😏😒😞😔😟😕🙁☹️😣😖😫😩🥺😢😭😤😠😡🤬🤯😳🥵🥶😱😨😰😥😓🤗🤔🤭🤫🤥😶😐😑😬🙄😯😦😧😮😲🥱😴🤤😪😵🤐🥴🤢🤮🤧😷🤒🤕')
        if emoji_count > config['max_emojis']:
            await self.handle_emoji_spam(message)
            return
            
        if len(message.content) > 10:
            caps_count = sum(1 for c in message.content if c.isupper())
            caps_percentage = (caps_count / len(message.content)) * 100
            if caps_percentage > config['max_caps']:
                await self.handle_caps_spam(message)
                return

    async def handle_spam(self, message):
        """Gère le spam de messages"""
        await message.delete()
        await message.channel.send(
            f"{message.author.mention} Arrêtez le spam!",
            delete_after=5
        )

    async def handle_mention_spam(self, message):
        """Gère le spam de mentions"""
        await message.delete()
        await message.channel.send(
            f"{message.author.mention} Trop de mentions!",
            delete_after=5
        )

    async def handle_emoji_spam(self, message):
        """Gère le spam d'emojis"""
        await message.delete()
        await message.channel.send(
            f"{message.author.mention} Trop d'emojis!",
            delete_after=5
        )

    async def handle_caps_spam(self, message):
        """Gère le spam de majuscules"""
        await message.delete()
        await message.channel.send(
            f"{message.author.mention} Pas besoin de crier!",
            delete_after=5
        )

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def lockdown(self, ctx):
        """Active le mode lockdown sur le serveur"""
        if ctx.channel.id in self.lockdown_channels:
            await ctx.send("Le mode lockdown est déjà actif dans ce canal!")
            return
            
        self.lockdown_channels.add(ctx.channel.id)
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
        
        embed = discord.Embed(
            title="🔒 Mode Lockdown",
            description="Ce canal est maintenant en mode lockdown. Seuls les administrateurs peuvent envoyer des messages.",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def unlock(self, ctx):
        """Désactive le mode lockdown"""
        if ctx.channel.id not in self.lockdown_channels:
            await ctx.send("Le mode lockdown n'est pas actif dans ce canal!")
            return
            
        self.lockdown_channels.remove(ctx.channel.id)
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
        
        embed = discord.Embed(
            title="🔓 Mode Lockdown désactivé",
            description="Ce canal est maintenant débloqué.",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def raidcheck(self, ctx):
        """Vérifie les membres en quarantaine"""
        quarantine_role = discord.utils.get(ctx.guild.roles, name="Quarantaine")
        if not quarantine_role:
            await ctx.send("Aucun membre n'est en quarantaine.")
            return
            
        members = quarantine_role.members
        if not members:
            await ctx.send("Aucun membre n'est en quarantaine.")
            return
            
        embed = discord.Embed(
            title="🔍 Membres en quarantaine",
            description=f"Nombre de membres: {len(members)}",
            color=discord.Color.orange()
        )
        
        for member in members:
            embed.add_field(
                name=member.name,
                value=f"ID: {member.id}\nRejoint le: {member.joined_at.strftime('%d/%m/%Y %H:%M')}",
                inline=False
            )
            
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def config(self, ctx, setting: str, value: int):
        """Configure les paramètres de sécurité"""
        config = self.load_config()
        if setting not in config:
            await ctx.send(f"Paramètre invalide! Paramètres disponibles: {', '.join(config.keys())}")
            return
            
        config[setting] = value
        self.save_config(config)
        
        embed = discord.Embed(
            title="⚙️ Configuration mise à jour",
            description=f"Le paramètre `{setting}` a été défini à `{value}`",
            color=discord.Color.blue()
        )
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setautorole(self, ctx, role: discord.Role):
        """Définit le rôle automatique pour les nouveaux membres"""
        config = self.load_config()
        config['auto_role'] = role.id
        self.save_config(config)
        
        embed = discord.Embed(
            title="👥 Rôle automatique configuré",
            description=f"Le rôle {role.mention} sera automatiquement attribué aux nouveaux membres.",
            color=discord.Color.blue()
        )
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setwelcome(self, ctx, channel: discord.TextChannel):
        """Définit le canal de bienvenue"""
        config = self.load_config()
        config['welcome_channel'] = channel.id
        self.save_config(config)
        
        embed = discord.Embed(
            title="👋 Canal de bienvenue configuré",
            description=f"Les messages de bienvenue seront envoyés dans {channel.mention}",
            color=discord.Color.blue()
        )
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Security(bot)) 