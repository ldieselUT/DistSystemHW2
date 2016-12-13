import operator


class Game:
	def __init__(self, game_name):
		""" Init Game before game can begin all players need to fill out their playfields
		:param game_name: name of game
		"""
		self.game_name = game_name
		self.players = dict()
		self.winner = None
		self.owner = None

	def addPlayer(self, player):
		""" adds player to dictionary of players in the game, players limited to size of battlefield
		:param player: name of player
		:type player: str
		:returns: if adding player was successful
		:rtype: bool
		"""
		newPlayer = Player(player)
		if not self.players.has_key(player):
			self.players[player] = newPlayer
			return True
		else:
			return False

	def addShip(self, player, params):
		# type: (str, str) -> bool
		try:
			if '|' in params:
				for command in params.split('|'):
					ship, coords, orientation = command.split(';')
					y = coords[:1]
					x = coords[1:]
					currentPlayer = self.players[player]
					field = currentPlayer.playfield
					if not field.addShip(ship, (y, int(x)), orientation):
						return False
				return True
			else:
				ship, coords, orientation = params.split(';')
				y = coords[:1]
				x = coords[1:]
				currentPlayer = self.players[player]
				field = currentPlayer.playfield
				if not field.addShip(ship, (y, int(x)), orientation):
					return False
				return True
		except Exception, e:
			print e
			return False

	def populatePlayersField(self, player, init=""):
		''' Init the playfield of a player, if no init arguments given can be done interacively
		:param player: name of player
		:type player: str
		:param init: name of owner of the game
		:type init: list of tuples (<str:name of ship>, <str: ship placement args>)
		:returns: if populating playfield was successful
		:rtype: bool
		'''
		field = self.players[player].getPlayfield()
		shipTypes = Ship.getShipTypes()
		if init == "":
			for ship in shipTypes:
				name, len = ship
				print field.toString()
				while True:
					usr = raw_input("enter coords for %s (%d tiles) (<y>,<x>,<rotation>)> " % ship)
					try:
						print usr[:1], usr[1:]
						y = usr[:1]
						x, rot = usr[1:].split(" ")
						if field.addShip(name, (y, int(x)), rot):
							break
						print "illegal ship pos"
					except Exception, e:
						print "wrong params enter <a-j><1-10>,<horizontal-vertical>", e
			return True
		else:
			for param in init:
				ship, coords = param
				try:
					y = coords[:1]
					x, rot = coords[1:].split(" ")
					if not field.addShip(ship, (y, int(x)), rot):
						return False
				except Exception, e:
					print "wrong params enter <a-j><1-10>,<horizontal-vertical>", e
					return False

		print field.toString()
		return

	def getPlayerState(self, player):
		''' returns string of players playfield for displaying
		:param player: player's name
		:type player: str
		:returns: string of playfiled
		:rtype: str
		'''
		return self.players[player].playfield.toString()

	def attackPlayer(self, player, location):
		'''
		attack player
		:param player: name of player to attack
		:type player: str
		:param location: tuple of coords where to attack
		:type location: tuple (<str>, int)
		'''
		y, x = location
		location = (Battlefield.y_coords.index(y), Battlefield.x_coords.index(x))
		field = self.players[player].getPlayfield()

		result = field.fireAtShip(location)
		if result == 'sunk':
			ships = field.getAliveShips()
			if len(ships) == 0:
				result = 'end'
		return result

	def getGameState(self, requestMaker):
		'''
		Assemble different players playfield into one printout mask ship locations for all ships others than the
		selected players ship
		:param player: name of player making request
		:type player: str
		:return:
		'''
		# create empty list of strings
		gamestate = [''] * 13
		for player in self.players.keys():
			lines = self.players[player].getPlayfield().toString()[:-1]
			# hide ships from all players other than own
			if player != requestMaker:
				lines = lines.replace(u'\u25C9', u'\u2610')
			lines = lines.split('\n')
			for i in range(len(lines)):
				gamestate[i + 1] += lines[i] + '|\t'
			rowLen = len(gamestate[1].expandtabs(4))
			tags = gamestate[0] + 'Player : ' + player
			taglen = len((tags))
			gamestate[0] += 'Player : ' + player + ' ' * ((rowLen - taglen) - 4) + '|'
		gamestate[0] += '\n'
		gamestate[-1] = '\n'+Battlefield.getLegend()
		return reduce(lambda x, y: x + y + '\n', gamestate)

	def __eq__(self, other):
		return self.game_name == other

	def __repr__(self):
		return self.game_name


class Player:
	def __init__(self, name):
		'''
		:param name:
		:type name: str
		'''
		self.name = name
		self.isAlive = True
		self.playfield = Battlefield()


	def getPlayfield(self):
		return self.playfield


