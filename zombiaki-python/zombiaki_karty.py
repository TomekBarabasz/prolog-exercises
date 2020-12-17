from enum import Enum
from zombiaki_plansza import *

class Player(Enum):
	Zombies = 0
	Humans = 1
	@staticmethod
	def next(player):
		tn = (player.value + 1 ) % 2
		return Player(tn)

class Card:
	pass

class ZombieCard(Card):
	def __init__(self):
		self.owner = Player.Zombies

class Zombie(ZombieCard):
	def __init__(self, strength, description=None):
		ZombieCard.__init__(self)
		self.isZombie = True
		self.wounds = strength
		self.description = description
		self.isMovable = True
		self.position = None

	def __eq__(self, other):
		return type(other) == type(self) and self.wounds == other.wounds and self.description == other.description
	
	def getLegalMoves(self, board):
		raise NotImplementedError

class BulletProofZombie(Zombie):
	pass

class Krystyna(Zombie):
	pass

class Booster(ZombieCard):
	def canAttachTo(self, host):
		return type(host) != Kot and type(host) != Pies

	def attachTo(self, host):
		assert(self.canAttachTo(host))
		self.host = host
		host.booster = self

class Czlowiek(Booster):
	pass

class Szpony(Booster):
	pass

class Bear(Booster):
	def __init__(self):
		self.wounds = 4

class ZwierzakZombie(Zombie):
	def __init__(self, strength, description, movement):
		Zombie.__init__(self, strength, description)
		self.movement = movement
		
	def getLegalInitialPositions(self, board):
		#wystaw kota zgodnie z regułami wystawiania zombiaków: tylko 1wsza przecznica, na puste pole
		return [ Position(0,col)  for col in range(0,board.Columns) if board[0][col] is None ]
	
	def getLegalPositionsAfterMove(self, board):
		legalPositions=[]
		col = self.position.col
		for dr in range(-self.movement, self.movement+1):
			nr = self.position.row + dr
			if nr >= 0 and nr < board.Rows:
				legalPositions.append( Position(nr,col) )
		row = self.position.row
		for dc in (-1,1):
			nc = self.position.col + dc
			if nc >= 0 and nc < board.Columns:
				 legalPositions.append( Position(row,nc) )
		def isZombieOrEmpty(pos):
			bs = board[pos.row][pos.col]
			card = bs.cards[0] if bs is not None else None
			return card is None or card.isZombie
		return filter( isZombieOrEmpty, legalPositions)

class Kot(ZwierzakZombie):
	def __init__(self):
		ZwierzakZombie.__init__(self, 1, 'Kot', 2)

class Pies(ZwierzakZombie):
	def __init__(self):
		ZwierzakZombie.__init__(self, 2, 'Pies', 3)

ZombiesCards = (
	Zombie(2, 'Krzysztof'),
	Zombie(2, 'Czesiek'),
	Zombie(3, 'Arkadiusz'),
	Zombie(3, 'Mietek'),
	Zombie(3, 'Wacek'),
	Zombie(3, 'Kazimierz'),
	Zombie(3, 'Andrzej'),
	Zombie(3, 'Zenek'),
	Zombie(4, 'Stefan'),
	Zombie(4, 'Marian'),
	Zombie(5, 'Iwan'),
	Zombie(5, 'Mariusz'),
	BulletProofZombie(3)
)

#################################################################################

class HumansCard(Card):
	def __init__(self):
		self.owner = Player.Humans

class Shot(HumansCard):
	def __init__(self, strength, description):
		self.wounds = strength
		self.description = description

class BulletBurst(Shot):
	pass

class SharpShot(Shot):
	pass

class Zapora(HumansCard):
	pass

HumansCards = (
	Shot(1,'Regular'),
	Shot(1,'Regular'),
	Shot(1,'Regular'),
	Shot(1,'Regular'),
	Shot(1,'Regular'),
	Shot(1,'Regular'),
	Shot(1,'Regular'),
	Shot(2,'Better'),
	Shot(2,'Better'),
	Shot(2,'Better'),
	BulletBurst(2,'Short'),
	BulletBurst(3,'Long'),
	SharpShot(2,'Sharp shot')
)
