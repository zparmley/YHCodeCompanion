from twisted.protocols.basic import LineReceiver
from twisted.internet.protocol import Factory
from twisted.internet.endpoints import TCP4ServerEndpoint
from twisted.internet import reactor

from code_companion import CodeCompanion

class MessageReceiver(LineReceiver):

    def lineReceived(self, line):
        print "Got a line:", line
        app, message = line.split(' ', 1)

        if message == "FAIL":
            self.factory.code_companion.set_led_color("red")
        elif message == "PASS":
            self.factory.code_companion.set_led_color("green")
        else:
            self.factory.code_companion.set_led_color("blue")


class MessageReceiverFactory(Factory):
    
    protocol = MessageReceiver

    def startFactory(self):
        self.code_companion = CodeCompanion()

endpoint = TCP4ServerEndpoint(reactor, 8080)
endpoint.listen(MessageReceiverFactory())
reactor.run()

