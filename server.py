#!/usr/bin/env python
import pika
import time
import threading
import game

class Server:
	def __init__(self, host):
		self.enAnnounce = True
		self.games = list()

		connection = pika.BlockingConnection(pika.ConnectionParameters(
				host=host))
		self.channel = connection.channel()

		# set up game announce broadcast
		self.channel.exchange_declare(exchange='game announce',
		                              type='fanout')

		self.channel.exchange_declare(exchange='client communication',
		                              type='direct')

		result = self.channel.queue_declare(exclusive=True)
		queue_name = result.method.queue

		self.channel.queue_bind(exchange='client communication',
		                        queue=queue_name,
		                        routing_key='ADD NAME')

		print(' [*] Waiting for logs. To exit press CTRL+C')

		self.channel.basic_consume(self.clientCallback,
		                           queue=queue_name,
		                           no_ack=True)

		# set up thread to announce new games every 10 seconds
		self.announceThread = threading.Thread(target=self.serverAnnounce,
		                                       args=(10,))
		self.announceThread.start()

		self.channel.start_consuming()

	def clientCallback(self, ch, method, properties, body):
		if method.routing_key == 'ADD GAME':
			if not body in self.games:
				self.games.append(body)

		print method.routing_key
		print ch, method, properties, body
		print '%r' % body

	def serverAnnounce(self, interval):
		while self.enAnnounce:
			self.channel.basic_publish(exchange='game announce',
			                           routing_key='',
			                           body='no games')
			print 'announce : no games'
			time.sleep(interval)


# class GameServer:
# 	routing_keys = ['ADD PLAYER',
# 	                'NEW GAME',
# 	                'JOIN GAME']
# 	def __init__(self, name, host):
# 		"""
# 		Inits a game server that announces it's existance to a rabbitmq broker
# 		:param name: name of game
# 		:type name: str
# 		:param host: location of a rabbitmq broker
# 		:type host: str
# 		"""
# 		# set up a blank
# 		self.name = name
# 		self.channel = self.initConnection(host)
# 		# set up thread to announce the server in 1s intervals
# 		announceThread = threading.Thread(target=self.serverAnnounce,
# 		                                       args=(1,))
# 		announceThread.start()
# 		pass
#
# 	def initConnection(self, host):
# 		connection = pika.BlockingConnection(pika.ConnectionParameters(
# 				host=host))
# 		channel = connection.channel()
# 		# set up channel to announce server to
# 		channel.exchange_declare(exchange='server announce',
# 	                              type='fanout')
#
# 		# set up a channel to accept connections
# 		# check if server with same name already exists
#
# 		channel.exchange_declare(exchange=self.name, type='direct', passive=False)
# 		result = channel.queue_declare(exclusive=True)
#
# 		client_queue = result.method.queue
# 		# set up initial routing keys for communication
# 		for key in self.routing_keys:
# 			channel.queue_bind(exchange=self.name,
# 			                        queue=client_queue,
# 			                        routing_key=key)
#
# 		channel.basic_consume(self.clientCallback,
# 		                           queue=client_queue,
# 		                           no_ack=True)
# 		return channel
#
# 	def serverAnnounce(self, interval):
# 		while True:
# 			self.channel.basic_publish(exchange='server announce',
# 			                           routing_key='',
# 			                           body=self.name)
# 			print 'announce server : ', self.name
# 			time.sleep(interval)
#
# 	def clientCallback(self, ch, method, properties, body):
# 		print 'client Callback'
# 		if method.routing_key == 'ADD Player':
# 			if not body in self.games:
# 				self.games.append(body)

class GameServer:
	def __init__(self, name, host='localhost'):
		self.name = name
		self.players = list()
		self.games = list()

		connection = pika.BlockingConnection(pika.ConnectionParameters(
				host=host))
		self.channel = connection.channel()

		self.channel.exchange_declare(exchange='topic_game',
		                                type='topic')

		result = self.channel.queue_declare(exclusive=True)
		topic_queue = result.method.queue

		self.channel.queue_bind(exchange='topic_game',
		                   queue=topic_queue,
		                   routing_key='*')


		self.channel.basic_consume(self.callback,
		                      queue=topic_queue,
		                      no_ack=True)

		announceThread = threading.Thread(target=self.serverAnnounce,
		                                       args=(1,))
		announceThread.start()

		self.channel.start_consuming()


	def callback(self, ch, method, properties, body):
		key = method.routing_key
		if key == 'join_server.'+self.name:
			player_name = body
			if player_name not in self.players:
				self.players.append(player_name)
				self.channel.basic_publish(exchange='topic_game',
				                           routing_key='accept_connection.' + player_name,
				                           body=self.name)
			else:
				self.channel.basic_publish(exchange='topic_game',
				                           routing_key='reject_connection.'+player_name,
				                           body=self.name)
		elif key == 'join_game.' + self.name:


		#print(" [x] %r:%r" % (method.routing_key, body))

	def serverAnnounce(self, interval):

		while True:
			self.channel.basic_publish(exchange='topic_game',
		                           routing_key='announce_server',
		                           body=self.name)
			print 'announce server : ', self.name
			time.sleep(interval)


name = raw_input('enter server name\n:>')
server = GameServer(name, 'localhost')
