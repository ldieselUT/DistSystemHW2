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
			self.channel.basic_publish(exchange='topic_game',
		                           routing_key='announce_server',
		                           body=self.name)
			#print 'announce server : ', self.name
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

#name = raw_input('enter server name\n:>')
server = GameServer('a', 'localhost')