class Battlefield:
	x_coords = range(1, 11)
	y_coords = ['a', 'b', 'c', 'd', 'e',
	            'f', 'g', 'h', 'i', 'j']

	legend = {'none' : u'\u2610',
	          'water': u'\u2612',
	          'hit'  : u'\u2b14',
	          'ship' : u'\u25C9',
	          'sunk' : u'\u271d'}

	def __init__(self):
		self.battlefield_complete = False
		self.ships = list()
		self.battlefield = list()
		for y in self.y_coords:
			self.battlefield.append(list())
			for x in range(len(self.x_coords)):
				self.battlefield[-1].append('none')
		return

	def addShip(self, type, location, rotation):
		# convert coord from human readable to index
		y, x = location
		location = (self.y_coords.index(y), self.x_coords.index(x))
		# check if ship already exists
		if not (type in self.ships):
			try:
				ship = Ship(type, location, rotation)
				location = ship.getLocation()
				# check if ship location legal
				for coord in location:
					y, x = coord
					for y_offset in range(-1, 2):
						for x_offset in range(-1, 2):
							try:
								cell = self.battlefield[y + y_offset][x + x_offset]
								if cell != 'none':
									return False
							except ValueError:
								pass

				# add ship to battlefield
				for coord in location:
					y, x = coord
					self.battlefield[y][x] = 'ship'
				self.ships.append(ship)
				return True
			except Exception, e:
				print e
				return False
		return False

	def toString(self):
		string = ""
		string += '\t'
		for x in self.x_coords:
			string += str(x) + '\t'
		string += '\n'
		for y in range(len(self.y_coords)):
			string += str(self.y_coords[y]) + '\t'
			for x in range(len(self.x_coords)):
				cell = self.battlefield[y][x]
				string+= self.legend[cell]
				string += '\t'
			string += '\n'
		return string

	def printPlayfield(self):
		print self.toString()

	def hasShip(self, location):
		y, x = location
		if self.battlefield[y][x] != 'none':
			return True
		return False

	def fireAtShip(self, location):
		y, x = location
		for ship in self.ships:
			result = ship.hitShip(location)
			if result == 'hit':
				self.battlefield[y][x] = 'hit'
				return 'hit'
			elif result == 'sunk':
				for loc in ship.getLocation():
					y, x = loc
					self.battlefield[y][x] = 'sunk'
				return 'sunk'
		self.battlefield[y][x] = 'water'
		return 'miss'

	def getAliveShips(self):
		alive_ships = list()
		for ship in self.ships:
			if not ship.isSunk():
				alive_ships.append(ship)
		return alive_ships

	@classmethod
	def getLegend(self):
		returnString = "Legend :\n"
		for key, value in self.legend.iteritems():
			returnString+= value+' : '+key+'\n'
		return returnString.replace('none', 'fog of war')


class Ship:
	shipTypes = {'Aircraft Carrier': 5,
	             'Battleship'      : 4,
	             'Submarine'       : 3,
	             'Cruiser'         : 3,
	             'Destroyer'       : 2}

	def __init__(self, type, location, rotation='h'):
		self.type = type
		self.length = self.shipTypes[type]
		self.location = location
		self.rotation = rotation
		self.hit_indices = list()
		for x in range(self.length):
			self.hit_indices.append(0)
		return

	def hitShip(self, locationHit):
		yHit, xHit = locationHit
		yLoc, xLoc = self.location
		if self.rotation == 'h':
			if (yHit == yLoc) and (xLoc <= xHit <= xLoc + self.length):
				self.hit_indices[yHit - yLoc] = 1
				if self.isSunk():
					return 'sunk'
				else:
					return 'hit'
			else:
				return 'miss'
		else:
			if (xHit == xLoc) and (yLoc <= yHit <= yLoc + self.length):
				self.hit_indices[yHit - yLoc] = 1
				if self.isSunk():
					return 'sunk'
				else:
					return 'hit'
			else:
				return 'miss'

	def isSunk(self):
		return sum(self.hit_indices) == len(self.hit_indices)

	def getLocation(self):
		yLoc, xLoc = self.location
		location = list()
		if self.rotation == 'h':
			for x in range(self.length):
				location.append((yLoc, xLoc + x))
			return location
		else:
			for y in range(self.length):
				location.append((yLoc + y, xLoc))
			return location

	@classmethod
	def getShipTypes(self):
		ships = sorted(self.shipTypes.items(), key=operator.itemgetter(1))
		ships.reverse()
		return ships

	def __eq__(self, other):
		return self.type == other

	def __str__(self):
		return self.type

	def __repr__(self):
		return self.type


if __name__ == "__main__":
	# some tests
	initField = [('Aircraft Carrier', 'a1 v'),
	             ('Battleship', 'a3 v'),
	             ('Cruiser', 'a5 v'),
	             ('Submarine', 'a7 v'),
	             ('Destroyer', 'a9 v')]

	game = Game(3, 'me')

	game.addPlayer('me')
	game.populatePlayersField('me', init=initField)
	game.addPlayer('him')
	game.populatePlayersField('him', init=initField)

	game.addPlayer('her')
	game.populatePlayersField('her', init=initField)
	print game.attackPlayer('me', ('a', 9))
	print game.attackPlayer('me', ('b', 9))
	print game.attackPlayer('me', ('a', 2))
	print game.attackPlayer('me', ('a', 1))

	print game.getPlayerState('me')
	print game.getGameState('me')
