from board import Board
import math

#returns the quality of board b
def oldquality(b):
	cp = []
	magic = 17.0
	for i in range(0, 17):
		cp.append(math.log(magic-i))
	#map score from f[0] = 99%, f[16]=20%
	cp0, cp16, minp, maxp = cp[0], cp[16], .20, .99
	slope = (maxp-minp) / (cp0 - cp16)
	for i in range(0, 17):
		cp[i] = slope * (cp[i] - cp16) + minp
	drops = b.possibleDrops()
	return (b.score * cp[16-len(drops)])

def quality(b):
	quality = 0
	for i in range(0, 4):
		for j in range(0, 4):
			if (b.board[i][j] == 0 or 
				((i != 3 and b.moveOk(i+1, j, i, j)) or 
				(j != 3 and b.moveOk(i, j+1, i, j)))):
				quality += 1
	return quality

# For testing
if __name__ == "__main__":
	testb = Board("0,0,0,0, 0,0,0,0, 2,8,0,0, 16,4,2,4", 60)
	print newquality(testb)
