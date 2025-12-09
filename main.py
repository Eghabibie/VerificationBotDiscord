import discord
import os
from discord.ext import commands
from dotenv import load_dotenv
from discord.ui import Button, View
from keep_alive import keep_alive

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

CHANNEL_TARGET_ID = int(os.getenv('CHANNEL_ID_TARGET'))


ID_ROLE_MEMBER = int(os.getenv('ROLE_ID_MEMBER'))
ID_ROLE_ROBLOX = int(os.getenv('ROLE_ID_ROBLOX'))
ID_ROLE_VALORANT = int(os.getenv('ROLE_ID_VALORANT'))

EMOJI_MEMBER = int(os.getenv('EMOJI_ID_MEMBER'))
EMOJI_ROBLOX = int(os.getenv('EMOJI_ID_ROBLOX'))
EMOJI_VALORANT = int(os.getenv('EMOJI_ID_VALORANT'))


BANNER_URL = os.getenv('LINK_BANNER')
THUMB_URL = os.getenv('LINK_THUMBNAIL')

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

async def toggle_role(interaction, role_id, nama_role):
    role = interaction.guild.get_role(role_id)
    
    if role is None:
        await interaction.response.send_message("❌ Error: Role tidak ditemukan!", ephemeral=True)
        return

    if role in interaction.user.roles:
        await interaction.user.remove_roles(role)
        embed = discord.Embed(description=f"❌ Role **{nama_role}** telah dilepas.", color=discord.Color.red())
        await interaction.response.send_message(embed=embed, ephemeral=True)
    else:
        try:
            await interaction.user.add_roles(role)
            embed = discord.Embed(description=f"✅ Role **{nama_role}** berhasil dipasang!", color=discord.Color.green())
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except discord.Forbidden:
            await interaction.response.send_message("⚠️ Bot kurang sakti! Naikkan role bot di atas role target.", ephemeral=True)

class ModernRoleView(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(discord.ui.Button(
            label="Verifikasi Member",
            style=discord.ButtonStyle.success, 
            custom_id="btn_member",
            emoji=discord.PartialEmoji(name="member", id=EMOJI_MEMBER)
        ))

        self.add_item(discord.ui.Button(
            label="Roblox Player",
            style=discord.ButtonStyle.primary, 
            custom_id="btn_roblox",
            emoji=discord.PartialEmoji(name="roblox", id=EMOJI_ROBLOX)
        ))

        self.add_item(discord.ui.Button(
            label="Valorant Agent",
            style=discord.ButtonStyle.danger, 
            custom_id="btn_valorant",
            emoji=discord.PartialEmoji(name="val", id=EMOJI_VALORANT)
        ))

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        custom_id = interaction.data['custom_id']
        
        if custom_id == "btn_member":
            await toggle_role(interaction, ID_ROLE_MEMBER, "Member Server")
        elif custom_id == "btn_roblox":
            await toggle_role(interaction, ID_ROLE_ROBLOX, "Roblox")
        elif custom_id == "btn_valorant":
            await toggle_role(interaction, ID_ROLE_VALORANT, "Valorant")
            
        return True

@bot.event
async def on_ready():
    print(f'Bot {bot.user.name} sudah online dengan tampilan Modern!')
    bot.add_view(ModernRoleView())

@bot.command()
@commands.has_permissions(administrator=True)
async def setup(ctx):
    target_channel = bot.get_channel(CHANNEL_TARGET_ID)

    if target_channel is None:
        await ctx.send("❌ Error: Channel target tidak ditemukan.")
        return

    embed = discord.Embed(
        title=f"SELAMAT DATANG DI {ctx.guild.name.upper()}!",
        description="NI HAO FINESHYT baru! Silakan ambil role kalian di bawah ini untuk menjadi another fineshyt.",
        color=0x2b2d31
    )
    
    if BANNER_URL:
        embed.set_image(url=BANNER_URL)
    
    if THUMB_URL:
        embed.set_thumbnail(url=THUMB_URL)

    embed.add_field(name="👤 Verification", value="Akses untuk melihat seluruh channel server.", inline=True)
    embed.add_field(name="🎮 Game Roles", value="Membuka channel khusus mabar Roblox & Valorant.", inline=True)
    embed.add_field(name="ℹ️ Info", value="Klik tombol lagi untuk melepas role (Toggle).", inline=False)

    embed.set_footer(text="Bie System • Secure Bot", icon_url=bot.user.avatar.url if bot.user.avatar else None)

    await target_channel.send(embed=embed, view=ModernRoleView())
    await ctx.send(f"Setup GUI terkirim ke {target_channel.mention}")
keep_alive() 
bot.run(TOKEN)
bot.run(TOKEN)