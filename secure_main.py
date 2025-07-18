import discord
from discord import app_commands
from discord.ext import commands
import os
import asyncio
import logging
import random
from datetime import datetime, timezone, timedelta
import pytz
import json
from security_config import security, SecurityError

# Bot configuration with security
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True
intents.guild_messages = True
intents.dm_messages = True

class SecureBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='!', intents=intents)
        self.security = security
        self.start_time = datetime.now(timezone.utc)
        self.log_channels = {}  # Store logging channels per server
        self.load_log_config()
    
    def load_log_config(self):
        """Load logging configuration from file"""
        try:
            with open('log_config.json', 'r') as f:
                self.log_channels = json.load(f)
        except FileNotFoundError:
            self.log_channels = {}
    
    def save_log_config(self):
        """Save logging configuration to file"""
        with open('log_config.json', 'w') as f:
            json.dump(self.log_channels, f, indent=2)
    
    async def setup_hook(self):
        """Secure bot setup"""
        try:
            synced = await self.tree.sync()
            logging.info(f"Successfully synced {len(synced)} slash commands")
        except Exception as e:
            logging.error(f"Failed to sync commands: {e}")
    
    async def on_ready(self):
        """Secure bot ready event"""
        logging.info("=" * 50)
        logging.info(f"{self.user} connected securely!")
        logging.info(f"Bot ID: {self.user.id}")
        logging.info(f"Servers: {len(self.guilds)}")
        logging.info(f"Environment: {self.security.environment}")
        logging.info(f"Current User's Login: cRaz0y")
        logging.info(f"Current Date and Time (UTC - YYYY-MM-DD HH:MM:SS formatted): {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')}")
        logging.info("=" * 50)
        
        # Set status based on environment
        if self.security.environment == 'development':
            activity = discord.Game(name="🔧 L-Hub Development | Secure Mode")
        else:
            activity = discord.Game(name="L-Hub on TOP. https://discord.gg/MrgrqUYfx6")
        
        await self.change_presence(activity=activity)
    
    async def log_event(self, guild_id, embed):
        """Send log embed to configured log channel"""
        if str(guild_id) in self.log_channels:
            channel_id = self.log_channels[str(guild_id)]
            channel = self.get_channel(channel_id)
            if channel:
                try:
                    await channel.send(embed=embed)
                except:
                    pass
    
    # =================================
    # LOGGING EVENTS
    # =================================
    
    async def on_message(self, message):
        """Log all messages"""
        if message.author.bot:
            return
        
        embed = discord.Embed(
            title="📝 Message Sent",
            color=0x00ff00,
            timestamp=datetime.now(timezone.utc)
        )
        embed.add_field(name="👤 User", value=f"{message.author.mention} ({message.author})", inline=True)
        embed.add_field(name="📁 Channel", value=f"{message.channel.mention}", inline=True)
        embed.add_field(name="🆔 Message ID", value=message.id, inline=True)
        embed.add_field(name="💬 Content", value=message.content[:1000] if message.content else "*No text content*", inline=False)
        
        if message.attachments:
            embed.add_field(name="📎 Attachments", value="\n".join([att.filename for att in message.attachments]), inline=False)
        
        embed.set_thumbnail(url=message.author.avatar.url if message.author.avatar else message.author.default_avatar.url)
        
        await self.log_event(message.guild.id, embed)
    
    async def on_message_delete(self, message):
        """Log deleted messages"""
        if message.author.bot:
            return
        
        embed = discord.Embed(
            title="🗑️ Message Deleted",
            color=0xff4444,
            timestamp=datetime.now(timezone.utc)
        )
        embed.add_field(name="👤 User", value=f"{message.author.mention} ({message.author})", inline=True)
        embed.add_field(name="📁 Channel", value=f"{message.channel.mention}", inline=True)
        embed.add_field(name="🆔 Message ID", value=message.id, inline=True)
        embed.add_field(name="💬 Deleted Content", value=message.content[:1000] if message.content else "*No text content*", inline=False)
        embed.add_field(name="📅 Original Time", value=message.created_at.strftime('%Y-%m-%d %H:%M:%S UTC'), inline=True)
        
        if message.attachments:
            embed.add_field(name="📎 Attachments", value="\n".join([att.filename for att in message.attachments]), inline=False)
        
        embed.set_thumbnail(url=message.author.avatar.url if message.author.avatar else message.author.default_avatar.url)
        
        await self.log_event(message.guild.id, embed)
    
    async def on_message_edit(self, before, after):
        """Log edited messages"""
        if before.author.bot or before.content == after.content:
            return
        
        embed = discord.Embed(
            title="✏️ Message Edited",
            color=0xffaa00,
            timestamp=datetime.now(timezone.utc)
        )
        embed.add_field(name="👤 User", value=f"{before.author.mention} ({before.author})", inline=True)
        embed.add_field(name="📁 Channel", value=f"{before.channel.mention}", inline=True)
        embed.add_field(name="🆔 Message ID", value=before.id, inline=True)
        embed.add_field(name="📝 Before", value=before.content[:500] if before.content else "*No content*", inline=False)
        embed.add_field(name="📝 After", value=after.content[:500] if after.content else "*No content*", inline=False)
        embed.add_field(name="🔗 Jump to Message", value=f"[Click here]({after.jump_url})", inline=True)
        
        embed.set_thumbnail(url=before.author.avatar.url if before.author.avatar else before.author.default_avatar.url)
        
        await self.log_event(before.guild.id, embed)
    
    async def on_member_join(self, member):
        """Log member joins"""
        embed = discord.Embed(
            title="📥 Member Joined",
            color=0x00ff00,
            timestamp=datetime.now(timezone.utc)
        )
        embed.add_field(name="👤 User", value=f"{member.mention} ({member})", inline=True)
        embed.add_field(name="🆔 User ID", value=member.id, inline=True)
        embed.add_field(name="📅 Account Created", value=member.created_at.strftime('%Y-%m-%d %H:%M:%S UTC'), inline=True)
        embed.add_field(name="👥 Member Count", value=member.guild.member_count, inline=True)
        
        # Account age
        account_age = datetime.now(timezone.utc) - member.created_at
        embed.add_field(name="⏰ Account Age", value=f"{account_age.days} days old", inline=True)
        
        embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
        
        await self.log_event(member.guild.id, embed)
    
    async def on_member_remove(self, member):
        """Log member leaves"""
        embed = discord.Embed(
            title="📤 Member Left",
            color=0xff4444,
            timestamp=datetime.now(timezone.utc)
        )
        embed.add_field(name="👤 User", value=f"{member.mention} ({member})", inline=True)
        embed.add_field(name="🆔 User ID", value=member.id, inline=True)
        embed.add_field(name="📅 Joined Server", value=member.joined_at.strftime('%Y-%m-%d %H:%M:%S UTC') if member.joined_at else "Unknown", inline=True)
        embed.add_field(name="👥 Member Count", value=member.guild.member_count, inline=True)
        
        # Time in server
        if member.joined_at:
            time_in_server = datetime.now(timezone.utc) - member.joined_at
            embed.add_field(name="⏰ Time in Server", value=f"{time_in_server.days} days", inline=True)
        
        # Roles
        roles = [role.name for role in member.roles[1:]]  # Exclude @everyone
        if roles:
            embed.add_field(name="🎭 Roles", value=", ".join(roles[:10]), inline=False)
        
        embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
        
        await self.log_event(member.guild.id, embed)
    
    async def on_member_update(self, before, after):
        """Log member updates (nickname, roles, etc.)"""
        changes = []
        
        # Nickname change
        if before.nick != after.nick:
            changes.append(f"**Nickname:** `{before.nick or 'None'}` → `{after.nick or 'None'}`")
        
        # Role changes
        if before.roles != after.roles:
            added_roles = set(after.roles) - set(before.roles)
            removed_roles = set(before.roles) - set(after.roles)
            
            if added_roles:
                changes.append(f"**Roles Added:** {', '.join([role.name for role in added_roles])}")
            if removed_roles:
                changes.append(f"**Roles Removed:** {', '.join([role.name for role in removed_roles])}")
        
        if changes:
            embed = discord.Embed(
                title="👤 Member Updated",
                color=0x0099ff,
                timestamp=datetime.now(timezone.utc)
            )
            embed.add_field(name="👤 User", value=f"{after.mention} ({after})", inline=True)
            embed.add_field(name="🔄 Changes", value="\n".join(changes), inline=False)
            embed.set_thumbnail(url=after.avatar.url if after.avatar else after.default_avatar.url)
            
            await self.log_event(after.guild.id, embed)
    
    async def on_guild_channel_create(self, channel):
        """Log channel creation"""
        embed = discord.Embed(
            title="📁 Channel Created",
            color=0x00ff00,
            timestamp=datetime.now(timezone.utc)
        )
        embed.add_field(name="📁 Channel", value=f"{channel.mention} (`{channel.name}`)", inline=True)
        embed.add_field(name="🆔 Channel ID", value=channel.id, inline=True)
        embed.add_field(name="📂 Type", value=str(channel.type).title(), inline=True)
        
        await self.log_event(channel.guild.id, embed)
    
    async def on_guild_channel_delete(self, channel):
        """Log channel deletion"""
        embed = discord.Embed(
            title="🗑️ Channel Deleted",
            color=0xff4444,
            timestamp=datetime.now(timezone.utc)
        )
        embed.add_field(name="📁 Channel", value=f"`{channel.name}`", inline=True)
        embed.add_field(name="🆔 Channel ID", value=channel.id, inline=True)
        embed.add_field(name="📂 Type", value=str(channel.type).title(), inline=True)
        
        await self.log_event(channel.guild.id, embed)
    
    async def on_voice_state_update(self, member, before, after):
        """Log voice channel activity"""
        if before.channel == after.channel:
            return
        
        if before.channel is None and after.channel is not None:
            # User joined voice channel
            embed = discord.Embed(
                title="🔊 Voice Channel Joined",
                color=0x00ff00,
                timestamp=datetime.now(timezone.utc)
            )
            embed.add_field(name="👤 User", value=f"{member.mention} ({member})", inline=True)
            embed.add_field(name="🔊 Channel", value=after.channel.name, inline=True)
            
        elif before.channel is not None and after.channel is None:
            # User left voice channel
            embed = discord.Embed(
                title="🔇 Voice Channel Left",
                color=0xff4444,
                timestamp=datetime.now(timezone.utc)
            )
            embed.add_field(name="👤 User", value=f"{member.mention} ({member})", inline=True)
            embed.add_field(name="🔊 Channel", value=before.channel.name, inline=True)
            
        else:
            # User moved between voice channels
            embed = discord.Embed(
                title="🔄 Voice Channel Moved",
                color=0x0099ff,
                timestamp=datetime.now(timezone.utc)
            )
            embed.add_field(name="👤 User", value=f"{member.mention} ({member})", inline=True)
            embed.add_field(name="🔊 From", value=before.channel.name, inline=True)
            embed.add_field(name="🔊 To", value=after.channel.name, inline=True)
        
        embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
        await self.log_event(member.guild.id, embed)

