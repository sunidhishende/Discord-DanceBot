from collections import Counter
from hashlib import sha256
from aiohttp import Payload
from black import target_version_option_callback
import discord
import random
from discord.embeds import Embed
from discord.ext import commands
from discord.reaction import Reaction
from discord.utils import get
from youtube_search import YoutubeSearch
import time
import pafy


# Client = our bot
client= commands.Bot(command_prefix='++')
client.remove_command('help')
intents= discord.Intents.default()
intents.members= True
intents.reactions= True

# Functionality of the bot

@client.event
async def on_ready():
    print('Bot says hi')

@client.event
async def on_message(message):
    if message.author==client.user:
        return
    if message.content.startswith('Hello'):
        responses= ['Hi!', 'How you doin?', 'Hello Friend!', 'Hey There!']
        await message.channel.send(random.choice(responses))
    await client.process_commands(message)

@client.command(name='help')
async def help(ctx):
    embed=discord.Embed(
        title='Bot Commands',
        description='Welcome to the help section. Here are all the commands!',
        color= discord.Colour.green())
    embed.add_field(
        name='++help',
        value='List of all the commands',
        inline='false'
    )
    embed.add_field(
        name='++pair',
        value='Pairs up the given names randomly',
        inline='false'
    )
    embed.add_field(
        name='++join',
        value='Bot joins the voice channel',
        inline='false'
    )
    embed.add_field(
        name='++exit',
        value='Bot exits the voice channel',
        inline='false'
    )
    embed.add_field(
        name='++beginbattle',
        value='Plays the songs mentioned and dance battle starts',
        inline='false'
    )
    embed.add_field(
        name='++vote',
        value='Anonymous voting to decide the winner',
        inline='false'
    )
    await ctx.send(embed=embed)
    

#pair people command

@client.command(name='pair')
async def pair(ctx):
    await ctx.message.channel.send('Type names with space to differentiate them')
    def check(m):
        return m.author.id == ctx.author.id
    response= await client.wait_for('message', check=check)
    resp= response.content
    inp = [(inp) for inp in resp.split(" ")]
    result= []
    random.shuffle(inp)
    if len(inp)%2==0:
        for j in range(0, len(inp), 2):
            result= [inp[j], inp[j+1]]
            await ctx.message.channel.send(' '.join(result))
    if len(inp)%2!=0:
        for j in range(0, len(inp)-1, 2):
            result= [inp[j], inp[j+1]]
            await ctx.message.channel.send(' '.join(result))
        await ctx.message.channel.send(inp[len(inp)-1])
        

#Join command

@client.command(name= 'join')
async def join(ctx):
     if not ctx.message.author.voice:
        await ctx.message.channel.send('You\'re not connected to a voice channel')
        return
     else:
         channel= ctx.message.author.voice.channel
         a=channel
     await channel.connect()

#Exit command

@client.command(name= 'exit')
async def exit(ctx):
        voice_client= ctx.message.guild.voice_client
        await voice_client.disconnect()


#music play command

@client.command(name= 'beginbattle')
async def beginbattle(ctx):

    await ctx.send("Give song names using + to differentiate keywords of same song and space to differentiate the song names")
    def check(m):
        return m.author.id == ctx.author.id
    response= await client.wait_for('message', check=check)
    resp= response.content
    inp = [(inp) for inp in resp.split(" ")]
    playlist=[]
    i=0
    for i in range(0, len(inp), 1):
        results = YoutubeSearch(inp[i],max_results=1).to_dict()
        for result in results:
          url_suffix = result['url_suffix']
          link = "https://www.youtube.com" + url_suffix
          playlist.append(link)
    
    
    for j in range(0, len(playlist),1):
        #await ctx.channel.send('Beginning round {}'.format(j+1))
        voice = get(client.voice_clients, guild=ctx.guild)
        url= pafy.new(playlist[j])
        audio = url.getbestaudio()
        source = discord.FFmpegPCMAudio(audio.url)
        #voice = get(client.voice_clients, guild=ctx.guild)
        voice.play(source)
        time.sleep(20)
        voice.pause()
        time.sleep(3)
        voice.resume()
        time.sleep(20)
        voice.pause()
    await ctx.channel.send('Battle is over')
 

#Voting command

numbers=["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣"]
targetmsgid=''
Dict={}
@client.command(name= 'vote')
async def vote(ctx):
    await ctx.send("Give names to vote on with spaces in between them to distinguish them")
    def check(m):
        return m.author.id == ctx.author.id
    response= await client.wait_for('message', check=check)
    resp= response.content
    inp = [(inp) for inp in resp.split(" ")]
    emb= Embed(Title= "Vote")
    fields=[("Who won?", "\n".join([f"{numbers[idx]} {inp[idx]}" for idx in range(len(inp)) ]), False)]
    for name, value, inline in fields:
        emb.add_field(name=name, value=value, inline=inline)
    message= await ctx.send(embed=emb)
    for emoji in numbers[: len(inp)]:
        await message.add_reaction(emoji)
    targetmsgid=message.id
    time.sleep(5)
    res=Counter(Dict.values())
    max=1
    winner=''
    for key,value in res.items():
        if value>=max:
            max=value
            winner=key
        
    await ctx.send("The winner is "+ winner)


async def on_raw_reaction_add(payload: discord.RawReactionActionEvent):
    userid=payload.user_id
    if payload.message_id==targetmsgid:
        Dict.update(userid='{payload.emoji}')
    targetmsgid.remove(payload.user_id)

        
        
       
        
    
    
    

    





# Run the bot on the server
# client.run(#'Enter your token here')
client.run('ODQ1NTM0MTkxMzIwMDM5NDM1.YKiXFA.JMaT073jsG6mxhjqRhpug-rfZIg')
