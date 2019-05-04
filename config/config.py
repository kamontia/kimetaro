import configparser as ConfigParser
import sys
import os

import pysnooper


HEY_MESSAGE1 = ''
KIMETARO_MESSAGE1 = ''
KIMETARO_MESSAGE2 = ''
ADD_ERROR1 = ''
LIST_MESSAGE1 = ''
LIST_ERROR1 = ''
REMOVE_MESSAGE1 = ''
REMOVE_MESSAGE2 = ''


@pysnooper.snoop()
def parse():
    config = ConfigParser.ConfigParser()
    try:
        config.read("config/config.ini")
    except FileNotFoundError as e:
        print(e)
    global HEY_MESSAGE1, KIMETARO_MESSAGE1, KIMETARO_MESSAGE2, \
        ADD_ERROR1, LIST_MESSAGE1, LIST_ERROR1, \
        REMOVE_MESSAGE1, REMOVE_MESSAGE2
    HEY_MESSAGE1 = [e for e in config.get('hey', 'message1').split('\n')]
    KIMETARO_MESSAGE1 = [e for e in config.get(
        'kimetaro', 'message1').split('\n')]
    KIMETARO_MESSAGE2 = [e for e in config.get(
        'kimetaro', 'message2').split('\n')]
    ADD_ERROR1 = [e for e in config.get(
        'add', 'error_message1').split('\n')]
    LIST_MESSAGE1 = [e for e in config.get('list', 'message1').split('\n')]
    LIST_ERROR1 = [e for e in config.get('list', 'error_message1').split('\n')]
    REMOVE_MESSAGE1 = [e for e in config.get('remove', 'message1').split('\n')]
    REMOVE_MESSAGE2 = [e for e in config.get('remove', 'message2').split('\n')]


def display():
    print("@@@ DISPLAY - HEY_MESSAGE1 - @@@")
    for v in HEY_MESSAGE1:
        print(v)


if __name__ == '__main__':
    parse()
    display()
