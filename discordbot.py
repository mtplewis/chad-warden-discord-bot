import scrapepages
import discord
from discord.ext import tasks
import markov_chain as mchain
import responses
import random
from mememaker import meme
import os
import time

# Discord info
TOKEN = os.environ.get('disc_token')


class MyClient(discord.Client):

    client = discord.Client()
    last_messaged = 0

    async def on_ready(self):
        print('Logged on as', self.user)
        self.checkstock.start()
        self.check_headset.start()

    @tasks.loop(minutes=1)
    async def checkstock(self):
        channel = client.get_channel(758447405451837482)
        results = scrapepages.scrape_zoolert()
        if len(results) > 0:
            message = ""
            for result in results:
                message = f'{message}\n{result}'
            if time.time() >= self.last_messaged + 1800:
                self.last_messaged = time.time()
                await channel.send(message)

    @tasks.loop(minutes=10)
    async def check_headset(self):
        channel = client.get_channel(758447405451837482)
        results = scrapepages.scrape_sony_for_headset()
        print(results)
        if len(results['in_stock']) > 0:
            message = ""
            for result in results['in_stock']:
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
                if random.randit(0,99) == 0:
                    sentence = "chad is a thicc ring boi" 
                else:
                    sentence = mchain.make_a_sentence(random.choice(responses.chat_wardens).split(" ")[0], responses.chat_wardens)
                await message.channel.send(sentence)
            elif 'og' in message.content:
                await message.channel.send(responses.chat_warden_vid)
            elif 'check current stock' in message.content.lower():
                out_of_stock = 'Out of Stock: ```'
                in_stock = 'In Stock: ```'
                results = scrapepages.scrape_zoolert(include_all=True)
                if len(results['in_stock']) > 0:
                    for result in results['in_stock']:
                        in_stock = in_stock + '\n' + result
                    in_stock = f'{in_stock}```'
                else:
                    in_stock = in_stock + '\n' + 'None' + '```'
                for result in results['sold_out']:
                    out_of_stock = out_of_stock + '\n' + result
                headset_out_of_stock = 'Out of Stock: ```'
                headset_in_stock = 'In Stock: ```'
                results = scrapepages.scrape_sony_for_headset()
                if len(results['in_stock']) > 0:
                    for result in results['in_stock']:
                        headset_in_stock = headset_in_stock + '\n' + result
                    headset_in_stock = f'{headset_in_stock}```'
                else:
                    headset_in_stock = headset_in_stock + '\n' + 'None' + '```'
                for result in results['sold_out']:
                    headset_out_of_stock = headset_out_of_stock + '\n' + result
                await message.channel.send(f'**PS5 Stock:**')
                await message.channel.send(f'{out_of_stock}```')
                await message.channel.send(in_stock)
                await message.channel.send(f'**Pulse 3D wireless headset stock:**')
                await message.channel.send(f'{headset_out_of_stock}```')
                await message.channel.send(f'{headset_in_stock}')
            else:
                await message.channel.send(random.choice(responses.chat_wardens))


client = MyClient()
client.run(TOKEN)
