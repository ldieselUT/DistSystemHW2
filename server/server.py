#!/usr/bin/env python
import Queue

import pika
import time
import threading
from game import *

class GameServer_old:
	def __init__(self, name, host='localhost'):
		self.name = name
		self.players = list()
		self.games = list()
		self.communicationQueue = Queue.Queue()

		connection = pika.BlockingConnection(pika.ConnectionParameters(
				host=host))
		self.channel = connection.channel()

		self.channel.exchange_declare(exchange='game servers',
		                              type='fanout')

		self.channel.exchange_declare(exchange='topic_game',
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

		announceThread = threading.Thread(target=self.serverAnnounce,
		                                       args=(1,))
		announceThread.start()

		self.channel.start_consuming()

	def callback(self, ch, method, properties, body):
		key = method.routing_key
		if key != 'announce_server':
			print(" [x] %r:%r" % (method.routing_key, body))

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
			game_name, player_name = body.split(':')
			if game_name not in self.games:
				newGame = Game(game_name)
				newGame.addPlayer(player_name)
				self.games.append(newGame)

				self.channel.basic_publish(exchange='topic_game',
				                           routing_key='game_info.' + self.name + '.' + player_name,
				                           body='new game:'+game_name)
				newGame.owner = player_name
			else:
				existingGame = self.games[self.games.index(game_name)]
				existingGame.addPlayer(player_name)

				self.channel.basic_publish(exchange='topic_game',
				                           routing_key='game_info.' + self.name + '.' + player_name,
				                           body='existing game:' + game_name)
		elif 'game_command.'+self.name in key:
			game_name = key.split('.')[-1]
			params, command, player_name = body.split(':')
			for game in self.games:
				if game.game_name == game_name:
					if command == 'PLACE_SHIP':
						if game.addShip(player_name, params):
							self.channel.basic_publish(exchange='topic_game',
							                           routing_key='game_info.' + self.name + '.' + player_name,
							                           body='ship added')
							return
						else:
							break
					elif command == 'GET_PLAYFIELD':
						result = game.getGameState(player_name)
						self.channel.basic_publish(exchange='topic_game',
						                           routing_key='game_info.' + self.name + '.' + player_name,
						                           body=result)
						return
					elif command == 'WAIT_FOR_PLAYER':
						for player in game.players:
							if player != player_name:
								self.channel.basic_publish(exchange='topic_game',
								                           routing_key='game_info.' + self.name + '.' + player,
								                           body='new player joined')
						return
					elif command == 'START_GAME':
						self.channel.basic_publish(exchange='topic_game',
						                           routing_key='game_info.' + self.name + '.' + game_name,
						                           body='game start')
						gamethread = threading.Thread(target=self.gameThread,
						                              args=(game_name, ))
						gamethread.start()
						return
					elif command == 'ATTACK_PLAYER':
						player, coords = params.split(';')
						self.communicationQueue.put((player, coords))
						return

			self.channel.basic_publish(exchange='topic_game',
			                           routing_key='game_info.' + self.name + '.' + player_name,
			                           body='error')



	def serverAnnounce(self, interval):
		while True:
			self.channel.basic_publish(exchange='game servers',
		                           routing_key='',
		                           body='Announce server:'+self.name)
			print 'announce server : ', self.name
			time.sleep(interval)

	def gameThread(self, game):
		current_game = self.games[self.games.index(game)]
		while not current_game.isGameOver():
			for player in current_game.players:
				if current_game.players[player].isAlive:
					self.channel.basic_publish(exchange='topic_game',
					                           routing_key='game_info.' + self.name + '.' + player,
					                           body='your turn')
					attackedPlayer, coords = self.communicationQueue.get()
					result = current_game.attackPlayer(attackedPlayer, (coords[:1], int(coords[1:])))
					self.channel.basic_publish(exchange='topic_game',
					                           routing_key='game_info.' + self.name + '.' + attackedPlayer,
					                           body='you were attacked')
					self.channel.basic_publish(exchange='topic_game',
					                           routing_key='game_info.' + self.name + '.' + player,
					                           body=result)
				else:
					self.channel.basic_publish(exchange='topic_game',
					                           routing_key='game_info.' + self.name + '.' + player,
					                           body='you are dead')

class GameServer:
	def __init__(self, name, host='localhost'):
		self.name = name
		self.players = list()
		self.games = list()
		self.communicationQueue = Queue.Queue()

		connection = pika.BlockingConnection(pika.ConnectionParameters(
				host=host))
		self.channel = connection.channel()
		""" declare sending channels """
		self.channel.exchange_declare(exchange='game servers',
		                              type='fanout')

		self.channel.exchange_declare(exchange='join game',
		                              type='topic')

		""" declare reciving channels """
		self.bindExchange(self.channel,             # channel
		                  'new connections',        # exchange name
		                  'topic',                  # type
		                  self.name + '.*.toServer',# topic
		                  self.newConnectionManager)# callback

		self.bindExchange(self.channel,             # channel
		                  'new games',              # exchange name
		                  'topic',                  # type
		                  self.name + '.toServer',  # topic
		                  self.newGameManager)      # callback

		self.bindExchange(self.channel,                     # channel
		                  'running games',                 # exchange name
		                  'topic',                          # type
		                  self.name + '.*' + '.toServer',   # topic <server>.<game>.<direction>
		                  self.existingGameManager)                # callback


		announceThread = threading.Thread(target=self.serverAnnounce,
		                                  args=(1,))
		announceThread.start()

		gameAnnounceThread = threading.Thread(target=self.gameAnnounce,
		                                  args=(1,))
		gameAnnounceThread.start()

		self.channel.start_consuming()

	def existingGameManager(self, ch, method, properties, body):
		command, params = body.split(':')
		server, game, dir = method.routing_key.split('.')
		if game in self.games:
			if command == 'JOIN_GAME':
				pass

	def newConnectionManager(self, ch, method, properties, body):
		server, player_name, server = method.routing_key.split('.')
		if player_name not in self.players:
			self.players.append(player_name)
			self.channel.basic_publish(exchange='new connections',
			                           routing_key='%s.%s.%s' % (self.name, player_name, 'toClient'),
			                           body='accept')
		else:
			print self.players
			self.channel.basic_publish(exchange='new connections',
			                           routing_key='%s.%s.%s' % (self.name, player_name, 'toClient'),
			                           body='deny')
		print 'new connection: ', method.routing_key

	def newGameManager(self, ch, method, properties, body):
		key = method.routing_key
		if key == self.name + '.toServer':
			owner_name, game_name = body.split(':')
			if game_name not in self.games:
				self.games.append(Game(game_name))
				print 'newgame', method.routing_key
				self.channel.basic_publish(exchange='join game',
				                           routing_key='%s.%s' % (self.name, owner_name),
				                           body='owner')
				game_thread = threading.Thread(target=self.gameThread,
				                               args=(game_name,))
				game_thread.start()
			else:
				self.channel.basic_publish(exchange='join game',
				                           routing_key='%s.%s' % (self.name, owner_name),
				                           body='player')

	def bindExchange(self, channel, exchange, type, routing_key, callback):
		channel.exchange_declare(exchange=exchange, type=type)
		result = channel.queue_declare(exclusive=True)
		new_queue = result.method.queue

		channel.queue_bind(exchange=exchange,
		                   queue=new_queue,
		                   routing_key=routing_key)

		channel.basic_consume(callback,
		                      queue=new_queue,
		                      no_ack=True)

	def serverAnnounce(self, interval):
		while True:
			self.channel.basic_publish(exchange='game servers',
		                           routing_key='',
		                           body='Announce server:'+self.name)
			#print 'announce server : ', self.name
			time.sleep(interval)

	def gameAnnounce(self, interval):
		while True:
			if len(self.games):
				games = ''
				for game in self.games:
					games += game.game_name+':'
				self.channel.basic_publish(exchange='new games',
			                           routing_key=self.name,
			                           body=games[:-1])
				#print 'announce server : ', self.name
				time.sleep(interval)

	def gameThread(self, game):
		while True:
			key = '%s.%s.%s' % (self.name, game, 'all')
			gamestate = ''

			for self.games[game]
			gamestate = .
			self.channel.basic_publish(exchange='running games',
			                           routing_key=key,
			                           body=gamestate)
			time.sleep(0.5)
#name = raw_input('enter server name\n:>')
server = GameServer('kalle\'s server' , 'localhost')
