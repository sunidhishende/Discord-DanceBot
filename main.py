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

# Functionality of the bot

@client.event
async def on_message(message):
    if message.content.startswith('Hello'):
        responses= ['Fuck off', 'Bitch seriously, Hello?', 'Umm What are you?', 'You are just a sad child who cannot accept that life is meaningless']
        await message.channel.send(random.choice(responses))
    await client.process_commands(message)


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
    for j in range(0, len(inp), 2):
        result= [inp[j], inp[j+1]]
        await ctx.message.channel.send(' '.join(result))
        

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
        
        voice = get(client.voice_clients, guild=ctx.guild)
        await ctx.channel.send('Beginning round {}'.format(j+1))
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

@client.command(name= 'vote')
async def vote(ctx, *options):
    emb= Embed(Title= "Vote")
    fields=[("Who won?", "\n".join([f"{numbers[idx]} {options[idx]}" for idx in range(len(options)) ]), False)]
    for name, value, inline in fields:
        emb.add_field(name=name, value=value, inline=inline)
    message= await ctx.send(embed=emb)
    for emoji in numbers[: len(options)]:
        await message.add_reaction(emoji)

             

    





# Run the bot on the server
client.run('ODQ1NTM0MTkxMzIwMDM5NDM1.YKiXFA.mi127AeH9jpAg4x9zCb9mhWJ1lE')