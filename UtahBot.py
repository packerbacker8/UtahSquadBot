#UtahSquadBot by Chandler Waugh

import discord
import datetime
from discord.ext import commands
from discord.ext.commands import Bot
from discord.voice_client import VoiceClient
import asyncio
import pandas as pd
import pandas_datareader.data as web

BOT_TOKEN = "NDA5MTI4MDI4NjM2MTg0NTg3.DcFJbQ.qixPJQJCT1ImpU0uoqwllRVo2eA"

#Client = discord.Client()
startup_extensions = ["Music"]
bot = commands.Bot(command_prefix='$')
banned_words = {'anime', 'weaboo', 'waifu', 'hentai', 'tentacle porn', 'vore'}

@bot.event
async def on_ready():
    print("I am running on " + bot.user.name)
    #await bot.say("I have arrived.")

#events when any message is sent, regardless of command
@bot.event
async def on_message(message):
    # if message.author.name == 'Ighuchiro':
    #     await bot.send_message(message.channel, 'no')
    #     await bot.delete_message(message)
    #     return
    await bot.process_commands(message)
    if bot.user.mentioned_in(message):
        await bot.send_message(message.channel,'<@{}> no u'.format(message.author.id))
    if message.content == "What is the meaning of life?":
        await bot.send_message(message.channel, "42 :b:oi".format(message.author))

    lower_msg = message.content.lower()
    for word in banned_words:
        if word in lower_msg:
            await bot.send_message(message.channel, "<@{}> **Get that trash out of here!**".format(message.author.id))
            await bot.delete_message(message)
            return

    if "Execute Order 66" == message.content:
        await bot.send_message(message.channel, "https://www.youtube.com/watch?v=Ng-QLo2hHn0")
        #bot.play(message.context)
        return

class Main_Commands():
    def __init__(self, bot):
        self.bot = bot


@bot.command(pass_context=True)
async def ping(ctx):
    await bot.say(":ping_pong: Pinged!")

@bot.command(pass_context=True)
@commands.has_role("SUPREME LEADER")
async def change_prefix(ctx, new_prefix):
    bot.command_prefix = new_prefix
    await bot.say("New prefix is '{}'.".format(new_prefix))


@bot.command(pass_context=True)
async def info(ctx, user: discord.Member):
    embed = discord.Embed(title="{}'s info".format(user.name), description="Here's what I could find.", color=0x0000ff)
    embed.add_field(name="Name: ", value=user.name, inline=True)
    embed.add_field(name="Current nickname: ", value=user.nick, inline=True)
    embed.add_field(name="User status: ", value=user.status, inline=True)
    embed.add_field(name="User's top role is: ", value=user.top_role, inline=True)
    embed.add_field(name="User joined at time: ", value=user.joined_at, inline=True)
    embed.set_thumbnail(url=user.avatar_url)
    embed.set_footer(text="https://youtu.be/zgnHF2CwrPs?t=2m22s")
    await bot.say(embed=embed)

@bot.command(pass_context=True)
async def server_info(ctx):
    serv = ctx.message.server
    embed = discord.Embed(name="{}'s info".format(serv.name), description="Here's what I could find for this server.", color=0xff0000)
    embed.set_author(name="Ya boi Chandler Waugh")
    embed.add_field(name="Server name: ", value=serv.name, inline=True)
    embed.add_field(name="Server role count: ", value=len(serv.roles), inline=True)
    role_arr = []
    for role in serv.roles:
        role_arr.append(role.name)
    role_str = ', '.join(role_arr)
    embed.add_field(name="Server roles:", value=role_str, inline=True)
    embed.add_field(name="Member count: ", value=len(serv.members), inline=True)
    embed.set_thumbnail(url=serv.icon_url)
    embed.set_footer(text="https://youtu.be/dQw4w9WgXcQ")
    await bot.say(embed=embed)

@bot.command(pass_context=True)
async def stock(ctx, symbol):
    await bot.say(":mag: Looking for the stock of symbol {}...".format(symbol.upper()))
    end = datetime.datetime.now()
    start_month = end.month
    if end.day - 5 < 1:
        start_month -= 1
    start = datetime.datetime(end.year, start_month, end.day - 5)
    df = web.DataReader(symbol.upper(), 'morningstar', start, end)
    df.reset_index(inplace=True)
    df.set_index("Date", inplace=True)
    df = df.drop("Symbol", axis=1)

    await bot.say(df.head())

@bot.command(pass_context=True)
async def addword(ctx, word):
    if not ctx.message.author.server_permissions.administrator:
        bot.say('you do not have permission to edit filtered words')
        return
    banned_words.add(word)
    await bot.say("Word has been added.")

@bot.command(pass_context=True)
async def removeword(ctx, word):
    if not ctx.message.author.server_permissions.administrator:
        bot.say('you do not have permission to edit filtered words')
        return
    try:
        banned_words.remove(word)
        await bot.say("Word has been removed.")
    except KeyError:
        await bot.say('word was not found in filtered words')


@bot.command(pass_context=True)
async def filteredwords(ctx):
    words = ", ".join(banned_words)
    embed = discord.Embed(name="Filtered Words", description="The following words are banned by this server", color=0xff0000)
    embed.set_author(name="Ya boi Chandler Waugh")
    embed.add_field(name="Words: ", value=words, inline=True)
    embed.set_thumbnail(url=ctx.message.server.icon_url)
    await bot.say(embed=embed)

if __name__ == "__main__":
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc = "{}: {}".format(type(e).__name__, e)
            print("Failed to load extension {}\n{}".format(extension, exc))

bot.run(BOT_TOKEN)
