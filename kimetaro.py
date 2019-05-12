# coding: utf-8
import os
import random
import re
from collections import defaultdict
import asyncio

import discord
import pysnooper

from config.config import MessageParser


class Kimetaro(object):
    def __init__(self):
        self.parser = MessageParser()


# Global definition(Workaround)
kimetaro = Kimetaro()
loop = asyncio.get_event_loop()

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

    if message.content.startswith('/hey' + COMMAND_SUFFIX):
        await send_reply(message, random.choice(
            kimetaro.parser.getParameter("HEY_MESSAGE1")[0])[1:-1])

    if message.content.startswith('/kimetaro' + COMMAND_SUFFIX):
        await send_reply(message, random.choice(
            kimetaro.parser.getParameter("KIMETARO_MESSAGE1")[0])[1:-1])
        await send_reply(message, random.choice(
            kimetaro.parser.getParameter("KIMETARO_MESSAGE2")[0])[1:-1])
        await send_reply(message, doKimetaro(message))

    if message.content.startswith('/add'):
        add(message)

    if message.content.startswith('/list' + COMMAND_SUFFIX):
        if len(LIST[message.channel.id]) == 0:
            await send_reply(message, random.choice(
                kimetaro.parser.getParameter("LIST_ERROR1")[0])[1:-1])

        else:

            await send_reply(message, random.choice(
                kimetaro.parser.getParameter("LIST_MESSAGE1")[0])[1:-1])
            message_list = formatList(message)
            for i in message_list:
                sync_send_reply(message, i)
            sync_send_reply(message, r'`/kimetaro` でワイが1つ決めたるで')

    if message.content.startswith('/remove' + COMMAND_SUFFIX):
        remove(message)
        await send_reply(message, random.choice(
            kimetaro.parser.getParameter("REMOVE_MESSAGE1")[0])[1:-1])
        await send_reply(message, random.choice(
            kimetaro.parser.getParameter("REMOVE_MESSAGE2")[0])[1:-1])


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
    # Pick up matched words
    item_list = re.findall(COMPILED_PATTERN, item_toSring)

    if not item_list:
        '''
        Expected pattern:`/add string1 string2`
        '''
        for v in item:
            addItem(message, v)
    else:
        '''
        Expected pattern:`/add "string1" "string2"`
        '''
        for v in item_list:
            # Not to add into list if the length of words is zero
            if len(v) != 0 and re.match(r'^\s*$', v) is None:
                addItem(message, v)
            else:
                break


def addItem(message, item):
    if canAppend(message):
        LIST[message.channel.id].append(item)
        sync_send_reply(message, item + ' を追加したで')

    else:
        sync_send_reply(message, random.choice(
            kimetaro.parser.getParameter("ADD_ERROR1")[0])[1:-1]
            .format(MAX_ITEMS))


@pysnooper.snoop()
def doKimetaro(message):
    random.seed()

    # True: List is empty
    if len(LIST[message.channel.id]) == 0:
        return random.choice(kimetaro.parser.getParameter(
            "KIMETARO_ERROR1")[0])[1:-1]
    else:
        reply = random.choice(LIST.get(message.channel.id))
        emoji = random.choice(
            kimetaro.parser.getParameter("KIMETARO_EMOJI1")[0])[1:-1]
        reply = '{} '.format(emoji) + reply + ' {}'.format(emoji)
        return reply


@pysnooper.snoop()
def formatList(message):
    reply_list = LIST.get(message.channel.id)
    formatted_reply_list = []
    for i, v in enumerate(reply_list):
        formatted_reply_list.append(
            '[{index:2}]. {value}'.format(index=i + 1, value=v))
    return formatted_reply_list


@pysnooper.snoop()
def remove(message):
    LIST[message.channel.id].clear()


@pysnooper.snoop()
async def send_reply(message, reply):
    await message.channel.send(reply)


@pysnooper.snoop()
def sync_send_reply(message, reply):
    asyncio.run_coroutine_threadsafe(send_reply(message, reply), loop)


@pysnooper.snoop()
def canAppend(message):
    if len(LIST[message.channel.id]) < MAX_ITEMS:
        return True
    else:
        return False


@pysnooper.snoop()
def main():
    global ACCESSTOKEN, LIST, MAX_ITEMS

    kimetaro.parser.parse()
    kimetaro.parser.display()

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
