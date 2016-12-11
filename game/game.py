import operator

initField = [('Aircraft Carrier','a1 v'),
             ('Battleship','a3 v'),
             ('Cruiser','a5 v'),
             ('Submarine','a7 v'),
             ('Destroyer','a9 v')]
class Game:
	def __init__(self, battlefield_size, owner):
		self.battlefield_size = battlefield_size
		self.owner = owner
		self.players = dict()
		self.players[self.owner] = Battlefield()
		self.winner = None
		return

	def addPlayer(self, player):
		if len(self.players.keys()) < self.battlefield_size and not self.players.has_key(player):
			self.players[player] = Battlefield()
			return True
		else:
			return False

	def populatePlayersField(self, player, init=""):
		field = self.players[player]
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
					except Exception,e :
						print "wrong params enter <a-j><1-10>,<horizontal-vertical>", e
			return True
		else:
			for param in init:
				ship, coords = param
				try:
					y = coords[:1]
					x, rot =coords[1:].split(" ")
					if not field.addShip(ship, (y, int(x)), rot):
						return False
				except Exception, e:
					print "wrong params enter <a-j><1-10>,<horizontal-vertical>", e
					return False


		print field.toString()
		return

	def getPlayerState(self, player):
		return self.players[player].toString()

	def attackPlayer(self, player, location):
		y, x = location
		location = (Battlefield.y_coords.index(y), Battlefield.x_coords.index(x))
		field = self.players[player]

		result = field.fireAtShip(location)
		if result == 'sunk':
			ships = field.getAliveShips()
			print ships
		return result

class Battlefield:
	x_coords = range(1, 11)
	y_coords = ['a', 'b', 'c', 'd', 'e',
	            'f', 'g', 'h', 'i', 'j']

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
					for y_offset in range(-1,2):
						for x_offset in range(-1,2):
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
				if cell == 'none':
					string +=u'\u2610'
				elif cell == 'water':
					string +=u'\u2612'
				elif cell == 'hit':
					string +=u'\u2b14'
				elif cell == 'ship':
					string += u'\u25C9'
				elif cell == 'sunk':
					string += u'\u271d'
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


class Ship:
	shipTypes = {'Aircraft Carrier' : 5,
	             'Battleship'       : 4,
	             'Submarine'        : 3,
	             'Cruiser'          : 3,
	             'Destroyer'        : 2}

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
			if (yHit == yLoc) and (xLoc <= xHit <= xLoc+self.length):
				self.hit_indices[yHit-yLoc] = 1
				if self.isSunk():
					return 'sunk'
				else:
					return 'hit'
			else:
				return 'miss'
		else:
			if (xHit == xLoc) and (yLoc <= yHit <= yLoc+self.length):
				self.hit_indices[yHit-yLoc] = 1
				if self.isSunk():
					return 'sunk'
				else:
					return 'hit'
			else:
				return 'miss'

	def isSunk(self):
		return sum(self.hit_indices)==len(self.hit_indices)

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
		ships =sorted(self.shipTypes.items(), key=operator.itemgetter(1))
		ships.reverse()
		return ships

	def __eq__(self, other):
		return self.type == other

	def __str__(self):
		return self.type

	def __repr__(self):
		return  self.type

game = Game(2,'me')

game.addPlayer('me')
game.populatePlayersField('me', init=initField)
print game.attackPlayer('me', ('a', 9))
print game.attackPlayer('me', ('b', 9))
print game.attackPlayer('me', ('a', 2))
print game.attackPlayer('me', ('a', 1))

print game.getPlayerState('me')
