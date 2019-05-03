# coding: utf-8
import os
import random
import re
from collections import defaultdict
from configparser import ConfigParser

import discord
import pysnooper

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
        send_reply(message, 'よし、決めたろうやないか')

    if message.content.startswith('/hey' + COMMAND_SUFFIX):
        send_reply(message, 'おーきに')

    if message.content.startswith('/choice' + COMMAND_SUFFIX):
        send_reply(message, 'よーうし、決めたるで〜')
        send_reply(message, 'むむっ、これや！\n')
        send_reply(message, choice(message))

    if message.content.startswith('/add'):
        if len(LIST[message.channel.id]) >= MAX_ITEMS:
            send_reply(message,
                       'もうリストがいっぱいや！最大 {} 個までしか追加できんで'.format(MAX_ITEMS))
        else:
            add_item = add(message)
            for v in add_item:
                if len(v) != 0:
                    send_reply(message, v + ' を追加したで')

    if message.content.startswith('/list' + COMMAND_SUFFIX):
        if len(LIST[message.channel.id]) == 0:
            send_reply(message, r'残念やったな！リストはからっぽや！`/add "タスク"`でタスクを追加できるで')
        else:
            send_reply(message, 'リストにあるのはこれやで\n')
            send_reply(message, showList(message))
            send_reply(message, r'`/choice` でワイが1つ決めたるで')

    if message.content.startswith('/remove' + COMMAND_SUFFIX):
        remove(message)
        send_reply(message, '登録されたリストは削除しといたで')
        send_reply(message, 'また利用してな')


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
async def send_reply(message, reply):
    await message.channel.send(reply)


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
