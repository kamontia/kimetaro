import configparser as ConfigParser
from collections import defaultdict
import pysnooper


class MessageParser(object):

    def __init__(self):
        self.Messages = defaultdict(list)
        print(type(self.Messages))

    def parse(self):
        config = ConfigParser.ConfigParser()
        try:
            config.read("config/config.ini")
        except FileNotFoundError as e:
            print(e)

        self.setParameter("HEY_MESSAGE1",  [e for e in config.get(
            'hey', 'message1').split('\n')])
        self.setParameter("KIMETARO_MESSAGE1", [e for e in config.get(
            'kimetaro', 'message1').split('\n')])
        self.setParameter("KIMETARO_MESSAGE2", [e for e in config.get(
            'kimetaro', 'message2').split('\n')])
        self.setParameter("KIMETARO_EMOJI1", [e for e in config.get(
            'kimetaro', 'emoji1').split('\n')])
        self.setParameter("KIMETARO_ERROR1", [e for e in config.get(
            'kimetaro', 'error_message1').split('\n')])
        self.setParameter("ADD_ERROR1", [e for e in config.get(
            'add', 'error_message1').split('\n')])
        self.setParameter("LIST_MESSAGE1", [e for e in config.get(
            'list', 'message1').split('\n')])
        self.setParameter("LIST_ERROR1", [e for e in config.get(
            'list', 'error_message1').split('\n')])
        self.setParameter("REMOVE_MESSAGE1", [e for e in config.get(
            'remove', 'message1').split('\n')])
        self.setParameter("REMOVE_MESSAGE2", [e for e in config.get(
            'remove', 'message2').split('\n')])

    def getParameter(self, key):
        return self.Messages[key]

    def setParameter(self, key, value):
        self.Messages[key].append(value)

    def display(self):
        print(self.Messages)


if __name__ == '__main__':
    parser = MessageParser()
    parser.parse()
    parser.display()
