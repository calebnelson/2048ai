from aiapi import AiRequest, AiResponse
from aibasic import AiLeft

def AiCorner(aireq):
	
	def moveOk(r0, c0, r1, c1):
		a = aireq.board[r0][c0]
		b = aireq.board[r1][c1]
		return (a == 0 and b != 0) or (a != 0 and a == b)

	def tryDir(dir):
		if (dir == 'l' or dir == "left"):
			for row in range(0,4):
				for col in range(0, 3):
					if (moveOk(row, col, row, col+1)):
						return True
		if (dir == 'u' or dir == "up"):
			for col in range(0, 4):
				for row in range(0, 3):
					if (moveOk(row, col, row+1, col)):
						return True
		if (dir == 'r' or dir == "right"):
			for row in range(0,4):
				for col in range(1, 4):
					if (moveOk(row, col, row, col-1)):
						return True
		if (dir == 'd' or dir == "down"):
			for col in range(0, 4):
				for row in range(1, 4):
					if (moveOk(row, col, row-1, col)):
						return True
		return False

	priority = { 'up':"lurd", 'right':"lurd", 'down':"uldr", 'left':"uldr" }
	name = { 'u':'up', 'r':'right', 'd':'down', 'l':'left' }
	if (len(aireq.prior) == 0):
		return AiLeft(aireq)
	for d in priority[aireq.prior[0]]:
		if tryDir(d):
			return AiResponse(name[d])
