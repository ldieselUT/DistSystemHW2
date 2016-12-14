#!/usr/bin/env python
import Queue
from PyQt4 import QtCore

from PyQt4 import QtGui

import pika
import threading

import time

import gui
import sys


# class GameClient:
# 	def __init__(self, host):
# 		self.servers = list()
# 		self.connected_server = ''
# 		self.player_name = ''
# 		self.game_name = ''
# 		self.isOwner = False
#
# 		self.communicationQueue = Queue.Queue()
#
# 		connection = pika.BlockingConnection(pika.ConnectionParameters(
# 				host=host))
# 		self.channel = connection.channel()
#
# 		self.channel.exchange_declare(exchange='topic_',
# 		                              type='topic')
#
# 		result = self.channel.queue_declare(exclusive=True)
# 		topic_queue = result.method.queue
#
# 		self.channel.queue_bind(exchange='topic_game',
# 		                        queue=topic_queue,
# 		                        routing_key='*')
#
# 		self.channel.queue_bind(exchange='topic_game',
# 		                        queue=topic_queue,
# 		                        routing_key='*.*')
#
# 		self.channel.queue_bind(exchange='topic_game',
# 		                        queue=topic_queue,
# 		                        routing_key='*.*.*')
#
# 		self.channel.basic_consume(self.callback,
# 		                           queue=topic_queue,
# 		                           no_ack=True)
#
# 		self.interactiveThread = threading.Thread(target=self.mainLoop)
# 		self.interactiveThread.start()
#
# 		self.channel.start_consuming()
#
# 	# using single callback to handle all topics to avoid spaghetti code
# 	def callback(self, ch, method, properties, body):
# 		key = method.routing_key
# 		if key == 'announce_server':
# 			server_name = body
# 			if server_name not in self.servers:
# 				self.servers.append(server_name)
# 		elif key == 'accept_connection.' + self.player_name:
# 			server_name = body
# 			self.connected_server = server_name
# 			self.communicationQueue.put(server_name)
# 		elif key == 'reject_connection.' + self.player_name:
# 			self.communicationQueue.put(None)
# 		# handle game info meant for player
# 		elif key == 'game_info.' + self.connected_server + '.' + self.player_name:
# 			data = body
# 			self.communicationQueue.put(data)
# 		elif key == 'game_info.' + self.connected_server + '.' + self.game_name:
# 			data = body
# 			self.communicationQueue.put(data)
# 		if key != 'announce_server':
# 			# print(" [x] %r:%r" % (method.routing_key, body))
# 			pass
#
# 	def connectToServer(self, server, player_name):
# 		self.channel.basic_publish(exchange='topic_game',
# 		                           routing_key='join_server.' + server,
# 		                           body=player_name)
# 		return self.communicationQueue.get()
#
# 	def enterGame(self, game_name):
# 		self.channel.basic_publish(exchange='topic_game',
# 		                           routing_key='join_game.' + self.connected_server,
# 		                           body=game_name + ':' + self.player_name)
# 		return self.communicationQueue.get()
#
# 	def placeShip(self, params):
# 		self.channel.basic_publish(exchange='topic_game',
# 		                           routing_key='game_command.' + self.connected_server + '.' + self.game_name,
# 		                           body=params + ':' + 'PLACE_SHIP' + ':' + self.player_name)
# 		return self.communicationQueue.get()
#
# 	def getPlayField(self):
# 		self.channel.basic_publish(exchange='topic_game',
# 		                           routing_key='game_command.' + self.connected_server + '.' + self.game_name,
# 		                           body='' + ':' + 'GET_PLAYFIELD' + ':' + self.player_name)
# 		return self.communicationQueue.get()
#
# 	def waitForPlayer(self, announce=False):
# 		if announce:
# 			self.channel.basic_publish(exchange='topic_game',
# 			                           routing_key='game_command.' + self.connected_server + '.' + self.game_name,
# 			                           body='' + ':' + 'WAIT_FOR_PLAYER' + ':' + self.player_name)
# 		return self.communicationQueue.get()
#
# 	def startGame(self):
# 		self.channel.basic_publish(exchange='topic_game',
# 		                           routing_key='game_command.' + self.connected_server + '.' + self.game_name,
# 		                           body='' + ':' + 'START_GAME' + ':' + self.player_name)
# 		return self.communicationQueue.get()
#
# 	def attackPlayer(self, player, coords):
# 		self.channel.basic_publish(exchange='topic_game',
# 		                           routing_key='game_command.' + self.connected_server + '.' + self.game_name,
# 		                           body=player + ';' + coords + ':' + 'ATTACK_PLAYER' + ':' + self.player_name)
# 		return self.communicationQueue.get()
#
# 	def mainLoop(self):
# 		state = 'default'
# 		while True:
# 			### default state
# 			if state == 'default':
# 				print 'current servers: \n', self.servers
# 				user = raw_input('ENTER to refresh [server_name:player_name to connect]\n:>')
# 				if user != '':
# 					try:
# 						server_name, player_name = user.split(':')
# 						self.player_name = player_name
# 						result = self.connectToServer(server_name, player_name)
# 						if result is not None:
# 							state = 'connected'
# 					except Exception:
# 						print 'input error'
# 			##############################################
# 			elif state == 'connected':
# 				print 'Connected to server : ', self.connected_server
# 				user = raw_input('ENTER game name to enter [if game does not exist a new game will be created]\n:>')
# 				result = self.enterGame(user)
# 				if 'new game' in result:
# 					self.isOwner = True
# 				print result
# 				self.game_name = result.split(':')[-1]
# 				state = 'place_ships'
# 				pass
# 			elif state == 'place_ships':
# 				ships = 0
# 				print 'Enter location of ships',
# 				while ships < 5:
# 					user = raw_input('[name_of_ship;coordinates;orientation]:>')
# 					result = self.placeShip(user)
# 					if result == 'ship added':
# 						if '|' in user:
# 							ships += len(user.split('|'))
# 						else:
# 							ships += 1
# 				state = 'waiting'
# 				print self.getPlayField()
# 			# self.waitForPlayer(announce=True)
# 			elif state == 'waiting':
# 				if self.isOwner:
# 					while 'n' not in raw_input('Wait for more players? [y/n]\n:>'):
# 						print 'waiting for players'
# 						self.waitForPlayer(announce=True)
# 						print 'new player joined'
# 						print self.getPlayField()
# 					self.startGame()
# 					state = 'in_game'
# 				else:
# 					print 'waiting for owner to start'
# 					while True:
# 						result = self.waitForPlayer()
# 						if result == 'game start':
# 							break
# 						print 'new player joined', result
# 						print self.getPlayField()
# 					state = 'in_game'
# 			elif state == 'in_game':
# 				while True:
# 					print 'game started'
# 					print self.getPlayField()
# 					while True:
# 						while self.communicationQueue.get() != 'your turn':
# 							pass
# 						print self.getPlayField()
# 						user = raw_input('Enter player to attack [player_name;coords]\n:>')
# 						try:
# 							player, coords = user.split(';')
# 							int(coords[1:])
# 							print self.attackPlayer(player, coords)
# 							break
# 						except Exception, e:
# 							print 'input error'
#
# 			else:
# 				state = 'default'

