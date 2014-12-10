from aiapi import AiRequest, AiResponse, DirectionMap
from board import Board

scanned = 0

def AiLookahead(aireq):
	global scanned
	args = aireq.arg.split(", ")
	print str(args)
	x = (scanBoard(aireq.b, int(args[0])+1, int(args[1])+1))
	numscan = scanned
	scanned = 0
	return AiResponse(x[0], "#B: " + str(numscan) + " Q: " + str(x[1]))

#samples depth drops and returns the average quality of the resulting boards
def scanDrops(b, depth, breadth):
	drops = b.possibleDrops()
	if (depth <= 0 or len(drops) == 0):
		return b.quality()
	else:
		if (breadth <= 0):
			breadth = 1
		qual = 0
		for i in range (0, breadth):
			qual += scanBoard(b.drop(drops), depth, breadth)[1]
		return (qual / breadth)

#scans all directions and returns the best one
def scanBoard(b, depth, breadth):
	global scanned
	scanned += 1
	qualities = [0, 0, 0, 0]
	best = 0
	for i in range (0, 4):
		if (b.tryDir(DirectionMap[i])):
			qualities[i] = scanDrops(b.move(DirectionMap[i]), depth-1, breadth-1)
	for i in range (1, 4):
		if (qualities[i] > qualities[best]):
			best = i
	return (DirectionMap[best], qualities[best])

if __name__ == "__main__":
  r1 = AiRequest({'board':"0,0,0,0, 0,0,0,0, 2,8,0,0, 16,4,2,4", 'arg':"5, 5", 'score':60, 'prior':'lu', 'drop':'1,1,4'})
  print
  print "Test: " + str(r1)
  print "Response:  " + str(AiLookahead(r1))
  print