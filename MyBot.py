#!/usr/bin/env python
from ants import *
from math import sqrt
# define a class with a do_turn method
# the Ants.run method will parse and update bot input
# it will also run the do_turn method for us
class MyBot:
	def __init__(self):

        # define class level variables, will be remembered between turns
		pass
    
    # do_setup is run once at the start of the game
    # after the bot has received the game settings
    # the ants class is created and setup by the Ants.run method
	def do_setup(self, ants):
		self.SafeDistance2 = ants.attackradius2 + 4*sqrt(ants.attackradius2) + 4
		self.AttackDistance = sqrt(ants.attackradius2) + 2
		self.unseen = []
		
		for row in range((ants.rows)/10):
			for col in range((ants.cols)/10):
				self.unseen.append((row*10, col*10))
		self.Hills = []

		pass
    
    # do turn is run once per turn
    # the ants class has the game state and is updated by the Ants.run method
    # it also has several helper methods to use
	def do_turn(self, ants):
        # track all moves, prevent collisions

		orders = {}

		def Move_Direction(Loc, Direction):
			NewLoc = ants.destination(Loc, Direction)
			if (ants.unoccupied(NewLoc) and NewLoc not in orders):
 				ants.issue_order((Loc, Direction))
				orders[NewLoc] = Loc
				return True
			else:
				return False


		Targets = {}

		def Move_Toward_Loc(Loc, Dest):
			Directions = ants.direction(Loc, Dest)
			for Direction in Directions:
				if Move_Direction(Loc, Direction):
					Targets[Dest] = Loc
					return True
			return False

		def Move_Away_Loc(Loc, Dest):
			Directions = ants.Opp_Direction(Loc, Dest)
			for Direction in Directions:
				if Move_Direction(Loc, Direction):
					Targets[Dest] = Loc
					return True
			return False


		def Deal_With_Enemy(MyAntLoc):
			
			for (EnAntLoc,Owner) in ants.enemy_ants():
				Dist2E = ants.distance2(MyAntLoc, EnAntLoc)
				if (Dist2E <= self.SafeDistance2):
					DistE = ants.distance2(MyAntLoc, EnAntLoc)
					if (DistE <= self.AttackDistance):
						for MyOtherAntLoc in ants.my_ants():
							if (MyOtherAntLoc != MyAntLoc):
								DistF = ants.distance(EnAntLoc, MyOtherAntLoc)
								if (DistF <= self.AttackDistance):
									if(Move_Toward_Loc(MyAntLoc, EnAntLoc)):
										return True						
					if (Dist2E == self.SafeDistance2):
						return True
					if (Move_Away_Loc(MyAntLoc, EnAntLoc)):
						return True	
			return False

		def Deal_With_Food(MyAntLoc):
			FoodDists = []
			for FoodLoc in ants.food():
				Dist = ants.distance(MyAntLoc, FoodLoc)
				FoodDists.append((Dist, FoodLoc))
			FoodDists.sort()
			for Dist, FoodLoc in FoodDists:
				if(Move_Toward_Loc(MyAntLoc, FoodLoc)):
					return True
			return False

		def Explore(MyAntLoc):
			UnseenDists = []
			for UnseenLoc in self.unseen:
				Dist = ants.distance(MyAntLoc, UnseenLoc)
				UnseenDists.append((Dist, UnseenLoc))
			UnseenDists.sort()
			for Dist, UnseenLoc in UnseenDists:
				if(Move_Toward_Loc(MyAntLoc, UnseenLoc)):
					return True
			return False

		def Deal_With_Hills(MyAntLoc):
			HillDists = []
			for HillLoc in self.Hills:
				Dist = ants.distance(MyAntLoc, HillLoc)
				HillDists.append((Dist, HillLoc))
			HillDists.sort()
			for Dist, HillLoc in HillDists:
				if(Move_Toward_Loc(MyAntLoc, HillLoc)):
					return True				
			return False

		for loc in self.unseen[:]:
			if ants.visible(loc):
				self.unseen.remove(loc)

		for HillLoc, hill_owner in ants.enemy_hills():
			if HillLoc not in self.Hills:
				self.Hills.append(HillLoc) 


		for MyAntLoc in ants.my_ants():

			#worry about enemy ants
			if Deal_With_Enemy(MyAntLoc):
				continue

			#find food
			if Deal_With_Food(MyAntLoc):
				continue

			#worry about enemy hills

			if Deal_With_Hills(MyAntLoc):
				continue

			#explore
			if Explore(MyAntLoc):
				continue

			if ants.time_remaining() < 10:
				break
            
if __name__ == '__main__':
    # psyco will speed up python a little, but is not needed
	try:
		import psyco
		psyco.full()
	except ImportError:
		pass
    
	try:
        # if run is passed a class with a do_turn method, it will do the work
        # this is not needed, in which case you will need to write your own
        # parsing function and your own game state class
		Ants.run(MyBot())
	except KeyboardInterrupt:
		print('ctrl-c, leaving ...')