bot = SecureBot()

# =================================
# LOGGING COMMANDS
# =================================

@bot.tree.command(name="setlogchannel", description="Set the logging channel for this server (Admin only)")
@app_commands.describe(channel="Channel where logs will be sent")
@app_commands.default_permissions(administrator=True)
async def set_log_channel(interaction: discord.Interaction, channel: discord.TextChannel):
    bot.log_channels[str(interaction.guild.id)] = channel.id
    bot.save_log_config()
    
    embed = discord.Embed(
        title="📋 Logging Channel Set",
        description=f"All server logs will now be sent to {channel.mention}",
        color=0x00ff00
    )
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="removelogchannel", description="Remove logging for this server (Admin only)")
@app_commands.default_permissions(administrator=True)
async def remove_log_channel(interaction: discord.Interaction):
    if str(interaction.guild.id) in bot.log_channels:
        del bot.log_channels[str(interaction.guild.id)]
        bot.save_log_config()
        
        embed = discord.Embed(
            title="📋 Logging Disabled",
            description="Server logging has been disabled",
            color=0xff9900
        )
    else:
        embed = discord.Embed(
            title="❌ No Logging Channel",
            description="No logging channel was set for this server",
            color=0xff4444
        )
    
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="logstatus", description="Check current logging status (Admin only)")
@app_commands.default_permissions(administrator=True)
async def log_status(interaction: discord.Interaction):
    if str(interaction.guild.id) in bot.log_channels:
        channel_id = bot.log_channels[str(interaction.guild.id)]
        channel = bot.get_channel(channel_id)
        
        if channel:
            embed = discord.Embed(
                title="📋 Logging Status",
                description=f"✅ Logging is **enabled**\n📁 Log Channel: {channel.mention}",
                color=0x00ff00
            )
            embed.add_field(name="📊 Events Logged", value="• Messages (sent/edited/deleted)\n• Member joins/leaves\n• Role changes\n• Channel creation/deletion\n• Voice activity\n• Nickname changes", inline=False)
        else:
            embed = discord.Embed(
                title="📋 Logging Status",
                description="❌ Log channel not found (may have been deleted)",
                color=0xff4444
            )
    else:
        embed = discord.Embed(
            title="📋 Logging Status",
            description="❌ Logging is **disabled**\nUse `/setlogchannel` to enable logging",
            color=0xff4444
        )
    
    await interaction.response.send_message(embed=embed)

