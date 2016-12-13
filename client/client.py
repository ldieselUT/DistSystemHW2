#!/usr/bin/env python
import Queue

import pika
import threading

import time


class GameClient:
	def __init__(self, host):
		self.servers = list()
		self.connected_server = ''
		self.player_name = ''
		self.game_name = ''
		self.isOwner = False

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

		self.channel.queue_bind(exchange='topic_game',
		                        queue=topic_queue,
		                        routing_key='*.*')

		self.channel.queue_bind(exchange='topic_game',
		                        queue=topic_queue,
		                        routing_key='*.*.*')

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
		elif key == 'accept_connection.' + self.player_name:
			server_name = body
			self.connected_server = server_name
			self.communicationQueue.put(server_name)
		elif key == 'reject_connection.' + self.player_name:
			self.communicationQueue.put(None)
		# handle game info meant for player
		elif key == 'game_info.' + self.connected_server + '.' + self.player_name:
			data = body
			self.communicationQueue.put(data)
		if key != 'announce_server':
			print(" [x] %r:%r" % (method.routing_key, body))

	def connectToServer(self, server, player_name):
		self.channel.basic_publish(exchange='topic_game',
		                           routing_key='join_server.' + server,
		                           body=player_name)
		return self.communicationQueue.get()

	def enterGame(self, game_name):
		self.channel.basic_publish(exchange='topic_game',
		                           routing_key='join_game.' + self.connected_server,
		                           body=game_name + ':' + self.player_name)
		return self.communicationQueue.get()

	def placeShip(self, params):
		self.channel.basic_publish(exchange='topic_game',
		                           routing_key='game_command.' + self.connected_server + '.' + self.game_name,
		                           body=params + ':' + 'PLACE_SHIP' + ':' + self.player_name)
		return self.communicationQueue.get()

	def getPlayField(self):
		self.channel.basic_publish(exchange='topic_game',
		                           routing_key='game_command.' + self.connected_server + '.' + self.game_name,
		                           body='' + ':' + 'GET_PLAYFIELD' + ':' + self.player_name)
		return self.communicationQueue.get()

	def waitForPlayer(self, announce = False):
		if announce:
			self.channel.basic_publish(exchange='topic_game',
			                           routing_key='game_command.' + self.connected_server + '.' + self.game_name,
			                           body='' + ':' + 'WAIT_FOR_PLAYER' + ':' + self.player_name)
		return self.communicationQueue.get()

	def startGame(self):
		self.channel.basic_publish(exchange='topic_game',
		                           routing_key='game_command.' + self.connected_server + '.' + self.game_name,
		                           body='' + ':' + 'START_GAME' + ':' + self.player_name)
		return self.communicationQueue.get()

	def mainLoop(self):
		state = 'default'
		while True:
			### default state
			if state == 'default':
				print 'current servers: \n', self.servers
				user = raw_input('ENTER to refresh [server_name:player_name to connect]\n:>')
				if user != '':
					try:
						server_name, player_name = user.split(':')
						self.player_name = player_name
						result = self.connectToServer(server_name, player_name)
						if result is not None:
							state = 'connected'
					except Exception:
						print 'input error'
			##############################################
			elif state == 'connected':
				print 'Connected to server : ', self.connected_server
				user = raw_input('ENTER game name to enter [if game does not exist a new game will be created]\n:>')
				result = self.enterGame(user)
				if 'new game' in result:
					self.isOwner = True
				print result
				self.game_name = result.split(':')[-1]
				state = 'place_ships'
				pass
			elif state == 'place_ships':
				ships = 0
				print 'Enter location of ships',
				while ships < 5:
					user = raw_input('[name_of_ship;coordinates;orientation]:>')
					result = self.placeShip(user)
					if result == 'ship added':
						if '|' in user:
							ships += len(user.split('|'))
						else:
							ships += 1
				state = 'waiting'
				print self.getPlayField()
				self.waitForPlayer(announce=True)
			elif state == 'waiting':
				if self.isOwner:
					while 'n' not in raw_input('Wait for more players? [y/n]\n:>'):
						print 'waiting for players'
						self.waitForPlayer(announce=True)
						print 'new player joined'
						print self.getPlayField()
					self.startGame()
					state = 'in_game'
				else:
					print 'waiting for owner to start'
					while self.waitForPlayer() != 'game start':
						print 'new player joined'
						print self.getPlayField()
					state = 'in_game'
			elif state == 'in_game':

				raw_input('TODO: make game happen here')
			else:
				state = 'default'


client = GameClient('localhost')
