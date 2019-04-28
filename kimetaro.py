import discord
from configparser import ConfigParser
import os

# Make client instance
client = discord.Client()

# Notification processing when bot stars
@client.event
async def on_ready():
    print('Logged in')
    print(client.user.id)
    print(client.user.name)

# Processing when some messages are received
@client.event
async def on_message(message):

    if message.author == client.user:
        print(r'It\'s you')
        return

    if message.content.startswith('/kimetaro'):
        reply = 'よし、決めたろうやないか'
        await message.channel.send(reply)

    if message.content.startswith('/hey'):
        reply = 'おーきに'
        await message.channel.send(reply)

def main():
    # Set form configuration file
    parser = ConfigParser(default_section="TOKEN")
    try:
        with open("./config.ini") as k:
            parser.read_file(k)
    except:
        pass

    global ACCESSTOKEN
    ACCESSTOKEN = parser["TOKEN"]["ACCESSTOKEN"]
    print(ACCESSTOKEN)

    # Set from environment value if it is defined
    if os.environ.get('ACCESSTOKEN'):
        ACCESSTOKEN = os.environ.get('ACCESSTOKEN')


if __name__ == "__main__":
    main()

    # Bot start to run
client.run(ACCESSTOKEN)
