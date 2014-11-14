class Board:
	board  = []

	def __init__(self, grid):
		grid = map(int, grid.replace(' ', '').split(','))
    	if len(grid) < 16:
      		grid.extend([0 for x in range(16-len(grid))])
    	for row in range(0, 4):
      		board.append(grid[4*row:4*(row+1)])

    def __str__(self):
	    rowStrs = []
	    for row in board:
	      rowStrs.append(','.join(map(str, row)))
	    return ("[" + '|'.join(rowStrs) + "]")

	def getSqaure(self, row, col):
		return self.board[row][col]

	def moveOk(self, r0, c0, r1, c1):
		a = self.board[r0][c0]
		b = self.board[r1][c1]
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

	#def previewBoard(self, dir):
	#	newboard = new Board(self.board)
	#	if (!tryDir(dir)):
	#		return board
	#	else:
	#		if (dir == 'l' or dir == "left"):
	#			for row in range(0,4):
	#				for col in range(0, 3):
	#					if (moveOk(row, col, row, col+1)):
	#						board[row][col]
	#		if (dir == 'u' or dir == "up"):
	#			for col in range(0, 4):
	#				for row in range(0, 3):
	#					if (moveOk(row, col, row+1, col)):
	#						return True
	#		if (dir == 'r' or dir == "right"):
	#			for row in range(0,4):
	#				for col in range(1, 4):
	#					if (moveOk(row, col, row, col-1)):
	#						return True
	#		if (dir == 'd' or dir == "down"):
	#			for col in range(0, 4):
	#				for row in range(1, 4):
	#					if (moveOk(row, col, row-1, col)):
	#						return True