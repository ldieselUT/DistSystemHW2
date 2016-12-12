import snakemq.link
import snakemq.packeter
import snakemq.messaging
import snakemq.message

import threading

import time

class Client:
	def __init__(self,  ident, remote_addr):

		self.CLIENT_IDENT = ident

		self.client_link = snakemq.link.Link()
		self.client_packeter = snakemq.packeter.Packeter(self.client_link)
		self.client_messaging = None

		self.client_link.add_connector((remote_addr, 4000))
		self.client_link.add_connector((remote_addr, 4001))

		self.client_packeter.on_packet_recv.add(self.on_packet)
		# drop after 600 seconds if the message can't be delivered

		self.client_link.on_loop_pass.add(self.main_loop)

		self.client_messaging = snakemq.messaging.Messaging(self.CLIENT_IDENT, "", self.client_packeter)
		self.client_messaging.on_message_recv.add(self.on_recv)



		self.i = 0
		self.lastTime = time.time()

		message = snakemq.message.Message(b"hello" + str(self.i), ttl=600)
		self.client_messaging.send_message("server", message)

		self.client_link.loop()

	# handle messages recieved
	def on_recv(self, conn_id, ident, message):
	    print "recieved message from : ",ident, message.data, conn_id

	def on_sent(self, conn_id, ident, message_uuid):
		print "sendt message to : ", ident, message_uuid, conn_id

	# handle setting up unique idents because snakeMQ does not support duplicate idents
	def on_packet(self, conn_id, packet):
		if "ASSIGN ID:" in packet:
			self.CLIENT_IDENT = packet.split(":")[1]
			print "new ident: ", self.CLIENT_IDENT
			self.client_messaging = snakemq.messaging.Messaging(self.CLIENT_IDENT, "", self.client_packeter)
			self.client_messaging.on_message_recv.add(self.on_recv)


	def main_loop(self):
		if self.client_messaging is not None and time.time()-self.lastTime > 1.0:
			print "sending mess ", self.i
			message = snakemq.message.Message(b"hello" + str(self.i), ttl=600)
			self.client_messaging.send_message("server", message)
			self.i += 1
			self.lastTime = time.time()

client = Client('client', 'localhost')