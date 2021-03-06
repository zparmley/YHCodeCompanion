#!/usr/bin/python

import sys

from twisted.internet import reactor
from twisted.internet.protocol import Protocol
from twisted.internet.protocol import ClientCreator
from cc_config import home_hostname


class MessageSender(Protocol):

    def sendMessage(self, app, msg):
        self.transport.write("%s %s\r\n" % (app, msg))
        self.transport.loseConnection()

    def connectionLost(self, reason):
        reactor.stop()


def sendMessage(app, message):
    """ Setup TCP connection, send message and disconnect """
    creator = ClientCreator(reactor, MessageSender)
    d = creator.connectTCP(home_hostname, 8080)
    d.addCallback(lambda p: p.sendMessage(app, message))
    reactor.run()


if __name__ == "__main__":
    sendMessage(sys.argv[1], sys.argv[2])
