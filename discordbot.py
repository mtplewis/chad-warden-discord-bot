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
                sentence = mchain.make_a_sentence(random.choice(responses.chat_wardens).split(" ")[0], responses.chat_wardens)
                await message.channel.send(sentence)
            elif 'og' in message.content:
                await message.channel.send(responses.chat_warden_vid)
            else:
                await message.channel.send(random.choice(responses.chat_wardens))


client = MyClient()
client.run(TOKEN)
