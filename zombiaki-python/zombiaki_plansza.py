from enum import Enum
from copy import deepcopy
from itertools import count

class BoardSlot:
	def __init__(self, card, roundNo):
		self.cards=[card]
		self.roundPlayed = roundNo

class Position:
	def __init__(self, row, col):
		self.row = row
		self.col = col
	def __eq__(self, other):
		return self.row == other.row and self.col == other.col

class Board:
	Rows = 5	#przecznice, 0 to 1wsza przecznica, ... 4 to 5ta przecznica
	Columns = 3	#ulice 0,1,2
	@staticmethod
	def create():
		b = Board()
		b.cells = [ [None]*Board.Columns for i in range(0,Board.Rows) ]
		return b
	
	def __getitem__(self, row):
		return self.cells[row]
	
	def findExpiredCards(self, currentRoundNo):
		expired = []
		for r in range(0,Board.Rows):
			for c in range(0,Board.Columns):
				s = self.cells[r][c]
				if s is not None and (s.roundPlayed + 2) <= currentRoundNo:
					expired.append( Position(r,c) )

		#expired =   [   p 
		#                for p,s in 
		#                    [ ( Position(r,c), self.cells[r][c] )
		#                        for r in range(0,Board.Rows)
		#                        for c in range(0,Board.Columns) 
		#                    ]
		#                if s is not None and (s.roundPlayed + 2) >= currentRoundNo
		#            ]

		return expired

	def iter(self):
		for r in range(0,Board.Rows):
			for c in range(0,Board.Columns):
				yield self.cells[r][c], Position(r,c)

	def findMoveableCards(self, player):
		moveable = []
		for r in range(0,Board.Rows):
			for c in range(0,Board.Columns):
				s = self.cells[r][c]
				if s is not None:
					c = s.cards[0]
					if c.isMovable and c.owner == player:
						moveable.append( Position(r,c) )
		return moveable

	def removeCard(self, position):
		c = self.cells[position.row][position.col]
		self.cells[position.row][position.col] = None
		return c

	def placeCard(self, newCard, position, roundNo):
		slot = self.cells[position.row][position.col]
		if slot is not None:
			# TODO: FixMe
			# zagyrwająć drugą kartę są dwie opcje
			# 1. druga karta doczepia się na stałe do pierwszej
			#    np. człowiek, pazury, boss, miś
			# 2. kot lub pies poruszają się niezależnie
			if type(newCard) == Booster:
				success = False
				for card in slot.cards:
					if newCard.attachTo(card) == True:
						success = True
						break
				assert(success)
			else:
				slot.cards.append(newCard)
		else:
			self.cells[position.row][position.col] = BoardSlot(newCard, roundNo)
		newCard.position= position
	
	def moveCard(self, position):
		raise NotImplementedError
	
	def findCardByType(self, type_):
		for bp, _ in self.iter():
			if bp is None: continue
			for c in bp.cards:
				if type(c)==type_:
					return c
		return None
	
