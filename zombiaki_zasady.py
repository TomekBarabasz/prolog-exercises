import unittest
from enum import Enum
from random import shuffle
from copy import deepcopy
from itertools import count

from zombiaki_karty import *
from zombiaki_plansza import *

#################################################################################
class Actions(Enum):
	Noop = 0
	PlaceCard = 1
	MoveCards = 2
	RemoveCards = 3
	DiscardCard = 4
	TakeCards = 5

class Action:
	def __init__(self, action, args=None, position=None):
		self.action = action
		self.args = args
		self.position = position

""" Przebieg gry:
1 runda
	zombiaki
		sprzątanie
		przesuwanie kota
		przesuwanie psa
		przesuwanie zombie
		dobieranie
		wyrzucanie
		zagranie kart
2 runda
	Ludzie
		sprzątanie
		przesuwanie
		dobieranie
		wyrzucanie
		zagranie kart
2 runda
	zombiaki
		...
	ludzie
		...
3 runda """

class Phase(Enum):
	RemoveExpiredCards=0
	CatMovement=1   #skipped if no cat in play
	DogMovement=2   #skipped if no dog in play
	OtherCardMovement=3
	TakeNewCards=4
	DiscardCard=5
	Play1stCard=6
	Play2ndCard=7
	Play3rdCard=8
	NumberOfPhases=9

	@staticmethod
	def next(currentPhase, currentPlayer, useCat, useDog):
		vn = currentPhase.value + 1
		#need two if's as both can be skipped
		if vn==Phase.CatMovement.value\
			and (not useCat or currentPlayer == Player.Humans): 
			vn += 1
		if vn==Phase.DogMovement.value\
			and (not useDog or currentPlayer == Player.Humans):
			vn += 1
		nextRonud=False
		if vn==Phase.NumberOfPhases.value:
			vn = Phase.RemoveExpiredCards
			nextRonud=True
		return Phase(vn), nextRonud
	
class GameState:
	@classmethod
	def init(cls):
		cls.PhaseToLegalMoves = { Phase.RemoveExpiredCards  : cls.getLegalMoves_in_removeExpiredCards,
								  Phase.CatMovement         : cls.getLegalMoves_in_CatMovement,
								  Phase.DogMovement         : cls.getLegalMoves_in_DogMovement,
								  Phase.OtherCardMovement   : cls.getLegalMoves_in_Movement,
								  Phase.TakeNewCards        : cls.getLegalMoves_in_takeNewCards,
								  Phase.DiscardCard         : cls.getLegalMoves_in_DiscardCard,
								  Phase.Play1stCard         : cls.getLegalMoves_in_PlayCard,
								  Phase.Play2ndCard         : cls.getLegalMoves_in_PlayCard,
								  Phase.Play3rdCard         : cls.getLegalMoves_in_PlayCard }
		cls.PhaseToExec       = { Phase.RemoveExpiredCards  : cls.execMove_in_removeExpiredCards,
								  Phase.CatMovement         : cls.execMove_in_Movement,
								  Phase.DogMovement         : cls.execMove_in_Movement,
								  Phase.OtherCardMovement   : cls.execMove_in_Movement,
								  Phase.TakeNewCards        : cls.execMove_in_takeNewCards,
								  Phase.DiscardCard         : cls.execMove_in_DiscardCard,
								  Phase.Play1stCard         : cls.execMove_in_PlayCard,
								  Phase.Play2ndCard         : cls.execMove_in_PlayCard,
								  Phase.Play3rdCard         : cls.execMove_in_PlayCard }
	@staticmethod
	def createRandom():
		zombiesDeck = list(deepcopy(ZombiesCards))
		shuffle(zombiesDeck)
		humansDeck  = list(deepcopy(HumansCards))
		shuffle(humansDeck)
		return GameState.create(zombiesDeck, humansDeck)

	@staticmethod
	def create(zombiesDeck, humansDeck):
		gs = GameState()
		gs.board = Board()
		gs.isDogInPlay = False
		gs.isCatInPlay = False
		gs.cemetary = []
		gs.barricade = []
		gs.thrash = []
		gs.zombiesDeck = zombiesDeck
		gs.humansDeck = humansDeck
		gs.player = Player.Zombies
		gs.phase = Phase.TakeNewCards
		gs.roundNo = 1
		gs.deck = gs.zombiesDeck
		gs.hand = gs.cemetary
		return gs

	def nextPhase(self):
		self.phase,nextPlayer = Phase.next(self.phase, self.player, self.isCatInPlay, self.isDogInPlay)
		if nextPlayer:
			self.roundNo += 1
			self.player = Turn.next(self.player)
			if self.player == Player.Zombies:
				self.deck = self.zombiesDeck 
				self.hand = self.cemetary
			else:    
				self.deck =  self.humansDeck
				self.hand = self.barricade
	
	def getLegalMoves(self, player):
		if player != self.player: return [Action(Actions.Noop)]
		return GameState.PhaseToLegalMoves[self.phase](self, player)

	def getNextState(self, player, move):
		ns = deepcopy(self)
		GameState.PhaseToExec[ns.phase](ns, player,move)
		ns.nextPhase()
		return ns

	def getLegalMoves_in_removeExpiredCards(self, player):
		expired = self.board.findExpiredCards(player, self.roundNo)
		return [ Action(Actions.RemoveCards,expired) ]
	
	def getLegalMoves_in_takeNewCards(self, player):
		numCardsToTake = min( 4 - len(self.hand), len(self.deck) )
		return [ Action(Actions.TakeCards,numCardsToTake) ]

	def getLegalMoves_in_CatMovement(self, player):
		kot = self.board.findCardByType(Kot)
		assert(kot is not None)
		positions = kot.getLegalPositionsAfterMove(self.board)
		return [ Action(Actions.MoveCards, kot, pos)  for pos in positions ]

	def getLegalMoves_in_DogMovement(self, player):
		pies = self.board.findCardByType(Pies)
		assert(pies is not None)
		positions = pies.getLegalPositionsAfterMove(self.board)
		return [ Action(Actions.MoveCards, pies, pos)  for pos in positions ]
	
	def getLegalMoves_in_Movement(self, player):
		return [ Action(Actions.MoveCards, moveable) ]

	def getLegalMoves_in_DiscardCard(self, player):
		assert(self.hand is not None)
		return [ Action(Actions.DiscardCard, card) for card in self.hand ]
	
	def getLegalMoves_in_PlayCard(self, player):
		Mv = [ Action(Action.Noop) ]
		for card in self.hand:
			ValidPositions = self.board.getCardValidPositions(card)
			Mv.extend( [ Action(Actions.PlaceCard, c, vp) for vp in ValidPositions] )
		return Mv
	
	def execMove_in_removeExpiredCards(self, player, move):
		assert(move.action == Actions.RemoveCards)
		Bc = [self.board.removeCard(pos) for pos in move.args]
		for bc in Bc:
			self.thrash.extend( bd.cards )
		
	def execMove_in_Movement(self, player, move):
		assert(move.action == Actions.MoveCards)
		for pos in move.args:
			self.board.moveCard(pos)

	def execMove_in_takeNewCards(self, player, move):
		self.hand.extend( self.deck[0 : move.args] )
		del self.deck[0 : move.args]

	def execMove_in_DiscardCard(self, player, move):
		 self.hand.remove(move.args)
		 self.thrash.append(move.args)

	def execMove_in_PlayCard(self, player, move):
		pass

