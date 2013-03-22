import json
import sqlite3
import time

from twisted.protocols.basic import LineReceiver
from twisted.internet.protocol import Factory
from twisted.internet.endpoints import TCP4ServerEndpoint
from twisted.internet import reactor


APP_APPID_MAP = {
    'TESTIFY': 1,
    # 2: 'gitprecommit',
    # 3: 'trac',
    # 4: 'happymaker'
}

class MessageReceiver(LineReceiver):

    def lineReceived(self, line):
        print "Got a line:", line
        app, message = line.split(' ', 1)

        
        if message == "FAIL":
            data = {'pass': True, 'success': True}
        elif message == "PASS":
            data = {'pass': False, 'success': True}
        else:
            data = {'success': False}

        appid = APP_APPID_MAP[app]
        dbcon = sqlite3.connect('cc_messages.db')
        dbcon.execute(
            'insert into cc_messages (appid, created, data_blob) values (?, ?, ?)', (
                appid, 
                int(time.time()), 
                json.dumps(data)
            ))
        dbcon.commit()


class MessageReceiverFactory(Factory):

    protocol = MessageReceiver

endpoint = TCP4ServerEndpoint(reactor, 8080)
endpoint.listen(MessageReceiverFactory())
reactor.run()