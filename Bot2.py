import discord
from discord.ext import commands, tasks
import os
import asyncio
from flask import Flask
from threading import Thread
import subprocess
from datetime import timedelta
import json

TOKEN = os.getenv("TOKEN")
PREFIX = "*"

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=PREFIX, intents=intents)

# ================= KEEP ALIVE SERVER =================

app = Flask('')

@app.route('/')
def home():
    return "Bot is alive 24/7!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# ================= PERSISTENT WARNING DATABASE =================

if not os.path.exists("warnings.json"):
    with open("warnings.json", "w") as f:
        json.dump({}, f)

def load_warnings():
    with open("warnings.json", "r") as f:
        return json.load(f)

def save_warnings(data):
    with open("warnings.json", "w") as f:
        json.dump(data, f, indent=4)

# ================= AUTO GITHUB RESTART SYSTEM =================

@tasks.loop(minutes=5)
async def auto_update():
    subprocess.call("git pull", shell=True)
    print("Checked GitHub for updates.")

    # Restart bot if update pulled
    os.system("kill 1")

# ================= WARN SYSTEM (NO RESET EVER) =================

@bot.command()
@commands.has_permissions(manage_messages=True)
async def warn(ctx, member: discord.Member, *, reason="No reason provided"):

    data = load_warnings()

    if str(member.id) not in data:
        data[str(member.id)] = 0

    data[str(member.id)] += 1
    count = data[str(member.id)]
    save_warnings(data)

    if count == 1:
        await ctx.send(f"🟠 {member.mention} has been warned.\nReason: {reason}")

    elif count == 2:
        await member.timeout(timedelta(hours=1))
        await ctx.send(f"🟠 {member.mention} received 2nd warning.\n⏳ Timeout: 1 Hour")

    elif count >= 3:
        await member.timeout(timedelta(days=1))
        await ctx.send(f"🟠 {member.mention} received 3rd warning.\n⏳ Timeout: 1 Day")

# ================= MUTE =================

@bot.command()
@commands.has_permissions(moderate_members=True)
async def mute(ctx, member: discord.Member, minutes: int, *, reason="No reason"):
    await member.timeout(timedelta(minutes=minutes), reason=reason)
    await ctx.send(f"🟠 {member.mention} muted for {minutes} minutes.")

# ================= KICK =================

@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason="No reason"):
    await member.kick(reason=reason)
    await ctx.send(f"🟠 {member} has been kicked.\nReason: {reason}")

# ================= BAN =================

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason="No reason"):
    await member.ban(reason=reason)
    await ctx.send(f"🟠 {member} has been banned.\nReason: {reason}")

# ================= RULES =================

@bot.command()
async def rules(ctx):

    embed = discord.Embed(
        title="🟠 BLOX FRUITS & ROBLOX SERVER RULES",
        color=discord.Color.orange()
    )

    embed.description = """
**🟠 ACCOUNT RULES**
🟠 No buying Roblox accounts  
🟠 No selling Blox Fruits accounts  
🟠 No account exchange or trading  

**🟠 SCAM RULES**
🟠 No scamming or fake giveaways  
🟠 No cross trading Blox Fruits items  

**🟠 BEHAVIOUR RULES**
🟠 No abusing members  
🟠 Respect Discord staff  
🟠 No exploiting or hack discussion  
🟠 No spam or self promotion  
🟠 Use correct channels  
"""

    embed.set_image(url="https://i.postimg.cc/j26gPz3M/tenor.gif")
    embed.set_footer(text="Breaking rules = Warning & Punishment")

    await ctx.send(embed=embed)

# ================= ERROR HANDLER =================

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("🟠 You don't have permission to use this command.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("🟠 Missing arguments. Check command usage.")
    else:
        print(error)

# ================= READY =================

@bot.event
async def on_ready():
    print(f"Bot connected as {bot.user}")
    auto_update.start()

# ================= START =================

keep_alive()
bot.run(TOKEN)
