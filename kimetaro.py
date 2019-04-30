# coding: utf-8
import discord
from configparser import ConfigParser
import os
from collections import defaultdict
import random
import pysnooper

# Make client instance
client = discord.Client()

# Notification processing when bot stars
@pysnooper.snoop()
@client.event
async def on_ready():
    print('Logged in')
    print(client.user.id)
    print(client.user.name)


# Processing when some messages are received
@pysnooper.snoop()
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('/kimetaro'):
        reply = 'よし、決めたろうやないか'
        await message.channel.send(reply)

    if message.content.startswith('/hey'):
        reply = 'おーきに'
        await message.channel.send(reply)

    if message.content.startswith('/choice'):
        reply = 'よーうし、決めたるで〜'
        await message.channel.send(reply)
        reply = 'むむっ、これや！\n'
        await message.channel.send(reply)
        reply = choice(message)
        await message.channel.send(reply)

    if message.content.startswith('/add'):
        add_item = add(message)
        reply = add_item + ' を追加したで'
        await message.channel.send(reply)

    if message.content.startswith('/list'):
        reply = 'リストにあるのはこれやで\n'
        await message.channel.send(reply)
        reply = showList(message)
        await message.channel.send(reply)
        reply = r'`/choice` でワイが1つ決めたるで'
        await message.channel.send(reply)

@pysnooper.snoop()
def add(message):
    item = message.content
    item = item.split(' ')[1]
    LIST[message.channel.id].append(item)
    return item

@pysnooper.snoop()
def choice(message):
    reply = random.choice(LIST.get(message.channel.id))
    return reply

@pysnooper.snoop()
def showList(message):
    print(message.channel.id)
    reply = LIST.get(message.channel.id)
    return reply

@pysnooper.snoop()
def main():
    # Set form configuration file
    parser = ConfigParser(default_section="TOKEN")
    try:
        with open("./config.ini") as k:
            parser.read_file(k)
    except FileNotFoundError as e:
        print(e)
        raise

    global ACCESSTOKEN, LIST, MAX_ITEM
    ACCESSTOKEN = parser["TOKEN"]["ACCESSTOKEN"]
    print(ACCESSTOKEN)

    # Set from environment value if it is defined
    if os.environ.get('ACCESSTOKEN'):
        ACCESSTOKEN = os.environ.get('ACCESSTOKEN')

    MAX_ITEM = 5
    # LIST = [[] for i in range(MAX_ITEM)]
    LIST = defaultdict(list)
    LIST[499200204239667202].append("決めたろうを使う")
    LIST[499200204239667202].append("決めたろうを消す")
    print(LIST)


if __name__ == "__init__":
    pass

if __name__ == "__main__":
    main()

# Bot start to run
client.run(ACCESSTOKEN)
