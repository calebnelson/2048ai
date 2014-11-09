# Define some basic AIs: rand, left
#
from aiapi import AiRequest, AiResponse, DirectionMap
from random import randint

def AiRand(aireq):
	dir = DirectionMap[randint(0, 3)]
	return AiResponse(dir, "rand " + str(aireq))

def AiLeft(aireq):
	# helper that returns true if r1,c1 can move onto r0,c0
	def moveOk(r0, c0, r1, c1):
		a = aireq.board[r0][c0]
		b = aireq.board[r1][c1]
		return (a == 0 and b != 0) or (a != 0 and a == b)

	# Try left
	for row in range(0,4):
		for col in range(0, 3):
			if (moveOk(row, col, row, col+1)):
			return AiResponse("left")

	# Try up
	for col in range(0, 4):
		for row in range(0, 3):
			if (moveOk(row, col, row+1, col)):
			return AiResponse("up")

	# Randomly pick down or right
	dr = ['down', 'right']
	return AiResponse(dr[randint(0,1)], "rand(d|r)")

# For testing
if __name__ == "__main__":
  r1 = AiRequest({'board':'4,4,8,0, 0,4,0,0', 'prior':'lu', 'drop':'1,1,4'})
  r2 = AiRequest({'board':'4,8,2,0, 4,0,0,0', 'prior':'rd', 'drop':'0,2,2'})
  print
  print "Test Rand: " + str(r1)
  print "Response:  " + str(AiRand(r1))
  print
  print "Test Left 1: " + str(r1)
  print "Response:  " + str(AiLeft(r1))
  print
  print "Test Left 2: " + str(r2)
  print "Response:  " + str(AiLeft(r2))	