class CardTests(unittest.TestCase):
	def test_BulletProofZombie(self):
		z = BulletProofZombie(3)
		self.assertEqual( z.owner, Player.Zombies )
		self.assertTrue( z.isZombie )
		self.assertTrue( z.isMovable )
	
	def test_Kot(self):
		z = Kot()
		self.assertEqual( z.owner, Player.Zombies )
		self.assertTrue( z.isZombie )
		self.assertTrue( z.isMovable )
		self.assertEqual(z.wounds, 1)

	def test_Czlowiek(self):
		z = Czlowiek()
		self.assertEqual( z.owner, Player.Zombies )
		self.assertFalse( z.canAttachTo( Kot() ))
		self.assertFalse( z.canAttachTo( Pies() ))
		self.assertTrue( z.canAttachTo( BulletProofZombie(3) ))
	
	def test_compare_zombie_cards(self):
		b1 = BulletProofZombie(3)
		b2 = BulletProofZombie(3)
		self.assertEqual(b1,b2)
	
	def test_kot_initial_position(self):
		b = Board.create()
		kot =Kot()
		b.placeCard( Zombie(2), Position(0,0), 1 )
		validPositions = kot.getLegalInitialPositions(b)
		expvp = [ Position(0,1), Position(0,2) ]
		for p in validPositions:self.assertIn( p, expvp )
		for p in expvp:	 		self.assertIn( p, validPositions )
	
	def test_kot_movement(self):
		b = Board.create()
		kot = Kot()
		b.placeCard( kot, 		Position(0,1), 1 )
		b.placeCard( Zombie(2), Position(0,0), 1 )
		b.placeCard( Zombie(2), Position(1,1), 1 )
		b.placeCard( Zapora(), 	Position(4,0), 1 )
		b.placeCard( Zapora(), 	Position(4,1), 1 )
		b.placeCard( Zapora(), 	Position(4,2), 1 )
		vp = list(kot.getLegalPositionsAfterMove(b))
		exp_vp = [ Position(0,0), Position(0,1), Position(0,2), Position(1,1), Position(2,1) ]
		for p in vp: 		self.assertTrue( p in exp_vp )
		for p in exp_vp:	self.assertTrue( p in vp )
	
