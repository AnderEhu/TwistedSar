#!/usr/bin/env python3

from twisted.protocols.basic import LineReceiver
from twisted.internet.protocol import Factory
from twisted.internet import reactor

MAX_USERS = 100
MAX_MSG_LENGTH = 255
MAX_USER_LENGTH = 16
PORT = 8000

class ChatProtocol(LineReceiver):
    def __init__(self, factory):
        self.factory = factory
        self.name = None

    def connectionMade(self):
        #A COMPLETAR

    def connectionLost(self, reason):
        #A COMPLETAR

    def lineReceived(self, line):
        #A COMPLETAR

class ChatFactory(Factory):
    def __init__(self):
        self.users = {}

    def buildProtocol(self, addr):
        return ChatProtocol(self)

if __name__ == "__main__":
	reactor.listenTCP(PORT, ChatFactory())
	reactor.run()
