#!/usr/bin/env python
"""
tell.py - Phenny irccat Module
Copyright 2009, Ziling Zhao
"""

import threading

from twisted.internet.protocol import Protocol, Factory
from twisted.internet import reactor

import irc

class Relay(Protocol):
    def dataReceived(self, data):
        """
        Given data, relay to phenny for processing, and then lose connection
        """

        bot = self.factory.phenny
        channel = bot.config.channels[0]
        origin = irc.Origin(bot, channel, "")

        event = "PRIVMSG"

        user = bot.config.admins[0]
        if data.startswith("MSG: "):
            data = data[5:]
            origin.sender = user
        else:
            origin.sender = channel

        bytes = data

        origin.nick = user
        origin.user = user

        origin.host = "localhost"

        self.factory.phenny.dispatch(origin, (bytes, event, channel))
        self.transport.loseConnection()

class RelayFactory(Factory):
    protocol = Relay

    def __init__(self, phenny):
        self.phenny = phenny

def startcat(phenny, input): 
    factory = RelayFactory(phenny)
    reactor.listenTCP(8123, factory, interface="localhost")
    reactor.run()

startcat.event = '366'
startcat.rule = r'(.*)'
startcat.thread = True
startcat.priority = 'low'

if __name__ == '__main__': 
   print __doc__.strip()
