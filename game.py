import os
from board import Board
import keypress
import ai,copy,math
import argparse
class Game(object):



	def __init__(self,board=[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],ai=False, step=False):
		self.board = Board(board)
		self.score = 0
		self.ai = ai
		self.step = step
		
		
	def readMove(self):
		return keypress.getKey()
	
	def clrscr(self):
		if os.name == 'nt':	
			os.system('cls')
				
		else:
			os.system('clear')	
		
		
	def game(self):

		if not self.ai:
			while not self.board.won() or self.board.canMove():
			
				# self.board.drawBoard(self.board.getCells())
				
				key = self.readMove()
				self.clrscr()
				
				if key:
					if self.board.move(key):
						self.board.tileGen(1)
					self.board.drawBoard()
				else:
					break
		else:
			print 'Press any key to begin...'
			while True:
				raw_input('')
				self.clrscr()
				self.board.drawBoard()
				if self.board.highestTile()[0] > 512:
					self.evalfn(self.board, True)
					# raw_input(' ')
				# d = self.dfs(copy.deepcopy(self.board))
				# moves = ['up','left','right','down']
				# d = [float('inf'),None]
				# while depth<=1:
				# for m in moves:
					# b2 = copy.deepcopy(self.board)
					# if b2.move(m):
						# temp =  10*ai.manhatDist(b2.highestTile()) + (1.0/(b2.getEmptyCells()+0.001))
						# print b2.highestTile()
						# print ai.manhatDist(b2.highestTile())
						# print 'empty = '+str(b2.getEmptyCells())
						# print m
						# print temp
						# print '----'
						# if d[0]>temp:
							# d[0],d[1]=temp,m
					# else:
						# continue
				# if self.board.highestTile()[0] < 256:
					# d = self.expectimax(2)
				# else:
					# d = self.minimax(3)
					
				if self.board.emptyTiles()<=7:
					d = self.minimax(7)
				else:
					d=self.expectimax(2)	
				
				if d:
					self.board.move(d)
					self.board.tileGen(1)
				else:
					break
				# if self.board.highestTile()[0] >= 512:

				# raw_input(' ')
			return self.board.score()
			
			
			
	def minimax(self, depth):
		vals = {}
		moves = ['up','left','right','down']
		depth = 2*depth
		alpha = float('-inf')
		beta = float('inf')
		for m in moves:
			b = copy.deepcopy(self.board)
			if b.move(m):
				vals[m] = self.value(b, depth, alpha, beta)
		
		if vals:
			return max(vals, key=vals.get)
		else:
			return None
			
			
			
	def value(self, b, depth,alpha, beta):
		if depth == 1:
			return self.evalfn(b)
		
		# b = copy.deepcopy(b)
		if depth%2==0:
			return self.minval(b,depth-1, alpha, beta)
		else:
			return self.maxval(b,depth-1, alpha, beta)
	
	
	
	def maxval(self,state,depth,a,b):
		v = float('-inf')
		moves = ['up','left','right','down']
		
		for m in moves:
			s1 = copy.deepcopy(state)
			i = 0
			# while True:
				# if s1.move(m):
					# v = max(v,self.emvalue(s1, depth))
					# break
				# else:
					# if not s1.filled() and s1.highestTile() > 512 and i < 1:
						# i += 1
						# s1 = copy.deepcopy(s1)
						# s1.tileGen(1)
					# else:
						# break
			if s1.move(m):
				v = max(v,self.emvalue(s1, depth))
				
			if v >= b:
				return v
			a = max(a,v)
		return v
		
	def minval(self, state, depth, a, b):
		v = float('inf')		
		empty = state.emptyTiles()
		for pos in empty:
			s1 = copy.deepcopy(state)
			s1.tileGen(1,pos)
			v = min(v,self.value(s1, depth,a,b))
			
			if v <= a:
				return v
			b = min(b,v)
			
		return v
		
	def expectimax(self, depth):
		vals = {}
		moves = ['up','left','right','down']
		depth = 2*depth	
		
		for m in moves:
			b = copy.deepcopy(self.board)
			if b.move(m):
				vals[m] = self.emvalue(b, depth)
		
		if vals:
			return max(vals, key=vals.get)
		else:
			return None
			
			
			
	def emvalue(self, b, depth):
		if depth == 1:
			return self.evalfn(b)
		
		# b = copy.deepcopy(b)
		if depth%2==0:
			return self.expval(b,depth-1)
		else:
			return self.emaxval(b,depth-1)
	
	
	
	def emaxval(self,state,depth):
		v = float('-inf')
		moves = ['up','left','right','down']
		
		for m in moves:
			s1 = copy.deepcopy(state)
			i = 0
			# while True:
				# if s1.move(m):
					# v = max(v,self.emvalue(s1, depth))
					# break
				# else:
					# if not s1.filled() and s1.getEmptyCells() > 4 and s1.highestTile()[0] > 512 and i < 1:
						# s1 = copy.deepcopy(s1)
						# s1.tileGen(1)
						# i += 1
					# else:
						# break
			if s1.move(m):
				v = max(v,self.emvalue(s1, depth))
		return v
		
	def expval(self, state, depth):
		v = 0
		empty = state.emptyTiles()
		for pos in empty:
			s1 = copy.deepcopy(state)
			s1.tileGen(1,pos)
			v += (self.emvalue(s1, depth))*(1.0/len(empty))
			
		return v
			
		
	
		
	def evalfn(self, b2, p=False):
		mono = b2.monotonicity3()
		smooth = b2.smoothness8()
		empty = -1000+6*b2.getEmptyCells()
		o,n = b2.score(2)
		high = b2.highestTile()
		high_row = b2.getCells(row=high[1],column=None)
		temp = [0,0]
		for x in range(3):
			if high_row[x]>=high_row[x+1]:
				temp[0] += 1
			else:
				temp[1] += 1
		blocked = 0
		bonus = 0
		# if p:
			# print 'high row', high_row
			# print 'temp',temp
		if temp[1]==0:
			blocked = 100
			if 0 in high_row and high_row[3] != 0:
				blocked -= 150
		else:
			blocked = -200
		# if p:
			# print 'blockd1', blocked 
		
		# else:
			# bonus += 100
		# blocked += bonus
		
		# if p:
			# print 'blocked2', blocked
		# temp = 2.7*b2.getEmptyCells() + mono + math.log(b2.highestTile()[0]) + 0.1*smooth# - 2.7*ai.manhatDist(b2.highestTile())
		# empty = b2.getEmptyCells()
		# if empty/4==3:
			# empty = 0
		# else:
			# empty = 12*(-800+6*empty)
		deathPenalty = 0
		if b2.filled() and not b2.canMove():
			deathPenalty = -10000000
		
		corner = ai.atCorner(high)
		eW = 0
		if (b2.board[0][2] != 0 and b2.board[0][3] != 0 and high > 128):
			two = math.log(b2.board[0][2],2)
			three = math.log(b2.board[0][3],2)
			
			if two-three >= 5:
				eW = -3
		bw = 80.
		acw = 4.
		ew = 22.
		mw = 10.
		scw = 0.
		sw = 1.
		# if b2.getEmptyCells()<2:
			# ew += 10
			# bw -= 15
		if high[0] < 8193:
			# temp = 3*blocked + 4*ai.atCorner(high) + 18*empty + 2.3*mono + 1*(n-o) + 1.*smooth
			temp = bw*blocked + acw* + ew*empty + mw*mono + scw*(n-o) + sw*smooth+deathPenalty
			# temp = mono + deathPenalty + b2.sm()
			
			# temp = 4*blocked + 5.7*ai.atCorner(high) + 17*empty + 10.3*mono  + 1.11*smooth + deathPenalty#+ 1.12**(n-o)
		else:
			##### most recent
			temp = 3*blocked + 4*ai.atCorner(high) + 25.5*empty + 2.8*smooth+ 1.8*mono
			##### most recent
		# else:
			# temp = b2.sm() + 0.005*empty
		# if p:
			# print 'blocked:',bw*blocked
			# print 'corner', acw*corner
			# print 'empty', ew*empty
			# print 'mono', mw*mono
			# print 'score', scw*(n-o)
			# print 'smooth', sw*smooth
			
		return temp
			

			
if __name__ == '__main__':

	parser = argparse.ArgumentParser(description='Your favourite 2048 now in the terminal! Play it or have an AI solve it for you')
	parser.add_argument('--ai', action='store_true', help='AI Flag')
	parser.add_argument('--step', action='store_true', help='Run the AI Step by Step')
	args = parser.parse_args()

	g = Game(ai = args.ai, step = args.step)
	score = g.game()
	if score == None:
		print 'Game abandoned'
	print "Game Finished, Score :",score