import snakemq.link
import snakemq.packeter
import snakemq.messaging
import snakemq.message

import threading

import time
import Queue

class Client:
	def __init__(self,  ident, remote_addr):

		self.CLIENT_IDENT = "client"

		self.client_link = snakemq.link.Link()
		self.client_packeter = snakemq.packeter.Packeter(self.client_link)
		self.client_messaging = None

		self.client_link.wakeup_poll()

		self.client_link.on_loop_pass.add(self.main_loop)

		self.messageQueue = Queue.Queue()

		self.userThread = threading.Thread(target=self.interactiveThread,
		                                   args=(self.messageQueue,))
		self.userThread.start()

		self.client_messaging =  snakemq.messaging.Messaging('', "", self.client_packeter)
		message = snakemq.message.Message('new user', ttl=1)
		self.client_messaging.send_message('server', message)
		self.client_messaging.on_message_recv.add(self.on_recv)
		self.client_messaging.on_disconnect.add(self.on_disconnect)
		self.client_link.loop()

	def connect(self, server):
		self.client_link.add_connector((server, 4000))

	def sendMessage(self, nickname, target, data):
		self.client_messaging =  snakemq.messaging.Messaging(nickname, "", self.client_packeter)
		message = snakemq.message.Message(data, ttl=1)
		self.client_messaging.send_message(target, message)
		self.client_messaging.on_message_recv.add(self.on_recv)
		self.client_messaging.on_disconnect.add(self.on_disconnect)

	def on_disconnect(self, conn_id, ident):
		self.messageQueue.put('disconnect:'+ident)
		print "disconnect", conn_id, ident

	def on_error(self, conn_id, error):
		print "error ", error , conn_id

	# handle messages recieved
	def on_recv(self, conn_id, ident, message):
	    self.messageQueue.put(conn_id+ident+message.data)
	    print "recieved message from : ",ident, message.data, conn_id

	def main_loop(self):
		pass

	def interactiveThread(self, messageQueue):
		state = 'disconnect'
		while True:
			if state == 'disconnect':
				addr = raw_input("enter address\n:>")
				self.connect(addr)
				while True:
					nickname = raw_input("enter nickname\n:>")
					if nickname == '':
						break
					#self.sendMessage(nickname, 'server', 'add new player:'+nickname)
					result = messageQueue.get()
					print result
					if 'disconnect' not in result:
						print 'connected to ',addr, ' as ', nickname
						state = 'listen'
						break
			elif state == 'listen':
				print "getting game announce"
				games = messageQueue.get()
				raw_input('server announce :%s\n enter to refresh' % games)
				pass
			elif state == 'game':
				pass

client = Client('client', 'localhost')