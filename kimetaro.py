# coding: utf-8
import os
import random
import re
from collections import defaultdict

import discord
import pysnooper

import config.config as Parser

# Value initialization
COMMAND_SUFFIX = ''
'''
This pattern matches keywords enclosed in double quotes.

ex)
 /add "A" "B"
 -> A and B are added in list
'''
PATTERN = r"(?<=\").*?(?=\")"
COMPILED_PATTERN = re.compile(PATTERN)

# Make client instance
client = discord.Client()

# Notification processing when bot stars
@pysnooper.snoop()
@client.event
async def on_ready():
    print('Logged in')
    print(client.user.id)
    print(client.user.name)
    # Set COMMAND_SUFFIX
    COMMAND_SUFFIX = {
        'kimetaro': '',
        'kimetaro-dev1': '-dev1',
        'kimetaro-dev2': '-dev2',
        'kimetaro-dev3': '-dev3'
    }
    if client.user.name in COMMAND_SUFFIX:
        COMMAND_SUFFIX = COMMAND_SUFFIX[client.user.name]
        print("COMMAND_SUFFIX::" + COMMAND_SUFFIX)


# Processing when some messages are received
@pysnooper.snoop()
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('/kimetaro' + COMMAND_SUFFIX):
        reply = 'よし、決めたろうやないか'
        await message.channel.send(reply)

    if message.content.startswith('/hey' + COMMAND_SUFFIX):
        reply = random.choice(Parser.HEY_MESSAGE1)[1:-1]
        await message.channel.send(reply)

    if message.content.startswith('/kimetaro' + COMMAND_SUFFIX):
        reply = random.choice(Parser.KIMETARO_MESSAGE1)[1:-1]
        await message.channel.send(reply)
        reply = random.choice(Parser.KIMETARO_MESSAGE2)[1:-1]
        await message.channel.send(reply)
        reply = choice(message)
        await message.channel.send(reply)

    if message.content.startswith('/add'):
        if len(LIST[message.channel.id]) >= MAX_ITEMS:
            msg = random.choice(Parser.ADD_ERROR1)[1:-1]
            reply = msg.format(MAX_ITEMS)
        else:
            add_item = add(message)
            for v in add_item:
                if len(v) != 0:
                    reply = v + ' を追加したで'
                    await message.channel.send(reply)

    if message.content.startswith('/list' + COMMAND_SUFFIX):
        if len(LIST[message.channel.id]) == 0:
            reply = random.choice(Parser.LIST_ERROR1)[1:-1]
            await message.channel.send(reply)
        else:
            reply = random.choice(Parser.LIST_MESSAGE1)[1:-1]
            await message.channel.send(reply)
            reply = showList(message)
            await message.channel.send(reply)
            reply = r'`/choice` でワイが1つ決めたるで'
            await message.channel.send(reply)

    if message.content.startswith('/remove' + COMMAND_SUFFIX):
        remove(message)
        reply = random.choice(Parser.REMOVE_MESSAGE1)[1:-1]
        await message.channel.send(reply)
        reply = random.choice(Parser.REMOVE_MESSAGE2)[1:-1]
        await message.channel.send(reply)


@pysnooper.snoop()
def add(message):
    '''
     This method is expected receiving argument as below:
     `/add string1 string2`     : String enclosed in nothing sign
     `/add "string1" "string2"  : String not enclosed in double quotes
    '''
    item = message.content

    item = item.split(' ')[1:]

    # Convert to string type because of using regular expression
    item_toSring = ' '.join(item)
    added_list = []
    # Pick up matched words
    item_list = re.findall(COMPILED_PATTERN, item_toSring)

    if not item_list:
        '''
        Expected pattern:`/add string1 string2`
        '''
        for v in item:
            LIST[message.channel.id].append(v)
            added_list.append(v)
    else:
        '''
        Expected pattern:`/add "string1" "string2"`
        '''
        for v in item_list:
            # Not to add into list if the length of words is zero
            if len(v) != 0 and re.match(r'^\s*$', v) is None:
                LIST[message.channel.id].append(v)
                added_list.append(v)

    return added_list


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
    Parser.parse()

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
