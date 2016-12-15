#!/usr/bin/env python
import Queue
from PyQt4 import QtCore
from PyQt4 import QtGui

import pika
import threading

import time

import gui
import sys


class GameClientGui(QtGui.QMainWindow, gui.Ui_Game):
	x_coords = range(1, 11)
	y_coords = ['a', 'b', 'c', 'd', 'e',
	            'f', 'g', 'h', 'i', 'j']

	def __init__(self, parent=None, role='player'):
		super(GameClientGui, self).__init__(parent)
		self.setupUi(self)

		# set up globals
		self.lock = False
		self.restart = False


		# set up comboboxes
		self.x_coordsComboBox.addItems(map(str, self.x_coords))
		self.y_coordsComboBox.addItems(self.y_coords)
		# set up gui stuff

		self.startGameButton.setDisabled(role == 'player')

		font = QtGui.QFont()
		font.setFamily("Courier");
		font.setStyleHint(QtGui.QFont.Monospace);
		font.setFixedPitch(True);
		font.setPointSize(10);

		self.textEdit.setWordWrapMode(QtGui.QTextOption.NoWrap)
		self.textEdit.setFont(font)
		self.textEdit.setReadOnly(True)
		metric = QtGui.QFontMetrics(font)
		self.textEdit.setTabStopWidth(4 * metric.width(' '));

		# set up signals
		self.placeShipsSignal = gui.QtCore.SIGNAL('placeShips')
		self.connect(self, self.placeShipsSignal,
		             self.placeShips)

		self.updateStatusSignal = gui.QtCore.SIGNAL('updateStatus')
		self.connect(self, self.updateStatusSignal,
		             self.updateStatus)

		self.updatePlayersSignal = gui.QtCore.SIGNAL('updatePlayers')
		self.connect(self, self.updatePlayersSignal,
		             self.updatePlayer)

		self.connectionsStatusSignal = gui.QtCore.SIGNAL('connectionStatus')
		self.connect(self, self.connectionsStatusSignal,
		             self.connectionsStatusUpdate)

		# set up buttons
		self.startGameButton.clicked.connect(self.startGame)
		self.attackButton.clicked.connect(self.attack)
		self.leaveGameButton.clicked.connect(self.leaveGame)

	def leaveGame(self):
		parent = self.parent()
		parent.emit(parent.leaveGameSignal)
		self.close()

	def connectionsStatusUpdate(self, message):
		self.connectionsStatus.showMessage(message)

	def attack(self):
		for radio in self.PlayerSelectionBox.findChildren( QtGui.QRadioButton):
			if radio.isChecked():
				playerToAttack = radio.text()
				x = self.x_coordsComboBox.currentText()
				y = self.y_coordsComboBox.currentText()
				self.parent().emit(self.parent().attackPlayerSignal, playerToAttack, y,x)
				return

	def startGame(self):
		parent = self.parent()
		if self.restart:
			parent.emit(parent.restartGameSignal)
		else:
			parent.emit(parent.beginBattleSignal)
		self.startGameButton.setDisabled(True)

	def updateStatus(self, text):
		self.textEdit.setText(text.decode('utf-8'))

	def updatePlayer(self, player):
		if isinstance(player, list):
			for radio in self.PlayerSelectionBox.findChildren(QtGui.QRadioButton):
				if radio.text() not in player:
					radio.setParent(None)

		else:
			for radio in self.PlayerSelectionBox.findChildren( QtGui.QRadioButton):
				if radio.text() == player:
					return
			layout = self.PlayerSelectionBox.layout()
			layout.addWidget(QtGui.QRadioButton(player,self.PlayerSelectionBox))

	def placeShips(self):
		self.lock = True
		try:
			while True:
				text, result = QtGui.QInputDialog.getText(
						self,
						'Place ships',
						'enter name',
						text='Aircraft Carrier;a1;v|Battleship;a3;v|Cruiser;a5;v|Submarine;a7;v|Destroyer;a9;v')
				if result:
					try:
						placement = text.split('|')
						if len(placement) == 5:
							parent = self.parent()
							key = '%s.%s.toServer' % (parent.connectedServer, parent.gameName)
							body = 'PLACE_SHIPS:'+parent.playerName+'|'+text
							self.parent().channel.basic_publish(
									exchange='running games',
		                            routing_key=key,
		                            body=str(body))
							break
					except:
						pass
		except Exception, e:
			print e


