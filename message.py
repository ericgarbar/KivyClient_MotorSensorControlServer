__author__ = 'Eric'
from collections import namedtuple

from collections import namedtuple

# class Message(namedtuple('Message', ['type', 'data', 'sender_name'])):
#     def __new__(cls, type=None, data=None, sender_name=None):
#         return super(Message, cls).__new__(cls, type, data, sender_name)
#
#     def __str__(self):
#         return "message type: %s\nmessage data: %s" % (self.type, self.data)

class Message(object):

    def __init__(self, type, data=None):
        self.type = type
        self.data = data

    def __str__(self):
        return "message type: %s\nmessage data: %s" % (self.type, self.data)

if __name__ == '__main__':
    print Message('hi', [1,2])
