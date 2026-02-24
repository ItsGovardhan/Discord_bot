from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "Bot is alive!"

def run():
    app.run(host='0.0.0.0', port=8080)

t = Thread(target=run)
t.start()
import discord
from discord.ext import commands
from discord.ui import Button, View

# -----------------------
# CONFIGURATION
# -----------------------
GUILD_ID = 1368538603247894578 # Replace with your server ID
ROLE_NAME = "Dark King"        # Role to assign
THUMBNAIL_URL = "https://i.postimg.cc/kgfRpBtq/tenor.gif"  # Big banner GIF  # Replace with your bot token
BOT_PREFIX = "!"                # Command prefix
# -----------------------

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix=BOT_PREFIX, intents=intents)

# Blox Fruits / Server-specific rules
rules_list = [
    {"emoji": "🟠", "title": "No Account Trading", "description": "Never trade or exchange your Blox Fruits account."},
    {"emoji": "🟠", "title": "No Trading Scams", "description": "Be honest in trades; no fake offers or scams."},
    {"emoji": "🟠", "title": "No Scamming by Pretending YouTuber", "description": "Do not scam others by saying you are a YouTuber."},
    {"emoji": "🟠", "title": "No Abusing Members", "description": "Be polite; no insults or harassment."},
    {"emoji": "🟠", "title": "Respect Staff", "description": "Do not argue or disrespect moderators/admins."},
    {"emoji": "🟠", "title": "No Self-Promotion", "description": "Do not advertise Roblox groups, servers, or YouTube."},
    {"emoji": "🟠", "title": "Play Fair", "description": "No exploits, cheats, or unfair methods in Blox Fruits."},
    {"emoji": "🟠", "title": "Use Correct Channels", "description": "Post in proper channels (chat, trading, questions)."},
    {"emoji": "🟠", "title": "Never Ask for Personal IDs", "description": "No one should ask for Roblox ID or personal info."},
    {"emoji": "🟠", "title": "Follow Discord & Roblox TOS", "description": "Abide by rules of Discord and Roblox."}
]

# Role buttons
class RulesView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="I will obey ✅", style=discord.ButtonStyle.green)
    async def obey(self, interaction: discord.Interaction, button: Button):
        guild = bot.get_guild(GUILD_ID)
        member = guild.get_member(interaction.user.id)
        role = discord.utils.get(guild.roles, name=ROLE_NAME)
        if role not in member.roles:
            await member.add_roles(role)
            await interaction.response.send_message("✅ You have been given the Dark King role!", ephemeral=True)
        else:
            await interaction.response.send_message("✅ You already have the Dark King role!", ephemeral=True)

    @discord.ui.button(label="I will not obey ❌", style=discord.ButtonStyle.red)
    async def not_obey(self, interaction: discord.Interaction, button: Button):
        guild = bot.get_guild(GUILD_ID)
        member = guild.get_member(interaction.user.id)
        role = discord.utils.get(guild.roles, name=ROLE_NAME)
        if role in member.roles:
            await member.remove_roles(role)
            await interaction.response.send_message("❌ Your Dark King role has been removed!", ephemeral=True)
        else:
            await interaction.response.send_message("❌ You don't have the Dark King role!", ephemeral=True)

# Command to send rules step by step
@bot.command()
async def rules(ctx):
    # First panel: big GIF/banner
    start_embed = discord.Embed(
        title="📜 Welcome to the Server Rules!",
        description="**Please read all the rules carefully before accepting the Dark King role.**\n\nFollow them to enjoy the server fully!",
        color=discord.Color.orange()
    )
    start_embed.set_image(url=THUMBNAIL_URL)
    start_embed.set_footer(text="By clicking 'I will obey', you agree to follow all rules!")
    await ctx.send(embed=start_embed)

    # Send each rule as a separate panel
    for i, rule in enumerate(rules_list):
        embed = discord.Embed(
            title=f"{rule['emoji']} {rule['title']}",
            description=rule['description'],
            color=discord.Color.orange()
        )
        # Only last panel has buttons
        if i == len(rules_list) - 1:
            await ctx.send(embed=embed, view=RulesView())
        else:
            await ctx.send(embed=embed)

# Run the bot
bot.run(os.environ["TOKEN"])
