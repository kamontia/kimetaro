# coding: utf-8
import os
import random
from collections import defaultdict
from configparser import ConfigParser

import discord
import pysnooper

# Value initialization
CALLCOMMAND_SUFFIX = ''

# Make client instance
client = discord.Client()

# Notification processing when bot stars
@pysnooper.snoop()
@client.event
async def on_ready():
    print('Logged in')
    print(client.user.id)
    print(client.user.name)
    # Set CALLCOMMAND_SUFFIX
    CALLCOMMAND_LIST = {
        'kimetaro': '',
        'kimetaro-dev1': '-dev1',
        'kimetaro-dev2': '-dev2',
        'kimetaro-dev3': '-dev3'
    }
    if client.user.name in CALLCOMMAND_LIST:
        CALLCOMMAND_SUFFIX = CALLCOMMAND_LIST[client.user.name]
        print("CALLCOMMAND_SUFFIX::" + CALLCOMMAND_SUFFIX)


# Processing when some messages are received
@pysnooper.snoop()
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('/kimetaro' + CALLCOMMAND_SUFFIX):
        reply = 'よし、決めたろうやないか'
        await message.channel.send(reply)

    if message.content.startswith('/hey' + CALLCOMMAND_SUFFIX):
        reply = 'おーきに'
        await message.channel.send(reply)

    if message.content.startswith('/choice' + CALLCOMMAND_SUFFIX):
        reply = 'よーうし、決めたるで〜'
        await message.channel.send(reply)
        reply = 'むむっ、これや！\n'
        await message.channel.send(reply)
        reply = choice(message)
        await message.channel.send(reply)

    if message.content.startswith('/add'):
        if len(LIST[message.channel.id]) >= MAX_ITEMS:
            msg = 'もうリストがいっぱいや！最大 {} 個までしか追加できんで'
            reply = msg.format(MAX_ITEMS)
        else:
            add_item = add(message)
            reply = add_item + ' を追加したで'
        await message.channel.send(reply)

    if message.content.startswith('/list' + CALLCOMMAND_SUFFIX):
        reply = 'リストにあるのはこれやで\n'
        await message.channel.send(reply)
        reply = showList(message)
        await message.channel.send(reply)
        reply = r'`/choice` でワイが1つ決めたるで'
        await message.channel.send(reply)

    if message.content.startswith('/remove' + CALLCOMMAND_SUFFIX):
        remove(message)
        reply = '登録されたリストは削除しといたで'
        await message.channel.send(reply)
        reply = 'また利用してな'
        await message.channel.send(reply)


@pysnooper.snoop()
def add(message):
    item = message.content
    item = item.split(' ')[1:]
    LIST[message.channel.id].append(item[0])
    return item[0]


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
def remove(message):
    LIST[message.channel.id].clear()


@pysnooper.snoop()
def main():
    global ACCESSTOKEN, LIST, MAX_ITEMS

    # Set from environment value if it is defined
    if os.environ.get('ACCESSTOKEN'):
        ACCESSTOKEN = os.environ.get('ACCESSTOKEN')

    if os.environ.get('MAX_ITEMS'):
        MAX_ITEMS = int(os.environ.get('MAX_ITEMS'))
    else:
        MAX_ITEMS = 5  # Default

    # LIST = [[] for i in range(MAX_ITEMS)]
    LIST = defaultdict(list)


if __name__ == "__init__":
    pass

if __name__ == "__main__":
    main()

# Bot start to run
client.run(ACCESSTOKEN)