class ServerBrowserGui(QtGui.QMainWindow, gui.Ui_Server_browser):
	x_coords = range(1, 11)
	y_coords = ['a', 'b', 'c', 'd', 'e',
	            'f', 'g', 'h', 'i', 'j']

	def __init__(self, host,parent=None):
		super(ServerBrowserGui, self).__init__(parent)
		self.setupUi(self)

		#globals
		self.channel = None
		self.playerName = ''
		self.connectedServer = ''
		self.gameName = ''
		self.host = ''
		self.owner = False

		self.gameWindow = GameClientGui(self)
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

		self.connect(self, gui.QtCore.SIGNAL('publish'),
		             self.publishMessage)

		self.beginBattleSignal = gui.QtCore.SIGNAL('beginBattle' )
		self.connect(self, self.beginBattleSignal,
		             self.beginBattle)

		self.attackPlayerSignal = gui.QtCore.SIGNAL('attackPlayer')
		self.connect(self, self.attackPlayerSignal,
		             self.attackPlayer)

		self.leaveGameSignal = gui.QtCore.SIGNAL('leaveGame')
		self.connect(self, self.leaveGameSignal,
		             self.leaveGame)

		self.restartGameSignal = gui.QtCore.SIGNAL('restartGame')
		self.connect(self, self.restartGameSignal,
		             self.restartGame)

	def restartGame(self):
		key = '%s.%s.toServer' % (self.connectedServer, self.gameName)
		body = 'RESTART_GAME:%s' % self.playerName
		print 'leaving game ', body
		self.publishMessage('running games',
		                    key,
		                    body)

	def leaveGame(self):
		key = '%s.%s.toServer' % (self.connectedServer, self.gameName)
		body = 'LEAVE_GAME:%s' % self.playerName
		print 'leaving game ', body
		self.publishMessage('running games',
		                    key,
		                    body)

	def attackPlayer(self, player, y,x):
		key = '%s.%s.toServer' % (self.connectedServer, self.gameName)
		body = 'ATTACK_PLAYER:%s;%s;%s;%s' % (self.playerName, player, y,x )
		print 'attacking player ', body
		self.publishMessage('running games',
		                    key,
		                    body)

	def beginBattle(self):
		key = '%s.%s.toServer' % (self.connectedServer, self.gameName)
		self.publishMessage('running games',
		                    key,
		                   'BEGIN_BATTLE:' + self.playerName)

	def startGame(self, args):
		print 'starting game', args
		if args == 'owner':
			self.owner = True
			self.gameWindow.startGameButton.setDisabled(False)
		self.gameWindow.show()
		self.hide()

	def joinGame(self):
		try:
			game = self.gamesList.selectedItems()[0].text()
			game = game.split('<')[0]
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
				text, result = QtGui.QInputDialog.getText(self, 'Creating game', 'enter name', text='game')
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
				text, result = QtGui.QInputDialog.getText(self, 'Connecting to '+server, 'enter name', text='name')
				if result:
					self.publishMessage('new connections',
					                    '%s.%s.%s' % (server, text, 'toServer'),
					                    'new connection')
					self.playerName = str(text)
					print str(text)
		except:
			return

	def connectToHost(self):
		self.channel = self.initConnection()
		if self.channel.is_open:
			self.brokerConnectButton.setDisabled(True)
		threading.Thread(target=self.channel.start_consuming).start()

	def initConnection(self):
		self.host = str(self.hostLineEdit.text())

		connection = pika.BlockingConnection(pika.ConnectionParameters(
				host=self.host))
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
		# set up gamestate listener, format <server>.<game>.<direction>
		self.bindExchange(channel, 'running games', 'topic', '*.*.*', self.gameStateManager)
		"""  set up sending channels"""
		# self.channel.exchange_declare(exchange='topic_game',type='topic')

		return channel

	def joinGameManager(self, ch, method, properties, body):
		server, player = method.routing_key.split('.')
		print 'join',method.routing_key, body
		if server == self.connectedServer and player == self.playerName:
			self.emit( gui.QtCore.SIGNAL('startGame'), body)
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
			self.connectedServer = server
		else:
			self.emit(QtCore.SIGNAL('updateStatus'),
			          'error connecting to: %s as %s' % (server, player))
		print 'connected to server ', server, player, direction, body

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

	def updateStatus(self, message):
		self.connectionsStatus.showMessage(message)

	def gameStateManager(self, ch, method, properties, body):
		server, game, target = method.routing_key.split('.')
		# listen to only own game messages
		if server == self.connectedServer and game == self.gameName:
			# 'all' is for status messages about game state
			if target == 'all':
				state, params = body.split('|')
				if state == 'NOT_STARTED':
					players = params.split(';')
					for player in players:
						player_name, status = player.split(':')
						if self.playerName == player_name:
							print 'player status : ', player_name, status
							if status == 'not ready' and not self.gameWindow.lock:
								self.gameWindow.emit(self.gameWindow.placeShipsSignal)
							else:
								self.gameWindow.emit(self.gameWindow.updateStatusSignal, params)
								#self.gameWindow.lock = False
						else:
							self.gameWindow.emit(self.gameWindow.updatePlayersSignal, player_name)
				elif state == 'GAME_OVER':
					self.gameWindow.startGameButton.setEnabled(self.owner)
					self.gameWindow.emit(self.gameWindow.updateStatusSignal, params)
					self.gameWindow.lock = False
					self.gameWindow.restart = True
				elif state == 'GAME_RUNNING':
					turn = params.split(';')[0]
					players = params.split(';')[1:]
					self.gameWindow.emit(self.gameWindow.updatePlayersSignal, players)
					self.gameWindow.attackButton.setEnabled(turn == self.playerName)

			# parse messages only meant for the connected player
			elif target == self.playerName:
				if 'RESULT:' in body:
					self.gameWindow.emit(self.gameWindow.connectionsStatusSignal, body)
				else:
					self.gameWindow.emit(self.gameWindow.updateStatusSignal, body)

def main():
	app = QtGui.QApplication(sys.argv)
	form = ServerBrowserGui('localhost')
	form.show()
	app.exec_()


main()
# client = GameClient('localhost')
