from types import *
class Board:
	board  = []

	def __init__(self, grid = None):
		self.board = []
		if (grid == None):
			grid = "2,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0"
		if (type(grid) is ListType):
			self.board = grid
		else:
			grid = map(int, grid.replace(' ', '').split(','))
			if len(grid) < 16:
				grid.extend([0 for x in range(16-len(grid))])
			for row in range(0, 4):
				self.board.append(grid[4*row:4*(row+1)])

	def __str__(self):
	    rowStrs = []
	    for row in self.board:
	      rowStrs.append(','.join(map(str, row)))
	    return ("[" + '|'.join(rowStrs) + "]")

	def moveOk(self, r0, c0, r1, c1):
		a = self.board[r0][c0]
		b = self.board[r1][c1]
		return (a == 0 and b != 0) or (a != 0 and a == b)

	def tryDir(self, dir):
		if (dir == 'l' or dir == "left"):
			for row in range(0,4):
				for col in range(0, 3):
					if (self.moveOk(row, col, row, col+1)):
						return True
		elif (dir == 'u' or dir == "up"):
			for col in range(0, 4):
				for row in range(0, 3):
					if (self.moveOk(row, col, row+1, col)):
						return True
		elif (dir == 'r' or dir == "right"):
			for row in range(0,4):
				for col in range(1, 4):
					if (self.moveOk(row, col, row, col-1)):
						return True
		elif (dir == 'd' or dir == "down"):
			for col in range(0, 4):
				for row in range(1, 4):
					if (self.moveOk(row, col, row-1, col)):
						return True
		return False

	def move(self, dir):
		newboard = Board(self.board)
		if (not self.tryDir(dir)):
			return newboard
		else:
			if (dir == 'l' or dir == "left"):
				for row in range(0,4):
					for c in range(0, 3):
						col = 2 - c
						if (newboard.moveOk(row, col, row, col+1)):
							newboard.board[row][col] = newboard.board[row][col] + newboard.board[row][col+1]
							newboard.board[row][col+1] = 0
			elif (dir == 'u' or dir == "up"):
				for col in range(0, 4):
					for r in range(0, 3):
						row = 3 - r
						if (self.moveOk(row, col, row+1, col)):
							newboard.board[row][col] = self.board[row][col] + self.board[row+1][col]
                                                        newboard.board[row+1][col] = 0
			elif (dir == 'r' or dir == "right"):
				for row in range(0,4):
					for col in range(1, 4):
						if (self.moveOk(row, col, row, col-1)):
                                                        newboard.board[row][col] = self.board[row][col] + self.board[row][col-1]
                                                        newboard.board[row][col-1] = 0
			elif (dir == 'd' or dir == "down"):
				for col in range(0, 4):
					for row in range(1, 4):
						if (self.moveOk(row, col, row-1, col)):
                                                        newboard.board[row][col] = self.board[row][col] + self.board[row-1][col]
                                                        newboard.board[row-1][col] = 0
			return newboard


if __name__ == "__main__":
	testb = Board("2,2,0,0, 0,2,0,4, 0,0,0,0, 0,0,0,0")
	print testb.tryDir("left")
	print str(testb)
	print str(testb.move("left"))