# =================================
# SECURITY COMMANDS
# =================================

@bot.tree.command(name="security", description="Security status (Owner only)")
async def security_status(interaction: discord.Interaction):
    """Display security status - owner only"""
    if not bot.security.is_owner(interaction.user.id):
        await interaction.response.send_message("❌ This command is restricted to the bot owner.", ephemeral=True)
        return
    
    uptime = datetime.now(timezone.utc) - bot.start_time
    
    embed = discord.Embed(
        title="🔒 Security Status",
        description="Current bot security information",
        color=0x00ff00
    )
    
    embed.add_field(name="🌍 Environment", value=bot.security.environment.title(), inline=True)
    embed.add_field(name="🐛 Debug Mode", value="✅ On" if bot.security.debug_mode else "❌ Off", inline=True)
    embed.add_field(name="👑 Owner", value=f"<@{bot.security.owner_id}>" if bot.security.owner_id else "Not Set", inline=True)
    embed.add_field(name="🕒 Uptime", value=f"{uptime.days}d {uptime.seconds//3600}h {(uptime.seconds//60)%60}m", inline=True)
    embed.add_field(name="📊 Servers", value=len(bot.guilds), inline=True)
    embed.add_field(name="⚙️ Commands", value=len(bot.tree.get_commands()), inline=True)
    
    embed.set_footer(text=f"Secure Bot | {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}")
    
    await interaction.response.send_message(embed=embed, ephemeral=True)

# =================================
# OWNER-ONLY BOT MANAGEMENT
# =================================

@bot.tree.command(name="shutdown", description="Safely shutdown the bot (Owner only)")
async def shutdown_command(interaction: discord.Interaction):
    if not bot.security.is_owner(interaction.user.id):
        await interaction.response.send_message("❌ Owner only command!", ephemeral=True)
        return
    
    embed = discord.Embed(
        title="🔴 Bot Shutdown",
        description="Bot is shutting down safely...",
        color=0xff0000
    )
    await interaction.response.send_message(embed=embed)
    await bot.close()

@bot.tree.command(name="restart", description="Restart the bot (Owner only)")
async def restart_command(interaction: discord.Interaction):
    if not bot.security.is_owner(interaction.user.id):
        await interaction.response.send_message("❌ Owner only command!", ephemeral=True)
        return
    
    embed = discord.Embed(
        title="🔄 Bot Restart",
        description="Bot is restarting...",
        color=0xff9900
    )
    await interaction.response.send_message(embed=embed)
    os._exit(0)

@bot.tree.command(name="status", description="Change bot status (Owner only)")
@app_commands.describe(
    activity_type="Type of activity (playing, watching, listening, streaming)",
    text="Status text"
)
async def status_command(interaction: discord.Interaction, activity_type: str, text: str):
    if not bot.security.is_owner(interaction.user.id):
        await interaction.response.send_message("❌ Owner only command!", ephemeral=True)
        return
    
    activity_types = {
        "playing": discord.Game(name=text),
        "watching": discord.Activity(type=discord.ActivityType.watching, name=text),
        "listening": discord.Activity(type=discord.ActivityType.listening, name=text),
        "streaming": discord.Streaming(name=text, url="https://twitch.tv/placeholder")
    }
    
    activity = activity_types.get(activity_type.lower())
    if not activity:
        await interaction.response.send_message("❌ Invalid activity type! Use: playing, watching, listening, streaming", ephemeral=True)
        return
    
    await bot.change_presence(activity=activity)
    
    embed = discord.Embed(
        title="✅ Status Updated",
        description=f"Bot status changed to: **{activity_type.title()}** {text}",
        color=0x00ff00
    )
    await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.tree.command(name="servers", description="List all servers the bot is in (Owner only)")
