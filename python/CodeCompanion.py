# Main app, reads from the DB and arduio, acts accordingly.
import json
import serial
import sqlite3
import time

from CodeCompanionView import CodeCompanionView
from cc_config import device

class MessageHandler:
	def __init__(self, arduino_connection):
		self.arduino = arduino_connection

	def handleMessage(self):
		pass

class TestifyMessageHandler(MessageHandler):
	def handleMessage(self, id, data):
		print "Testify handle message", id, data
		companion = CodeCompanionView()
		companion.id = id
		if data['success'] == False:
			companion.screen = ['Oh nos!  There', 'was a problem!']
			companion.rgb = [0, 0, 255]
			companion.appstate = 3 # Arbitrary, i dont know...
		elif data['pass'] == False:
			companion.screen = ['  !TESTS FAIL!  ', 'simple code, plz']
			companion.rgb = [255, 0, 0]
			companion.appstate = 2
		elif data['pass'] == True:
			companion.screen = ['  *TESTS PASS*  ', ' refactor, plz! ']
			companion.rgb = [0, 255, 0]
			companion.appstate = 1
		self.arduino.write('%s\n' % companion.json)


APPID_MESSAGE_HANDLERS = {
	1: TestifyMessageHandler,
	2: 'gitprecommit',
	3: 'trac',
	4: 'happymaker'
}


def get_arduino_connection(device):
	return serial.Serial(device, 9600, timeout=1)
def get_db_connection():
	db = sqlite3.connect('cc_messages.db')
	return db

if __name__ == "__main__":

	arduino = get_arduino_connection(device)
	time.sleep(5) # wait for arduino to warm-up

	while True:

		db = get_db_connection()
		db_messages = db.execute('select id, appid, data_blob from cc_messages where new=1 order by created')

		for message in db_messages:
			handler = APPID_MESSAGE_HANDLERS.get(message[1], MessageHandler)(arduino)
			handler.handleMessage(message[0], json.loads(message[2]))
			db.execute('update cc_messages set new = 0 where id = %s' % message[0])
			db.commit()

		db.close()
		time.sleep(.1)
