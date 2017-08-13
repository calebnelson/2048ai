# Define some basic AIs: rand, left
#
from aiapi import AiRequest, AiResponse, DirectionMap
from random import randint

def AiRand(aireq):
	dir = DirectionMap[randint(0, 3)]
	while(aireq.b.tryDir(dir) == False):
		dir = DirectionMap[randint(0, 3)]
	return AiResponse(dir, "rand " + str(aireq))

def AiLeft(aireq):
	# helper that returns true if r1,c1 can move onto r0,c0

	# Try left
	if (aireq.b.tryDir("left")):
		return AiResponse("left")

	# Try up
	if (aireq.b.tryDir("up")):
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