async def servers_command(interaction: discord.Interaction):
    if not bot.security.is_owner(interaction.user.id):
        await interaction.response.send_message("❌ Owner only command!", ephemeral=True)
        return
    
    embed = discord.Embed(
        title="🏠 Bot Servers",
        description=f"Bot is currently in {len(bot.guilds)} servers:",
        color=0x0099ff
    )
    
    for guild in bot.guilds[:10]:  # Show first 10 servers
        embed.add_field(
            name=f"🏠 {guild.name}",
            value=f"ID: `{guild.id}`\nMembers: {guild.member_count}\nOwner: {guild.owner}",
            inline=False
        )
    
    if len(bot.guilds) > 10:
        embed.set_footer(text=f"Showing 10 of {len(bot.guilds)} servers")
    
    await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.tree.command(name="leave", description="Leave a server (Owner only)")
@app_commands.describe(server_id="Server ID to leave")
async def leave_server_command(interaction: discord.Interaction, server_id: str):
    if not bot.security.is_owner(interaction.user.id):
        await interaction.response.send_message("❌ Owner only command!", ephemeral=True)
        return
    
    try:
        guild = bot.get_guild(int(server_id))
        if not guild:
            await interaction.response.send_message("❌ Server not found!", ephemeral=True)
            return
        
        guild_name = guild.name
        await guild.leave()
        
        embed = discord.Embed(
            title="🚪 Left Server",
            description=f"Successfully left server: **{guild_name}**",
            color=0xff9900
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        
    except ValueError:
        await interaction.response.send_message("❌ Invalid server ID!", ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(f"❌ Error leaving server: {e}", ephemeral=True)

@bot.tree.command(name="globalban", description="Ban user from all mutual servers (Owner only)")
@app_commands.describe(
    user_id="User ID to ban globally",
    reason="Reason for global ban"
)
async def globalban_command(interaction: discord.Interaction, user_id: str, reason: str = "Global ban by owner"):
    if not bot.security.is_owner(interaction.user.id):
        await interaction.response.send_message("❌ Owner only command!", ephemeral=True)
        return
    
    try:
        user = await bot.fetch_user(int(user_id))
        banned_from = []
        
        for guild in bot.guilds:
            try:
                member = guild.get_member(user.id)
                if member:
                    await member.ban(reason=f"Global ban: {reason}")
                    banned_from.append(guild.name)
            except:
                pass
        
        embed = discord.Embed(
            title="🔨 Global Ban",
            description=f"**User:** {user.mention}\n**Reason:** {reason}\n**Banned from {len(banned_from)} servers**",
            color=0xff0000
        )
        if banned_from:
            embed.add_field(name="🏠 Servers", value="\n".join(banned_from[:10]), inline=False)
        
        await interaction.response.send_message(embed=embed, ephemeral=True)
        
    except ValueError:
        await interaction.response.send_message("❌ Invalid user ID!", ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(f"❌ Error: {e}", ephemeral=True)

@bot.tree.command(name="userinfo_global", description="Get detailed user info across all servers (Owner only)")
@app_commands.describe(user_id="User ID to check")
async def userinfo_global_command(interaction: discord.Interaction, user_id: str):
    if not bot.security.is_owner(interaction.user.id):
        await interaction.response.send_message("❌ Owner only command!", ephemeral=True)
        return
    
    try:
        user = await bot.fetch_user(int(user_id))
        mutual_servers = []
        
        for guild in bot.guilds:
            member = guild.get_member(user.id)
            if member:
                mutual_servers.append(f"🏠 {guild.name}")
        
        embed = discord.Embed(
            title=f"🔍 Global User Info - {user.name}",
            color=0x0099ff
        )
        embed.set_thumbnail(url=user.avatar.url if user.avatar else user.default_avatar.url)
        embed.add_field(name="🆔 User ID", value=user.id, inline=True)
        embed.add_field(name="📅 Account Created", value=user.created_at.strftime("%B %d, %Y"), inline=True)
        embed.add_field(name="🤖 Bot", value="Yes" if user.bot else "No", inline=True)
        embed.add_field(name="🏠 Mutual Servers", value=f"{len(mutual_servers)} servers", inline=True)
        
        if mutual_servers:
            embed.add_field(name="📋 Server List", value="\n".join(mutual_servers[:10]), inline=False)
            if len(mutual_servers) > 10:
                embed.set_footer(text=f"Showing 10 of {len(mutual_servers)} servers")
        
        await interaction.response.send_message(embed=embed, ephemeral=True)
        
    except ValueError:
        await interaction.response.send_message("❌ Invalid user ID!", ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(f"❌ Error: {e}", ephemeral=True)

@bot.tree.command(name="stats", description="Detailed bot statistics (Owner only)")
async def stats_command(interaction: discord.Interaction):
    if not bot.security.is_owner(interaction.user.id):
        await interaction.response.send_message("❌ Owner only command!", ephemeral=True)
        return
    
    uptime = datetime.now(timezone.utc) - bot.start_time
    total_members = sum(guild.member_count for guild in bot.guilds)
    
    embed = discord.Embed(
        title="📊 Bot Statistics",
        color=0x0099ff
    )
    embed.add_field(name="🕒 Uptime", value=f"{uptime.days}d {uptime.seconds//3600}h {(uptime.seconds//60)%60}m", inline=True)
    embed.add_field(name="🏠 Servers", value=len(bot.guilds), inline=True)
    embed.add_field(name="👥 Total Users", value=f"{total_members:,}", inline=True)
    embed.add_field(name="⚙️ Commands", value=len(bot.tree.get_commands()), inline=True)
    embed.add_field(name="🌍 Environment", value=bot.security.environment.title(), inline=True)
    embed.add_field(name="🐛 Debug Mode", value="On" if bot.security.debug_mode else "Off", inline=True)
    embed.add_field(name="📋 Logging Servers", value=len(bot.log_channels), inline=True)
    
    # Memory usage (if psutil is installed)
    try:
        import psutil
        process = psutil.Process()
        memory_mb = process.memory_info().rss / 1024 / 1024
        embed.add_field(name="💾 Memory Usage", value=f"{memory_mb:.1f} MB", inline=True)
    except ImportError:
        embed.add_field(name="💾 Memory", value="Install psutil for memory info", inline=True)
    
    embed.set_footer(text=f"Bot ID: {bot.user.id}")
    await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.tree.command(name="logs", description="View recent bot logs (Owner only)")
async def logs_command(interaction: discord.Interaction):
    if not bot.security.is_owner(interaction.user.id):
        await interaction.response.send_message("❌ Owner only command!", ephemeral=True)
        return
    
    embed = discord.Embed(
        title="📋 Recent Activity",
        description="Recent bot activity and events",
        color=0x9932cc
    )
    embed.add_field(name="🕒 Last Restart", value=bot.start_time.strftime('%Y-%m-%d %H:%M:%S UTC'), inline=True)
    embed.add_field(name="📊 Commands Synced", value=len(bot.tree.get_commands()), inline=True)
    embed.add_field(name="🔒 Security Status", value="✅ Active", inline=True)
    embed.add_field(name="📋 Logging Active", value=f"{len(bot.log_channels)} servers", inline=True)
    embed.add_field(name="🏠 Total Servers", value=len(bot.guilds), inline=True)
    embed.add_field(name="👤 Owner", value=f"<@{bot.security.owner_id}>", inline=True)
    
    await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.tree.command(name="emergency_stop", description="Emergency bot shutdown (Owner only)")
async def emergency_stop_command(interaction: discord.Interaction):
    if not bot.security.is_owner(interaction.user.id):
        await interaction.response.send_message("❌ Owner only command!", ephemeral=True)
        return
    
    embed = discord.Embed(
        title="🚨 EMERGENCY SHUTDOWN",
        description="Bot shutting down immediately!",
        color=0xff0000
    )
    await interaction.response.send_message(embed=embed, ephemeral=True)
    
    # Log emergency shutdown
    logging.critical("EMERGENCY SHUTDOWN triggered by owner")
    os._exit(1)

@bot.tree.command(name="maintenance", description="Toggle maintenance mode (Owner only)")
async def maintenance_command(interaction: discord.Interaction):
    if not bot.security.is_owner(interaction.user.id):
        await interaction.response.send_message("❌ Owner only command!", ephemeral=True)
        return
    
    maintenance_status = "🔧 MAINTENANCE MODE - Bot temporarily unavailable"
    
    await bot.change_presence(activity=discord.Game(name=maintenance_status))
    
    embed = discord.Embed(
        title="🔧 Maintenance Mode",
        description="Bot is now in maintenance mode",
        color=0xff9900
    )
    await interaction.response.send_message(embed=embed, ephemeral=True)

# =================================
# ALL YOUR ORIGINAL COMMANDS
# =================================

@bot.tree.command(name="serverinfo", description="Display detailed information about the current server")
async def serverinfo_slash(interaction: discord.Interaction):
    guild = interaction.guild
    embed = discord.Embed(
        title=f"🏠 Server Info - {guild.name}",
        color=0x0099ff
    )
    embed.set_thumbnail(url=guild.icon.url if guild.icon else None)
    embed.add_field(name="👑 Owner", value=guild.owner.mention, inline=True)
    embed.add_field(name="👥 Members", value=guild.member_count, inline=True)
    embed.add_field(name="📁 Channels", value=len(guild.channels), inline=True)
    embed.add_field(name="🎭 Roles", value=len(guild.roles), inline=True)
    embed.add_field(name="😊 Emojis", value=len(guild.emojis), inline=True)
    embed.add_field(name="🔗 Server ID", value=guild.id, inline=True)
    embed.add_field(name="📅 Created", value=guild.created_at.strftime("%B %d, %Y"), inline=False)
    
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="userinfo", description="Display information about a user")
@app_commands.describe(member="The user to get information about (leave empty for yourself)")
async def userinfo_slash(interaction: discord.Interaction, member: discord.Member = None):
    if member is None:
        member = interaction.user
    
    embed = discord.Embed(
        title=f"👤 User Info - {member.display_name}",
        color=member.color
    )
    embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
    embed.add_field(name="🏷️ Username", value=f"{member.name}#{member.discriminator}", inline=True)
    embed.add_field(name="🆔 ID", value=member.id, inline=True)
    embed.add_field(name="📱 Status", value=str(member.status).title(), inline=True)
    embed.add_field(name="🤖 Bot", value="Yes" if member.bot else "No", inline=True)
    embed.add_field(name="📅 Joined Server", value=member.joined_at.strftime("%B %d, %Y") if member.joined_at else "Unknown", inline=True)
    embed.add_field(name="📅 Account Created", value=member.created_at.strftime("%B %d, %Y"), inline=True)
    
    roles = [role.name for role in member.roles[1:]]
    embed.add_field(name="🎭 Roles", value=", ".join(roles) if roles else "None", inline=False)
    
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="avatar", description="Display a user's avatar in full size")
@app_commands.describe(member="The user whose avatar you want to see (leave empty for yourself)")
async def avatar_slash(interaction: discord.Interaction, member: discord.Member = None):
    if member is None:
        member = interaction.user
    
    embed = discord.Embed(
        title=f"🖼️ {member.display_name}'s Avatar",
        color=member.color
    )
    embed.set_image(url=member.avatar.url if member.avatar else member.default_avatar.url)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="membercount", description="Show detailed member statistics for the server")
async def membercount_slash(interaction: discord.Interaction):
    guild = interaction.guild
    total_members = guild.member_count
    online_members = len([m for m in guild.members if m.status != discord.Status.offline])
    bots = len([m for m in guild.members if m.bot])
    humans = total_members - bots
    
    embed = discord.Embed(
        title="📊 Member Statistics",
        color=0x0099ff
    )
    embed.add_field(name="👥 Total Members", value=total_members, inline=True)
    embed.add_field(name="🟢 Online", value=online_members, inline=True)
    embed.add_field(name="👤 Humans", value=humans, inline=True)
    embed.add_field(name="🤖 Bots", value=bots, inline=True)
    
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="channelinfo", description="Get information about a channel")
@app_commands.describe(channel="The channel to get information about (leave empty for current channel)")
async def channelinfo_slash(interaction: discord.Interaction, channel: discord.TextChannel = None):
    if channel is None:
        channel = interaction.channel
    
    embed = discord.Embed(
        title=f"📁 Channel Info - #{channel.name}",
        color=0x0099ff
    )
    embed.add_field(name="🆔 ID", value=channel.id, inline=True)
    embed.add_field(name="📅 Created", value=channel.created_at.strftime("%B %d, %Y"), inline=True)
    embed.add_field(name="📝 Topic", value=channel.topic or "No topic set", inline=False)
    embed.add_field(name="🔞 NSFW", value="Yes" if channel.is_nsfw() else "No", inline=True)
    embed.add_field(name="👥 Members", value=len(channel.members), inline=True)
    
    await interaction.response.send_message(embed=embed)

