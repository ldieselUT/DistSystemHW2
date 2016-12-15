#!/usr/bin/env python
import Queue

import pika
import time
import threading
from game import *

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
		print 'existing games :', method.routing_key, body
		if game in self.games:
			currentGame = self.games[self.games.index(game)]
			# process adding ships
			if command == 'PLACE_SHIPS':
				data = params.split('|')
				if len(data) == 6:
					player = data[0]
					currentPlayer = self.players[self.players.index(player)]
					ships = data[1:]
					for ship in ships:
						currentGame.addShip(player, ship)
			elif command == 'BEGIN_BATTLE' and currentGame.owner == params:
				currentGame.startGame()
			elif command == 'ATTACK_PLAYER':
				playerAttacking, playerAttacked, y, x = params.split(';')
				if playerAttacking == currentGame.getPlayerTurn():
					result = currentGame.attackPlayer(playerAttacking,playerAttacked, (y, int(x)))
					self.channel.basic_publish(exchange='running games',
					                           routing_key='%s.%s.%s' % (self.name, currentGame.game_name, playerAttacked),
					                           body='RESULT:'+str(result))



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
		# listen to new game messages, meant for server
		if key == self.name + '.toServer':
			game_name, owner_name = body.split(':')
			# if game not exist
			if game_name not in self.games:
				# create new game and add player to it
				newGame = Game(game_name)
				newGame.addPlayer(owner_name)
				newGame.owner = owner_name
				self.games.append(newGame)
				print 'newgame', method.routing_key, owner_name, game_name
				# send player message that game creation was successful
				self.channel.basic_publish(exchange='join game',
				                           routing_key='%s.%s' % (self.name, owner_name),
				                           body='owner')
				# start a thread to handle game logic
				game_thread = threading.Thread(target=self.gameThread,
				                               args=(game_name,))
				game_thread.start()
			# if game exists
			else:
				# add player to game
				exsistingGame = self.games[self.games.index(game_name)]
				exsistingGame.addPlayer(owner_name)
				# send message to player that joining game was successful
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
		currentGame = self.games[self.games.index(game)]
		# main loop for game
		while not currentGame.isGameOver():
			key_all = '%s.%s.%s' % (self.name, game, 'all')
			gamestate = 'NOT_STARTED|'
			for player in currentGame.players:
				if currentGame.players[player].isReady():
					gamestate += player + ':ready;'
				else:
					gamestate += player + ':not ready;'
			gamestate = gamestate[:-1]
			#print 'gamestate', gamestate, ' key ', key_all
			# game has not started yet
			if currentGame.gameflow == None:
				self.channel.basic_publish(exchange='running games',
				                           routing_key=key_all,
				                           body=gamestate)
			else:
				gamestate = 'GAME_RUNNING|'+currentGame.getPlayerTurn()
				self.channel.basic_publish(exchange='running games',
				                           routing_key=key_all,
				                           body=gamestate)
				for player in currentGame.players.values():
					key_player = '%s.%s.%s' % (self.name, currentGame.game_name, player.name)
					self.channel.basic_publish(exchange='running games',
					                           routing_key=key_player,
					                           body=currentGame.getGameState(player.name))
					#print 'gamestate', gamestate
			time.sleep(0.5)
		self.channel.basic_publish(exchange='running games',
		                           routing_key=key_all,
		                           body='GAME_OVER|Game over!\nWinner : %s' % currentGame.gameflow[0])

#name = raw_input('enter server name\n:>')
server = GameServer('kalle\'s server' , 'localhost')
