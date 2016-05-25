from __future__ import print_function
from random import randint,seed,sample
import math
import copy

# seed(10929)
# seed (10022)
# seed(34740)

class Board(object):


	m = {'up':-1,'down':1,'right':1,'left':-1}
	o = {'up':1,'down':2,'right':2,'left':1}
	vectors = {'up':[-1,0],'down':[1,0],'right':[0,1],'left':[0,-1]}

	def __init__(self,board):
	
		self.size = 4
		self.rows = 4
		self.columns = 4
		self.__score = 0
		self.__oscore = 0
		self.__goal = 2048
		self.__won = False
		self.__highest = [0,None,None]
		# self.board = [[1,0,1,0],[0,1,0,1],[1,0,1,0],[0,1,0,1]]
		self.board = board
		# print(self.board)
		self.initState()


		
	def initState(self):
		'''defines the initial state of the game'''
		

		n_tiles = 2
		
		self.tileGen(n_tiles,pos=None, tile=None)
		self.drawBoard()


		
	def tileGen(self, n, pos = None,tile= None):
		'''generates a tile at a random location'''
		cells = self.getCells()
		if not tile:
			x = randint(1,100)
			tile=4 if x%10==0 else 2
			
			
		e = self.emptyTiles()
		if not e:
			return False
		if pos==None:
			while not n==0:
				
				cell = sample(e,1)[0]
				row = cell[0]
				column = cell[1]

				
				if not cells[row][column]:
					self.setCells(tile,row,column)				
				
					n = n-1
					
					if not n==0:
						x = randint(1,100)
						tile=4 if x%20==0 else 2
							
					else:
						break
		else:
			self.setCells(tile,pos[0],pos[1])
		# self.drawBoard(self.board)

		
		
	def getCells(self, row=None,column=None):
		if (column==None and row==None):
			return self.board
			
		elif row==None:
			return [self.board[i][column] for i in range(self.rows)]
		
		elif column==None:
			return [self.board[row][i] for i in range(self.columns)]
		
		else:
			return self.board[row][column]
		

		
	def setCells(self, tile, row, column):
		if row!=None and column!=None:
			self.board[row][column] = tile
		
		elif row==None:
			for i in range(self.rows):
				self.board[i][column] = tile
				return
				
		elif column==None:
			for i in range(self.columns):
				self.board[row][i] = tile
				return
				
		else:
			self.board = tile
	
	
	def won(self):
		return self.__won
	
	
	def goal(self):
		return self.__goal
		
	def score(self,num=None):
		if not num:
			return self.__score
		else:
			return self.__score, self.__oscore
	
	def filled(self):
	
		b = self.getCells()
		for row in range(self.rows):
			for column in range(self.columns):
				if not [row][column]:
					return False
	
		return True
		
	def highestTile(self):
		b = self.board
		temp = [0,None,None]
		
		for i in range(self.rows):
			for j in range(self.columns):
				if b[i][j] > temp[0]:
					temp[0]=b[i][j]
					temp[1],temp[2] = i,j

		self.__highest = temp
		return self.__highest
	
	def emptyTiles(self):
		b = self.board
		empty=[]
		for x in range(self.rows):
			for y in range(self.columns):
				if b[x][y]==0:
					empty.append([x,y])
		return empty
	
	def canMove(self):
		
		
		if not self.filled():
			return True
		
		rows = self.rows
		columns = self.columns
		
		
		for row in range(rows):
		
			for column in range(columns):
				
				curr_cell = self.getCells(row,column)
				next_cell_col = self.getCells(row, column+1)
				next_cell_row = self.getCells(row+1, column)
				
				if (row<(rows-1) and curr_cell == next_cell_row) or (row<(rows-1) and curr_cell == next_cell_row):
					return True
					
		return False


		
	def drawBoard(self):
		board = self.board
		count = 0
		for row in board:
			for tile in row:
						
				print  ('.' if tile==0 else str(tile),end = '\t')
				count = count+1
				if count == self.columns:
					print ('\n')
					count=0
					
	
	def getEmptyCells(self):
		return len([self.board[i][j] for i in range(self.rows) for j in range(self.columns) if self.board[i][j] == 0])
	
	
	def getVectors(self,dir):
		v = Board.vectors
		return v[dir]
					
	def move(self, dir):
		old = copy.deepcopy(self.board)
		movem = Board.m[dir]
		origin = Board.o[dir]
		comb = [0,0,0,0]

		for i in range(self.size):
		
			if dir=='up' or dir=='down':
				curr_line = self.getCells(None,i)
			
			else:
				curr_line = self.getCells(i,None)
				
			for j in range(origin, origin-(3*movem),-movem):

				if curr_line[j] == 0:
					continue
					
				n = movem
				while True:
					
					curr_cell = curr_line[j]
					curr_comp = curr_line[j+n]
					
					if not (curr_comp==0):

						if curr_cell==curr_comp and not comb[j+n]:
														
							curr_line[j+n] = curr_comp*2							
							curr_line[j] = 0
							comb[j+n]=1
							self.__oscore = self.__score
							self.__score += curr_comp*2
							break
					
						elif not curr_line[j+n-movem]==curr_cell:
							
							curr_line[j+n-movem] = curr_cell
							curr_line[j] = 0
							break
						
						break
					
					elif curr_comp==0 and ((movem==-1 and (j+n)==0) or (movem==1 and (j+n)==3)):
						
						curr_line[j+n] = curr_cell
						curr_line[j]=0
						break
					
					else:
						
						n = (abs(n)+1)*movem
						continue
			
			for k in range(self.columns):
				if dir=='up' or dir=='down':
					self.board[k][i] = curr_line[k]
				else:
					self.board[i][k] = curr_line[k]
			
			comb=[0,0,0,0]
		
		if self.highestTile()[0] == self.__goal:
			self.__won == True
			
		if old == self.board:
			return False
		
		return True
	
	def traverse(self,init,dir,reverse=False):
		a=1
		if reverse:
			a = -1
		x = init[0]
		y = init[1]
		return [x+(a*dir[0]),y+(a*dir[1])]
		
		
	def end(self,dir,next):
		x = next[0]
		y = next[1]
		if dir==[0,1]:
			return True if y>=self.rows-1 else False
			
		elif dir==[0,-1]:
			return True if y<=0 else False
			
	
	# def monotonicity(self):
		# dirs = ['right', 'down', 'left', 'down', 'right', 'down', 'left']
		# init = [0,0]
		# weights = [0,0,0,0]
		# smoothness = 0
		# board = copy.deepcopy(self.board)
		
			
		# for i in range(self.rows):
			# curr=0
			# next=curr+1
			# while next<self.rows:
				
				# while next<self.rows and board[i][next]==0:
					# next = next+1
					
				# if next>=self.rows:
					# next=next-1 
					
				# curr_val = math.log(1+board[i][curr],2)
				
				# next_val = math.log(1+board[i][next],2)
					
				
					
				# if curr_val>next_val:
						# weights[0] = weights[0] - (curr_val - next_val)

				# elif curr_val<next_val:
					# weights[1] = weights[1] - (next_val - curr_val)
				
				# smoothness -= abs(curr_val - next_val)
				
				# curr = next
				# next = curr+1
				
		# for i in range(self.columns):
			# curr=0
			# next=curr+1
			# while next<self.columns:
				
				# while next<self.columns and board[i][next]==0:
					# next = next+1
					
				# if next>=self.columns:
					# next=next-1 
					
				# curr_val = math.log(1+board[i][curr],2)
				
				# next_val = math.log(1+board[i][next],2)
					
				
					
				# if curr_val>next_val:
						# weights[2] = weights[2] - (curr_val - next_val)

				# elif curr_val<next_val:
					# weights[3] = weights[3] - (next_val - curr_val)
				
				# smoothness -= abs(curr_val - next_val)
				
				# curr = next
				# next = curr+1
				
				
		# return max(weights[0],weights[1])+max(weights[2],weights[3]),smoothness

	def monotonicity3(self):
		r = 0.125
		n = -0.
		dirs = ['right', 'down', 'left', 'down', 'right', 'down', 'left']
		# dirs = ['right', 'down', 'right', 'down', 'right','down','right']
		curr = [0,0]
		sum = 0
		b = self.board
		i=0
		for dir in dirs:
			
			dir = self.getVectors(dir)
			
			if dir==[0,1] or dir==[0,-1]:
				while not self.end(dir,curr):
					# if i==3 and i==7:
						# i -= 1
						# sum += b[curr[0]][curr[1]]*(r**(n+i))
						# curr = self.traverse(curr,dir)
						# i += 2
					# if i==4 and i==8:
						# i += 2
						# sum += b[curr[0]][curr[1]]*(r**(n+i))
						# curr = self.traverse(curr,dir)
						# i -= 1
					# else:
					sum += b[curr[0]][curr[1]]*(r**(n+i))
					curr = self.traverse(curr,dir)
					i += 1
					# print (sum)
				
				
			else:
				# print(b[curr[0]][curr[1]])
				# sum += b[curr[0]][curr[1]]*(r**(n+i))
				curr = self.traverse(curr,dir)
				i -= 1 
				# print (sum)
		return sum
		
		
	def monotonicity2(self):
		dirs = ['right', 'down', 'left', 'down', 'right', 'down', 'left']
		init = [0,0]
		weights = [0,0]
		smoothness = 0
		for dir in dirs:
			dir = self.getVectors(dir)
			next = self.traverse(init, dir)
			# print('dir=',dir)
			# print('init=',init)			
			# print('next=',next)
			if dir==[0,1] or dir==[0,-1]:
				while not self.end(dir,next):
					try:
						while not self.end(dir,next) and not self.getCells(next[0],next[1]):
						
							next = self.traverse(next,dir)
							# print('next=',next)
					except:
						break
					# print(init)
					# print(next)
					curr_cell = 1+self.getCells(init[0],init[1])
					next_cell = 1+self.getCells(next[0],next[1])
										
					# curr_cell = self.getCells(init[0],init[1])
					# next_cell = self.getCells(next[0],next[1])
					# print('curr_cell=',2**curr_cell)
					# print('next_cell=',2**next_cell)
					# raw_input(' ')
					diff = curr_cell/next_cell
					
					if curr_cell>next_cell:
						weights[0] += diff
					elif curr_cell<next_cell:
						weights[1] -= diff
					
					
					init = next
					next = self.traverse(next,dir)
					# print('end')
					# print('init=',init)
					# print('next=',next)
					# raw_input(' ')
				# print('flow finished')
				init = self.traverse(next,dir,reverse = True)
				# init[0] += 1
				# print('new init=',init)
				# raw_input(' ')
			
			else:
				curr_cell = math.log(1+self.getCells(init[0],init[1]),2)
				next_cell = math.log(1+self.getCells(next[0],next[1]),2)
				# print('curr_cell=',2**curr_cell)
				# print('next_cell=',2**next_cell)
				# raw_input(' ')	
				diff = curr_cell-next_cell
					
				if curr_cell>next_cell:
					weights[0] += diff
				elif curr_cell<next_cell:
					weights[1] -= diff
				
				
				init = next
				
		return abs(weights[0]-weights[1])
		
		
	def smoothness(self):
		b = self.board
		smoothness = 0
		for x in range(self.rows):
			for y in range(self.columns):				
				
				if x==3 and y==3:
					break
				
				if x == 3:
					smoothness += b[x][y] - b[x][y+1]
					continue
					
				if y == 3:
					smoothness += b[x][y] - b[x+1][y]
					continue
					
				smoothness += b[x][y] - b[x+1][y] - b[x][y+1]
				
		return -abs(smoothness)
		
	def smoothness8(self):
		b = self.board
		diff=0
		subtrahend = []
		
		for x in range(self.rows):
			for y in range(self.columns):
				
				if y != 3:
					subtrahend.append(b[x][y+1])
					
				if x != 3:
					subtrahend.append(b[x+1][y])
				
				if x != 3 and y != 3:
					subtrahend.append(b[x+1][y+1])
				
				if x != 3 and y != 0:
					subtrahend.append(b[x+1][y-1])
					
					
				diff += b[x][y]-sum(subtrahend)
				subtrahend=[]
			
		return -abs(diff)

	def manhatD(self,t1,t2):
		return abs(t1[0]-t2[0])+abs(t1[1]-t2[1])
	
	def getTiles(self,value):
		t = []
		for x in range(self.rows):
			for y in range(self.columns):
				v = self.getCells(x,y)
				if v == math.pow(2,value):
					t.append([x,y])
		return t
	
	def sm(self):
		# self.board = [[128,64,32,16],[64,32,16,8],[32,16,8,4],[16,8,4,2]]
		h = self.highestTile()
		# print (h[0])
		h[0] = int(math.log(h[0],2))
		# print (h[0])
		# self.drawBoard(self.board)
		ts = 0
		# for j in range(0,4):
		j = 0
		c = 0
		for i in range(h[0],0,-1):
			# raw_input("row "+str(j))
			# raw_input("Tiles "+str(int(math.pow(2,i))))
			t = self.getTiles(i)
			# raw_input(t)
			if not t: 
				# raw_input("None")
				continue
			
			for tile in t:
				row = j
				col = 0+c
				# raw_input(tile)
				while row>=0 and col>=0:
					# raw_input("row="+str(row)+"\ncol="+str(col))
					d = self.manhatD([row,col],tile)
					# raw_input("d="+str(d))
					if d==0:
						ts -= row+col-15
						# raw_input("ts="+str(ts))
						break
					ts += -d*(3-row-col)
					# raw_input("ts="+str(ts))

					row -= 1
					col += 1
			j += 1
			if j>3:
				c += 1
				j=3

		return ts
