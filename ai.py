import math,copy


def manhatDist(cell1):
	x1 = cell1[1]
	y1 = cell1[2]
	if x1<2:
		x2 = 0
	else:
		x2 = 3
		
	if y1>=2:
		y2 = 3
	else:
		y2 = 0
	return abs(x1-x2)+abs(y1-y2)
	
def scoreWeight(diff):
	return 0.2*diff if diff<50 else diff
	# return 0
	
def atEdge(highest_old, highest_new):
	score = -30
	
	h_ov = highest_old[0]
	h_nv = highest_new[0]
	
	if h_nv == h_ov:
		if atCorner(highest_new):
			return 40
	else:
		if atCorner(highest_new):
			return 80
	
	return score
	
	
	
	
	
def atCorner(highest):
	score = -1600*highest[0]
	
	if highest[1]==0 or highest[1]==3:
		if highest[2]==0 or highest[2]==3:
			return highest[0]*300
		return score
	return score
	
	
	
	
