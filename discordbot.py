import scrapepages
import discord
from discord.ext import tasks
import markov_chain as mchain
import responses
import random
from mememaker import meme
import os

# Discord info
TOKEN = os.environ.get('disc_token')


class MyClient(discord.Client):

    client = discord.Client()

    chat_wardens = [
        'its ya boi chaaad warden!!!',
        'im talkin bout that PS QUINTOUPLE!',
        'Xbox SeX?? man that controller look like a DIL DO',
        'Xbox aint got no gameS!!!',
        'https://youtu.be/vyufDxxWIsM',
        'i aint talkin about that wii... shitt... people be talkin about its all... \'new\' n shit',
        'i aint tryna play my games with no DIL DO',
        'Warioware: shove it up yo own ass game NOT IN STOCK',
        'xbox palyers cant do shit except SUCK DICK',
        'sony is true shit',
        'FUCK gears of war, more like TEARS of war. lil bitch ass cryn all the time',
        'True games have some 50 cent in the background.. some fat joe.. some BALLIN',
        'Chad warden wipes his ASS with 600 dollars'
    ]

    async def on_ready(self):
        print('Logged on as', self.user)
        self.checkstock.start()

    @tasks.loop(minutes=1)
    async def checkstock(self):
        channel = client.get_channel(758447405451837482)
        results = scrapepages.scrape_zoolert()
        if len(results) > 0:
            message = ""
            for result in results:
                message = f'{message}\n{result}'
            await channel.send(message)

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return
        elif str(self.user.id) in message.content:
            print(message.content)
            if 'meme' in message.content.lower():
                response = meme() if 'chad' not in message.content.lower() else meme(made_up=True)
                await message.channel.send(response)
            elif 'chad' in message.content.lower():
                sentence = mchain.make_a_sentence(random.choice(responses.chat_wardens).split(" ")[0],
                                                        responses.chat_wardens)
                await message.channel.send(sentence)
            elif 'og' in message.content:
                await message.channel.send(responses.chat_warden_vid)
            else:
                await message.channel.send(random.choice(responses.chat_wardens))


client = MyClient()
client.run(TOKEN)
