import discord
from discord.ext import commands
from discord.ui import Button, View

BOT_PREFIX = "!"
THUMBNAIL_URL = "https://i.postimg.cc/kgfRpBtq/tenor.gif"  # Replace with your GIF

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=BOT_PREFIX, intents=intents)

# -----------------------
# ANNOUNCEMENT COMMAND
# -----------------------
@bot.command()
@commands.has_permissions(administrator=True)
async def announce(ctx, channel: discord.TextChannel = None):
    """
    Sends a formatted phishing/scam warning announcement.
    Usage: !announce #channel
    """
    if channel is None:
        channel = ctx.channel  # Default to current channel

    # Embed setup
    embed = discord.Embed(
        title="⚠️ **Phishing/Scam Alert!** ⚠️",
        description=(
            "Hello Peeps 👋\n\n"
            "There is a **new Phishing Scam method** going around where people may invite you to fake servers. "
            "If you join, your account can get **Hacked!**\n\n"
            "❌ Any kind of **Self Promotion** is **Bannable**.\n"
            "💡 Make a **Ticket** anytime someone promotes their server — it is most likely a **SCAM**!"
        ),
        color=discord.Color.red()
    )
    embed.set_thumbnail(url=THUMBNAIL_URL)
    embed.set_footer(text="Stay safe and never share your account info!")

    # Optional interactive buttons
    class AnnouncementPanel(View):
        def __init__(self):
            super().__init__(timeout=None)

        @discord.ui.button(label="Report Scam 🔍", style=discord.ButtonStyle.red, emoji="🚨")
        async def report(self, interaction: discord.Interaction, button: Button):
            await interaction.response.send_message(
                "Please open a ticket with the moderators immediately! ⚠️", ephemeral=True
            )

        @discord.ui.button(label="More Info ℹ️", style=discord.ButtonStyle.green, emoji="📘")
        async def more_info(self, interaction: discord.Interaction, button: Button):
            await interaction.response.send_message(
                "Always verify the server before joining and never share your password!", ephemeral=True
            )

    # Send the embed with buttons
    await channel.send(embed=embed, view=AnnouncementPanel())
    await ctx.send(f"✅ Announcement sent to {channel.mention}")

# -----------------------
# RUN BOT
# -----------------------
bot.run(os.environ["TOKEN"])