class GameClientGui(QtGui.QMainWindow, gui.Ui_Game):
	x_coords = range(1, 11)
	y_coords = ['a', 'b', 'c', 'd', 'e',
	            'f', 'g', 'h', 'i', 'j']

	def __init__(self, host, server_name ,game_name, player_name , parent=None):
		super(GameClientGui, self).__init__(parent)
		self.setupUi(self)

		# globals
		self.game_name = game_name
		self.player_name = player_name
		self.server_name = server_name

		# set up comboboxes
		self.x_coordsComboBox.addItems(map(str, self.x_coords))
		self.y_coordsComboBox.addItems(self.y_coords)

		self.textEdit.setReadOnly(True)

		self.channel = self.initConnection(host, server_name, game_name, player_name)


	def initConnection(self, host, server_name, game_name, player_name):
		connection = pika.BlockingConnection(pika.ConnectionParameters(
				host=host))
		channel = connection.channel()

		""" set up listening channels"""
		# listen to game state
		self.bindExchange(channel,
		                  'running games',
		                  'topic',
		                  '%s.%s.*' % (server_name, game_name),
		                  self.gameStateManager)

		return channel

	def gameStateManager(self, ch, method, properties, body):
		server, game, target = method.routing_key.split('.')
		if target == 'all':
			if player == 'not ready':
				self.placeShips()
			pass
		elif target == self.player_name:
			pass

	def placeShips(self):
		try:
			while not True:
				text, result = QtGui.QInputDialog.getText(
						self,
						'Place ships',
						'enter name',
						text='Aircraft Carrier;a1;v\nBattleship;a3;v\nCruiser;a5;v\nSubmarine;a7;v\nDestroyer;a9;v')
				if result:
					key= '%s.%s' % ( self.connectedServer, 'toServer')
					self.publishMessage('new games',
					                    key,
					                    str(text)+':'+self.playerName)
					print 'sending game ', text, 'to ',key
					self.gameName = str(text)
		except Exception, e:
			print e
			return