# =================================
# MODERATION SLASH COMMANDS
# =================================

@bot.tree.command(name="kick", description="Kick a member from the server")
@app_commands.describe(
    member="The member to kick",
    reason="Reason for the kick"
)
@app_commands.default_permissions(kick_members=True)
async def kick_slash(interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided"):
    if member == interaction.user:
        await interaction.response.send_message("❌ You cannot kick yourself!", ephemeral=True)
        return
    
    try:
        await member.kick(reason=reason)
        embed = discord.Embed(
            title="👢 Member Kicked",
            description=f"{member.mention} has been kicked.\n**Reason:** {reason}",
            color=0xff9900
        )
        embed.add_field(name="Moderator", value=interaction.user.mention, inline=True)
        await interaction.response.send_message(embed=embed)
    except discord.Forbidden:
        await interaction.response.send_message("❌ I don't have permission to kick this member!", ephemeral=True)

@bot.tree.command(name="ban", description="Ban a member from the server")
@app_commands.describe(
    member="The member to ban",
    reason="Reason for the ban"
)
@app_commands.default_permissions(ban_members=True)
async def ban_slash(interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided"):
    if member == interaction.user:
        await interaction.response.send_message("❌ You cannot ban yourself!", ephemeral=True)
        return
    
    try:
        await member.ban(reason=reason)
        embed = discord.Embed(
            title="🔨 Member Banned",
            description=f"{member.mention} has been banned.\n**Reason:** {reason}",
            color=0xff0000
        )
        embed.add_field(name="Moderator", value=interaction.user.mention, inline=True)
        await interaction.response.send_message(embed=embed)
    except discord.Forbidden:
        await interaction.response.send_message("❌ I don't have permission to ban this member!", ephemeral=True)

@bot.tree.command(name="unban", description="Unban a user from the server")
@app_commands.describe(user_id="The ID of the user to unban")
@app_commands.default_permissions(ban_members=True)
async def unban_slash(interaction: discord.Interaction, user_id: str):
    try:
        user = await bot.fetch_user(int(user_id))
        await interaction.guild.unban(user)
        embed = discord.Embed(
            title="✅ Member Unbanned",
            description=f"{user.mention} has been unbanned.",
            color=0x00ff00
        )
        await interaction.response.send_message(embed=embed)
    except ValueError:
        await interaction.response.send_message("❌ Invalid user ID!", ephemeral=True)
    except discord.NotFound:
        await interaction.response.send_message("❌ User not found in ban list!", ephemeral=True)
    except discord.Forbidden:
        await interaction.response.send_message("❌ I don't have permission to unban users!", ephemeral=True)

@bot.tree.command(name="purge", description="Delete multiple messages at once")
@app_commands.describe(amount="Number of messages to delete (1-100)")
@app_commands.default_permissions(manage_messages=True)
async def purge_slash(interaction: discord.Interaction, amount: int):
    if amount < 1 or amount > 100:
        await interaction.response.send_message("❌ Please specify a number between 1 and 100!", ephemeral=True)
        return
    
    try:
        await interaction.response.defer(ephemeral=True)
        deleted = await interaction.channel.purge(limit=amount)
        
        embed = discord.Embed(
            title="🧹 Messages Purged",
            description=f"Successfully deleted {len(deleted)} messages",
            color=0x00ff00
        )
        await interaction.followup.send(embed=embed, ephemeral=True)
    except discord.Forbidden:
        await interaction.followup.send("❌ I don't have permission to delete messages!", ephemeral=True)

@bot.tree.command(name="mute", description="Mute a member so they cannot type")
@app_commands.describe(
    member="The member to mute",
    reason="Reason for the mute"
)
@app_commands.default_permissions(manage_roles=True)
async def mute_slash(interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided"):
    muted_role = discord.utils.get(interaction.guild.roles, name="Muted")
    if not muted_role:
        await interaction.response.send_message("❌ No 'Muted' role found! Please create one first.", ephemeral=True)
        return
    
    try:
        await member.add_roles(muted_role, reason=reason)
        embed = discord.Embed(
            title="🔇 Member Muted",
            description=f"{member.mention} has been muted.\n**Reason:** {reason}",
            color=0xff9900
        )
        embed.add_field(name="Moderator", value=interaction.user.mention, inline=True)
        await interaction.response.send_message(embed=embed)
    except discord.Forbidden:
        await interaction.response.send_message("❌ I don't have permission to mute this member!", ephemeral=True)

@bot.tree.command(name="unmute", description="Unmute a member")
@app_commands.describe(member="The member to unmute")
@app_commands.default_permissions(manage_roles=True)
async def unmute_slash(interaction: discord.Interaction, member: discord.Member):
    muted_role = discord.utils.get(interaction.guild.roles, name="Muted")
    if not muted_role:
        await interaction.response.send_message("❌ No 'Muted' role found!", ephemeral=True)
        return
    
    try:
        await member.remove_roles(muted_role)
        embed = discord.Embed(
            title="🔊 Member Unmuted",
            description=f"{member.mention} has been unmuted.",
            color=0x00ff00
        )
        await interaction.response.send_message(embed=embed)
    except discord.Forbidden:
        await interaction.response.send_message("❌ I don't have permission to unmute this member!", ephemeral=True)

@bot.tree.command(name="warn", description="Issue a warning to a member")
@app_commands.describe(
    member="The member to warn",
    reason="Reason for the warning"
)
@app_commands.default_permissions(manage_messages=True)
async def warn_slash(interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided"):
    embed = discord.Embed(
        title="⚠️ Warning Issued",
        description=f"{member.mention} has been warned.\n**Reason:** {reason}",
        color=0xffff00
    )
    embed.add_field(name="Moderator", value=interaction.user.mention, inline=True)
    await interaction.response.send_message(embed=embed)
    
    # Send DM to warned user
    try:
        dm_embed = discord.Embed(
            title="⚠️ You have been warned",
            description=f"**Server:** {interaction.guild.name}\n**Reason:** {reason}\n**Moderator:** {interaction.user}",
            color=0xffff00
        )
        await member.send(embed=dm_embed)
    except:
        pass

# =================================
# TIME SLASH COMMANDS
# =================================

@bot.tree.command(name="time", description="Get the current time in UTC or a specific timezone")
@app_commands.describe(timezone_name="Timezone (e.g., US/Eastern, Europe/London)")
async def time_slash(interaction: discord.Interaction, timezone_name: str = None):
    if timezone_name:
        try:
            tz = pytz.timezone(timezone_name)
            time = datetime.now(tz)
            tz_display = timezone_name
        except:
            await interaction.response.send_message("❌ Invalid timezone! Use format like 'US/Eastern' or 'Europe/London'", ephemeral=True)
            return
    else:
        time = datetime.now(timezone.utc)
        tz_display = "UTC"
    
    embed = discord.Embed(
        title="🕒 Current Time",
        description=f"**{tz_display}:** {time.strftime('%Y-%m-%d %H:%M:%S')}",
        color=0x87ceeb
    )
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="date", description="Get the current date and time information")
async def date_slash(interaction: discord.Interaction):
    now = datetime.now(timezone.utc)
    embed = discord.Embed(
        title="📅 Current Date (UTC)",
        description=f"**Date:** {now.strftime('%Y-%m-%d')}\n**Time:** {now.strftime('%H:%M:%S')}\n**Day:** {now.strftime('%A')}\n**Month:** {now.strftime('%B')}",
        color=0x9932cc
    )
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="timezone", description="Show common timezones with current times")
async def timezone_slash(interaction: discord.Interaction):
    timezones = {
        "UTC": "UTC",
        "Eastern": "US/Eastern",
        "Central": "US/Central", 
        "Mountain": "US/Mountain",
        "Pacific": "US/Pacific",
        "London": "Europe/London",
        "Paris": "Europe/Paris",
        "Tokyo": "Asia/Tokyo",
        "Sydney": "Australia/Sydney"
    }
    
    embed = discord.Embed(title="🌍 Common Timezones", color=0x0099ff)
    for name, tz in timezones.items():
        try:
            time = datetime.now(pytz.timezone(tz))
            embed.add_field(
                name=name,
                value=f"`{tz}`\n{time.strftime('%H:%M')}",
                inline=True
            )
        except:
            pass
    
    embed.set_footer(text="Use /time [timezone] to get specific time")
    await interaction.response.send_message(embed=embed)

# =================================
# MATH SLASH COMMANDS
# =================================

@bot.tree.command(name="calc", description="Calculate a mathematical expression")
@app_commands.describe(expression="Mathematical expression to calculate (use * for multiply, ** for power)")
async def calc_slash(interaction: discord.Interaction, expression: str):
    try:
        # Remove spaces and validate
        expression = expression.replace(' ', '')
        
        # Only allow certain characters for security
        allowed_chars = set('0123456789+-*/().')
        if not all(c in allowed_chars for c in expression):
            await interaction.response.send_message("❌ Invalid characters in expression! Only use numbers, +, -, *, /, (, ), .", ephemeral=True)
            return
        
        # Evaluate safely
        result = eval(expression)
        
        embed = discord.Embed(
            title="🧮 Calculator",
            description=f"**Expression:** `{expression}`\n**Result:** `{result}`",
            color=0x0099ff
        )
        await interaction.response.send_message(embed=embed)
        
    except ZeroDivisionError:
        await interaction.response.send_message("❌ Cannot divide by zero!", ephemeral=True)
    except:
        await interaction.response.send_message("❌ Invalid mathematical expression!", ephemeral=True)

@bot.tree.command(name="random", description="Generate a random number between min and max")
@app_commands.describe(
    minimum="Minimum number (default: 1)",
    maximum="Maximum number (default: 100)"
)
async def random_slash(interaction: discord.Interaction, minimum: int = 1, maximum: int = 100):
    if minimum >= maximum:
        await interaction.response.send_message("❌ Minimum number must be less than maximum!", ephemeral=True)
        return
    
    if maximum - minimum > 1000000:
        await interaction.response.send_message("❌ Range too large! Maximum range is 1,000,000", ephemeral=True)
        return
    
    result = random.randint(minimum, maximum)
    embed = discord.Embed(
        title="🎲 Random Number",
        description=f"Random number between **{minimum:,}** and **{maximum:,}**:\n**{result:,}**",
        color=0x9932cc
    )
    await interaction.response.send_message(embed=embed)

# =================================
# MESSAGING SLASH COMMANDS
# =================================

@bot.tree.command(name="send", description="Send a message to a specific channel")
@app_commands.describe(
    channel="The channel to send the message to",
    message="The message to send"
)
@app_commands.default_permissions(manage_messages=True)
async def send_slash(interaction: discord.Interaction, channel: discord.TextChannel, message: str):
    try:
        await channel.send(message)
        
        embed = discord.Embed(
            title="📤 Message Sent",
            description=f"Message sent to {channel.mention}",
            color=0x00ff00
        )
        embed.add_field(name="Channel", value=f"#{channel.name}", inline=True)
        embed.add_field(name="Message", value=message[:100] + "..." if len(message) > 100 else message, inline=False)
        embed.set_footer(text=f"Sent by {interaction.user.display_name}")
        
        await interaction.response.send_message(embed=embed, ephemeral=True)
        
    except discord.Forbidden:
        await interaction.response.send_message("❌ I don't have permission to send messages in that channel!", ephemeral=True)

@bot.tree.command(name="sendembed", description="Send an embed message to a specific channel")
@app_commands.describe(
    channel="The channel to send the embed to",
    title="Title of the embed",
    description="Description/content of the embed"
)
@app_commands.default_permissions(manage_messages=True)
async def sendembed_slash(interaction: discord.Interaction, channel: discord.TextChannel, title: str, description: str):
    try:
        embed = discord.Embed(
            title=title,
            description=description,
            color=0x0099ff
        )
        embed.set_footer(text=f"Sent by {interaction.user.display_name}")
        embed.timestamp = datetime.now(timezone.utc)
        
        await channel.send(embed=embed)
        
        confirm_embed = discord.Embed(
            title="📤 Embed Sent",
            description=f"Embed message sent to {channel.mention}",
            color=0x00ff00
        )
        confirm_embed.add_field(name="Channel", value=f"#{channel.name}", inline=True)
        confirm_embed.add_field(name="Title", value=title, inline=True)
        
        await interaction.response.send_message(embed=confirm_embed, ephemeral=True)
        
    except discord.Forbidden:
        await interaction.response.send_message("❌ I don't have permission to send messages in that channel!", ephemeral=True)

@bot.tree.command(name="announce", description="Send an announcement to a specific channel")
@app_commands.describe(
    channel="The channel to send the announcement to",
    message="The announcement message"
)
@app_commands.default_permissions(administrator=True)
async def announce_slash(interaction: discord.Interaction, channel: discord.TextChannel, message: str):
    try:
        embed = discord.Embed(
            title="📢 Announcement",
            description=message,
            color=0xff6600
        )
        embed.set_footer(text=f"Announcement by {interaction.user.display_name}")
        embed.timestamp = datetime.now(timezone.utc)
        
        await channel.send("@everyone", embed=embed)
        
        confirm_embed = discord.Embed(
            title="📢 Announcement Sent",
            description=f"Announcement sent to {channel.mention}",
            color=0x00ff00
        )
        await interaction.response.send_message(embed=confirm_embed, ephemeral=True)
        
    except discord.Forbidden:
        await interaction.response.send_message("❌ I don't have permission to send messages in that channel!", ephemeral=True)

@bot.tree.command(name="say", description="Make the bot say something")
@app_commands.describe(message="The message for the bot to say")
async def say_slash(interaction: discord.Interaction, message: str):
    await interaction.response.send_message(message)

@bot.tree.command(name="test", description="Test if the bot is working properly")
async def test_slash(interaction: discord.Interaction):
    embed = discord.Embed(
        title="✅ Bot Test",
        description="All systems working! Ultimate secure bot is active.",
        color=0x00ff00
    )
    embed.add_field(name="User", value=interaction.user.mention, inline=True)
    embed.add_field(name="Server", value=interaction.guild.name, inline=True)
    embed.add_field(name="Environment", value=bot.security.environment.title(), inline=True)
    embed.add_field(name="Security", value="🔒 Enabled", inline=True)
    embed.add_field(name="Logging", value="📋 Available", inline=True)
    embed.add_field(name="Time", value=datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S'), inline=True)
    await interaction.response.send_message(embed=embed)

# =================================
# SECURE BOT STARTUP
# =================================

def main():
    """Secure bot startup"""
    try:
        logging.info("Starting Ultimate Secure Discord bot...")
        
        # Validate environment
        if security.environment == 'production':
            logging.info("Production mode: Enhanced security active")
        
        # Start bot
        bot.run(security.token)
        
    except SecurityError as e:
        logging.critical(f"Security error: {e}")
        return 1
    except discord.LoginFailure:
        logging.critical("Invalid bot token! Check your .env file.")
        return 1
    except KeyboardInterrupt:
        logging.info("Bot shutdown by user")
        return 0
    except Exception as e:
        logging.critical(f"Critical error: {e}")
        return 1

if __name__ == "__main__":
    exit(main())