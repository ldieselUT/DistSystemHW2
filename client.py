#!/usr/bin/env python
import Queue

import pika
import threading

import time


class Client:
	def __init__(self, host):
		# set up globals
		self.games = 'waiting for sever'
		self.name = ''

		connection = pika.BlockingConnection(pika.ConnectionParameters(
		        host=host))
		self.channel = connection.channel()
		# set up game announce listener
		self.channel.exchange_declare(exchange='game announce',
		                         type='fanout')

		result = self.channel.queue_declare(exclusive=True)
		queue_name = result.method.queue

		self.channel.queue_bind(exchange='game announce',
								queue=queue_name)

		self.channel.basic_consume(self.serverAnnounceConsumer,
		                           queue=queue_name,
		                           no_ack=True)

		# set up communication to server
		self.channel.exchange_declare(exchange='client communication',
		                         type='direct')

		# Set up main interactive thread
		self.interactiveThread = threading.Thread(target=self.mainLoop)
		self.interactiveThread.start()

		self.channel.start_consuming()

	def serverAnnounceConsumer(self,ch, method, properties, body):
		if method.exchange == 'game announce':
			if 'no games' not in body:
				try:
					self.games = body.split(';')
				except Exception, e:
					print 'error parsing games: ', e
					print ch
					print method
					print properties
					print body
					print '%r' % body
			else:
				self.games = body

	def addName(self, name):
		self.channel.basic_publish(exchange='client communication',
		                           routing_key='ADD NAME',
		                           body=name)

	def addGame(self, game):
		self.channel.basic_publish(exchange='client communication',
		                           routing_key='ADD GAME',
		                           body=game)

	def mainLoop(self):
		state = 'default'
		while True:
			if state == 'default':
				print 'current games: \n', self.games
				user = raw_input('\npress ENTER to refresh or type game name to join (entering a new name starts a new game)\n:>')
				if user != '':
					if not user in self.games:
						self.addGame(user)
						state = 'game'
			elif state == 'game':
				pass
			else:
				state = 'default'


# class GameClient:
# 	routing_keys = ['ADD PLAYER',
# 	                'NEW GAME',
# 	                'JOIN GAME']
# 	def __init__(self, host):
# 		self.serversQueue = Queue.Queue()
# 		self.serversQueue.put( dict() )
# 		self.channel = self.initConnection(host)
#
# 		# Set up main interactive thread
# 		self.interactiveThread = threading.Thread(target=self.mainLoop)
# 		self.interactiveThread.start()
#
# 		self.channel.start_consuming()
# 		pass
#
# 	def initConnection(self, host):
# 		connection = pika.BlockingConnection(pika.ConnectionParameters(
# 				host=host))
# 		channel = connection.channel()
#
# 		# check if server announce exchange exists
# 		channel.exchange_declare(exchange='server announce', type='fanout', passive=True)
#
# 		# set up a queue to listen to server announces
# 		result = channel.queue_declare(exclusive=True)
# 		servers_queue = result.method.queue
#
# 		channel.queue_bind(exchange='server announce',
# 								queue=servers_queue)
#
# 		channel.basic_consume(self.serverAnnounceConsumer,
# 		                           queue=servers_queue,
# 		                           no_ack=True)
# 		return channel
#
# 	def serverAnnounceConsumer(self, ch, method, properties, body):
# 		servers = self.serversQueue.get()
# 		if method.exchange == 'server announce':
# 			if body not in servers:
# 				servers[body] = (time.time())
# 		for server in servers.keys():
# 			if time.time() - servers[server] > 10:
# 				servers.pop(server, None)
# 		self.serversQueue.put(servers)
# 		# remove server form list if server has not responded in 10s
#
#
# 	def mainLoop(self):
# 		state = 'default'
# 		while True:
# 			if state == 'default':
# 				servers = self.serversQueue.get()
# 				keys = servers.keys()
# 				self.serversQueue.put(servers)
# 				print 'current servers: \n', keys
# 				user = raw_input('\npress ENTER to refresh or type game name to join (entering a new name starts a new game)\n:>')
# 				if user != '':
# 					if not user in self.games:
# 						self.addGame(user)
# 						state = 'game'
# 			elif state == 'game':
# 				pass
# 			else:
# 				state = 'default'
#
# 	def connectToServer(self, server):
# 		try:
# 			self.channel.exchange_declare(exchange=server,
# 			                              type='direct', passive=True)
# 			result = self.channel.queue_declare(exclusive=True)
# 			servers_queue = result.method.queue
#
# 			self.channel.queue_bind(exchange=server,
# 			                   queue=servers_queue)
#
# 			self.channel.queue_bind(exchange=server,
# 			                        queue=servers_queue,
# 			                        routing_key=key)
#
#
#
# 		except Exception, e:
# 			return e

class GameClient:
	def __init__(self, host):
		self.servers = list()
		self.connected_server = ''
		self.player_name = ''
		self.game_name = ''

		self.communicationQueue = Queue.Queue()

		connection = pika.BlockingConnection(pika.ConnectionParameters(
				host=host))
		self.channel = connection.channel()

		self.channel.exchange_declare(exchange='topic_',
		                         type='topic')

		result = self.channel.queue_declare(exclusive=True)
		topic_queue = result.method.queue

		self.channel.queue_bind(exchange='topic_game',
		                   queue=topic_queue,
		                   routing_key='*')

		self.channel.basic_consume(self.callback,
		                      queue=topic_queue,
		                      no_ack=True)

		self.interactiveThread = threading.Thread(target=self.mainLoop)
		self.interactiveThread.start()

		self.channel.start_consuming()

	# using single callback to handle all topics to avoid spaghetti code
	def callback(self, ch, method, properties, body):
		key = method.routing_key
		if key == 'announce_server':
			server_name = body
			if server_name not in self.servers:
				self.servers.append(server_name)
		elif key == 'accept_connection.'+self.player_name:
			server_name = body
			self.communicationQueue.put(server_name)
		elif key == 'reject_connection.'+self.player_name:
			self.communicationQueue.put(None)
		# handle game info meant for player
		elif key == 'game_info.' + self.connected_server + '.' + self.player_name:
			data = body

		#print(" [x] %r:%r" % (method.routing_key, body))

	def connectToServer(self, server, player_name):
		self.channel.basic_publish(exchange='topic_game',
		                           routing_key='join_server.'+server,
		                           body=player_name)
		return self.communicationQueue.get()

	def enterGame(self, game_name):
		self.channel.basic_publish(exchange='topic_game',
		                           routing_key='join_game.' + self.connected_server,
		                           body=game_name)
		return self.communicationQueue.get()

	def mainLoop(self):
		state = 'default'
		while True:
			if state == 'default':
				print 'current servers: \n', self.servers
				user = raw_input('ENTER to refresh [server_name:player_name to connect]\n:>')
				if user != '':
					try:
						server_name, player_name = user.split(':')
						result = self.connectToServer(server_name, player_name)
						if result is not None:
							state = 'connected'
					except Exception:
						print 'input error'
			elif state == 'connected':
				print 'Connected to server : ', self.connected_server
				user = raw_input('ENTER game name to enter [if game does not exist a new game will be created]\n:>')
				state == 'in_game'
				pass
			elif state == 'in_game':

			else:
				state = 'default'




client = GameClient('localhost')