class TurnsTests(unittest.TestCase):
	def test1(self):
		p = Phase.RemoveExpiredCards
		pn,nextPlayer = Phase.next(p, Player.Zombies, False,False)
		self.assertEqual(pn, Phase.OtherCardMovement)
		self.assertFalse(nextPlayer)
		p = Phase.Play3rdCard
		pn,nextPlayer = Phase.next(p, Player.Zombies, False,False)
		self.assertEqual(pn, Phase.RemoveExpiredCards)
		self.assertTrue(nextPlayer)

	def test2(self):
		p = Phase.RemoveExpiredCards
		pn,nextPlayer = Phase.next(p,Player.Zombies, True,False)
		self.assertEqual(pn, Phase.CatMovement)
		self.assertFalse(nextPlayer)

		pn,nextPlayer = Phase.next(pn,Player.Zombies, True,False)
		self.assertEqual(pn, Phase.OtherCardMovement)
		self.assertFalse(nextPlayer)

		p = Phase.CatMovement
		pn,nextPlayer = Phase.next(p,Player.Zombies, True,True)
		self.assertEqual(pn, Phase.DogMovement)
		self.assertFalse(nextPlayer)
		pn,nextPlayer = Phase.next(pn,Player.Zombies, False, False)
		self.assertEqual(pn, Phase.OtherCardMovement)
		self.assertFalse(nextPlayer)

	def test3(self):
		p = Phase.RemoveExpiredCards
		pn,nextPlayer = Phase.next(p,Player.Humans, True,True)
		self.assertEqual(pn, Phase.OtherCardMovement)
		self.assertFalse(nextPlayer)

class BoardTests(unittest.TestCase):
	def test1(self):
		c1 = Kot()
		c2 = Kot()
		c3 = Kot()
		b = Board.create()
		b.placeCard( c1, Position(0,0), 1)
		b.placeCard( c2, Position(1,1), 1)
		b.placeCard( c3, Position(2,2), 2)        
		e = b.findExpiredCards(1)
		self.assertEqual(e, [])
		e = b.findExpiredCards(2)
		self.assertEqual(e, [])
		e = b.findExpiredCards(3)
		self.assertEqual(e, [Position(0,0), Position(1,1)])
		e = b.findExpiredCards(4)
		self.assertEqual(e, [Position(0,0), Position(1,1), Position(2,2)])
		c = b.removeCard(Position(2,2))
		self.assertEqual(c.cards[0],c3)
		c = b.removeCard(Position(1,1))
		self.assertEqual(c.cards[0],c2)
		c = b.removeCard(Position(0,0))
		self.assertEqual(c.cards[0],c1)
		e = b.findExpiredCards(4)
		self.assertEqual(e, [])
	
	def test2(self):
		b = Board.create()
		b.placeCard(Kot(), Position(4,2), 1)
		c = b.findCardByType(Kot)
		self.assertTrue(c is not None)
		self.assertEqual(type(c),Kot)
		
		b.removeCard(Position(4,2))
		c = b.findCardByType(Kot)
		self.assertTrue(c is None)

class GameStateTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		GameState.init()

	def test1(self):
		#1st Zombie action after create
		s = GameState.createRandom()
		Mv = s.getLegalMoves(Player.Zombies)
		self.assertEqual( len(Mv), 1 )
		self.assertEqual( Mv[0].action, Actions.TakeCards )
		self.assertEqual( Mv[0].args, 4 )
	
	def test2(self):
		#1st human action after create
		s = GameState.createRandom()
		Mv = s.getLegalMoves(Player.Humans)
		self.assertEqual( len(Mv), 1 )
		self.assertEqual( Mv[0].action, Actions.Noop )

	def test3(self):
		#TakeCard action
		s = GameState.createRandom()
		self.assertEqual(s.hand,[])
		nc = len(s.deck)
		tod = s.deck[0:4]
		Mv = s.getLegalMoves(Player.Zombies)
		self.assertEqual(Mv[0].action, Actions.TakeCards)
		ns = s.getNextState(Player.Zombies, Mv[0])
		#check if s does not changes
		self.assertEqual(s.phase, Phase.TakeNewCards)
		self.assertEqual(s.hand, [])
		self.assertEqual(len(s.deck), nc)
		#check ifns is next phase
		self.assertEqual(ns.hand, tod)
		self.assertEqual(len(ns.deck), nc-4)
		self.assertEqual(ns.phase, Phase.DiscardCard)

	def test4(self):
		#DiscardCard action
		s = GameState.createRandom()
		Mv = s.getLegalMoves(Player.Zombies)
		self.assertEqual(Mv[0].action, Actions.TakeCards)
		s = s.getNextState(Player.Zombies, Mv[0])
		Mv = s.getLegalMoves(Player.Zombies)
		self.assertEqual(len(Mv),4)
		for m,i in zip(Mv,count(0)):
			self.assertEqual( m.action, Actions.DiscardCard )
			self.assertEqual( m.args, s.hand[i] )
		ns = s.getNextState(Player.Zombies, Mv[0])
		self.assertTrue( Mv[0].args not in ns.hand )
		self.assertTrue( Mv[0].args in ns.thrash )
		for i in range(1,4):
			c = Mv[i].args
			self.assertTrue( c in ns.hand )
			self.assertTrue( c not in ns.thrash )
		self.assertEqual(ns.phase, Phase.Play1stCard)
		

	
if __name__ == '__main__':
	unittest.main()
