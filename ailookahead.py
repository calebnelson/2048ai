from aiapi import AiRequest, AiResponse, DirectionMap
from board import Board

def AiLookahead(aireq):
	return AiResponse(scanBoard(aireq.b, int(aireq.arg)))	

#samples depth drops and returns the average quality of the resulting boards
def scanDrops(b, depth):
	if (depth <= 0 or len(b.possibleDrops()) == 0):
		return b.quality()
	else:
		qual = 0
		for i in range (0, depth):
			qual += b.move(scanBoard(b.drop(), depth)).quality()
		return (qual / depth)

#scans all directions and returns the best one
def scanBoard(b, depth):
	possibleBoards = [Board(None), Board(None), Board(None), Board(None)]
	qualities = [0, 0, 0, 0]
	best = 0
	for i in range (0, 4):
		possibleBoards[i] = b.move(DirectionMap[i])
		if (b.tryDir(DirectionMap[i])):
			qualities[i] = scanDrops(b.move(DirectionMap[i]), depth-1)
	for i in range (1, 4):
		if (qualities[i] > qualities[best]):
			best = i
	return DirectionMap[best]

if __name__ == "__main__":
  r1 = AiRequest({'board':"0,0,0,0, 0,0,0,0, 2,8,0,0, 16,4,2,4", 'arg':3, 'score':60, 'prior':'lu', 'drop':'1,1,4'})
  print
  print "Test: " + str(r1)
  print "Response:  " + str(AiLookahead(r1))
  print