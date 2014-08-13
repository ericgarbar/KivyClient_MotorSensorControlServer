__author__ = 'Eric'

class Message(object):

    def __init__(self, type, data=None):
        self.type = type
        self.data = data

    def __str__(self):
        return "message type: %s, message data: %s" % (self.type, self.data)