class ServerBrowserGui(QtGui.QMainWindow, gui.Ui_Server_browser):
	x_coords = range(1, 11)
	y_coords = ['a', 'b', 'c', 'd', 'e',
	            'f', 'g', 'h', 'i', 'j']

	def __init__(self, parent=None):
		super(ServerBrowserGui, self).__init__(parent)
		self.setupUi(self)

		#globals
		self.channel = None
		self.playerName = ''
		self.connectedServer = ''
		self.gameName = ''
		#queues

		# button methods
		self.brokerConnectButton.clicked.connect(self.connectToHost)
		self.serverConnectButton.clicked.connect(self.connectToServer)

		self.createGameButton.clicked.connect(self.createGame)
		self.joinGameButton.clicked.connect(self.joinGame)

		#set up signals
		self.connect(self, gui.QtCore.SIGNAL('updateStatus'),
		             self.updateStatus)

		self.connect(self, gui.QtCore.SIGNAL('startGame'),
		             self.startGame)

	def startGame(self, args):
		print 'starting game', args
		gameWindow = GameClientGui(self).show()
		self.hide()

	def joinGame(self):
		try:
			game = self.gamesList.selectedItems()[0].text()
			key = '%s.%s' % (self.connectedServer, 'toServer')
			print game
			if game:
				self.publishMessage('new games',
				                    key,
				                    str(game)+':'+ self.playerName)
				self.gameName = str(game)
		except Exception,e:
			print 'Exceptin:', e
			return

	def createGame(self):
		try:
			if self.connectedServer != '':
				text, result = QtGui.QInputDialog.getText(self, 'Creating game', 'enter name')
				if result:
					key= '%s.%s' % ( self.connectedServer, 'toServer')
					self.publishMessage('new games',
					                    key,
					                    str(text)+':'+self.playerName)
					print 'sending game ', text, 'to ',key
					self.gameName = str(text)
			else:
				print 'pressed cancel'
		except Exception, e:
			print e
			return

	def connectToServer(self):
		try:
			server = self.serverListWidget.selectedItems()[0].text()
			print server
			if server:
				text, result = QtGui.QInputDialog.getText(self, 'Connecting to '+server, 'enter name')
				if result:
					self.publishMessage('new connections',
					                    '%s.%s.%s' % (server, text, 'toServer'),
					                    'new connection')
					print str(text)
		except:
			return

	def connectToHost(self):
		self.channel = self.initConnection()
		if self.channel.is_open:
			self.brokerConnectButton.setDisabled(True)
		threading.Thread(target=self.channel.start_consuming).start()

	def initConnection(self):
		host = str(self.hostLineEdit.text())

		connection = pika.BlockingConnection(pika.ConnectionParameters(
				host=host))
		channel = connection.channel()

		""" set up listening channels"""
		# channel that listens to server announces
		self.bindExchange(channel, 'game servers', 'fanout', '', self.serverManager)
		# channel used for new connection communication, topic format: <server>.<player_name>.<direction>
		self.bindExchange(channel, 'new connections', 'topic', '*.*.toClient', self.newConnectionManager)
		# set up listener for new games
		self.bindExchange(channel, 'new games', 'topic', '*', self.newGameManager)
		# set up listener to join games
		self.bindExchange(channel, 'join game', 'topic', '*.*', self.joinGameManager)
		"""  set up sending channels"""
		# self.channel.exchange_declare(exchange='topic_game',type='topic')

		return channel

	def joinGameManager(self, ch, method, properties, body):
		server, game = method.routing_key.split('.')
		print 'join',method.routing_key, body
		if server == self.connectedServer and game == self.gameName:
			self.emit( gui.QtCore.SIGNAL('startGame'), (server, game))
		pass

	def publishMessage(self, exchange, routing_key, body):
		self.channel.basic_publish(exchange=exchange,
		                           routing_key=routing_key,
		                           body=body)

	def bindExchange(self, channel, exchange, type, routing_key, callback):
		channel.exchange_declare(exchange=exchange, type=type)
		result = channel.queue_declare(exclusive=True)
		new_queue = result.method.queue

		channel.queue_bind( exchange=exchange,
		                    queue=new_queue,
		                    routing_key=routing_key)

		channel.basic_consume(  callback,
		                        queue=new_queue,
		                        no_ack=True)

	def newGameManager(self, ch, method, properties, body):
		server = method.routing_key
		if server == self.connectedServer:
			#print 'new game :', body
			try:
				games = body.split(':')
			except:
				games = [body]
			for game in games:
				exists = False
				for i in range(self.gamesList.count()):
					# print str(self.serverListWidget.item(i).text()), newServer
					if str(self.gamesList.item(i).text()) == game:
						exists = True
				if not exists:
					self.gamesList.addItem(game)

	def newConnectionManager(self, ch, method, properties, body):
		server, player, direction = method.routing_key.split('.')
		if body == 'accept':
			self.emit(QtCore.SIGNAL('updateStatus'),
			          'Connected to: %s as %s' % (server, player))
			self.playerName = player
			self.connectedServer = server
		else:
			self.emit(QtCore.SIGNAL('updateStatus'),
			          'error connecting to: %s as %s' % (server, player))
		print server, player, direction, body

	def serverManager(self, ch, method, properties, body):
		try:
			info, newServer = body.split(':')
			for i in range(self.serverListWidget.count()):
				#print str(self.serverListWidget.item(i).text()), newServer
				if str(self.serverListWidget.item(i).text()) == newServer:
					return
			self.serverListWidget.addItem(newServer)
		except:
			return

	def ClearPlayers(self):
		for item in self.PlayerSelectionBox.children():
			if isinstance(item,QtGui.QRadioButton):
				item.setParent(None)
				#print item

	def updateStatus(self, message):
		self.connectionsStatus.showMessage(message)

def main():
	app = QtGui.QApplication(sys.argv)
	form = ServerBrowserGui()
	form.show()
	app.exec_()


main()
# client = GameClient('localhost')
