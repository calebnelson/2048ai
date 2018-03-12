from aiapi import AiRequest, AiResponse, DirectionMap
from board import Board
from quality import quality

def AiQuality(aireq):
	possibleBoards = [Board(None), Board(None), Board(None), Board(None)]
	choice = (-1,-1) #choice[0] is the highest quality, choice[1] is the direction you have to move to achieve that quality
	for i in range(0, 4):
		possibleBoards[i] = aireq.b.move(DirectionMap[i])
		if (choice == (-1,-1)):
			if (aireq.b.tryDir(DirectionMap[i])):
				choice = (quality(possibleBoards[i]), i)
		elif (quality(possibleBoards[i]) > choice[0]):
			choice = (quality(possibleBoards[i]), i)
	return AiResponse(DirectionMap[choice[1]], "with a potential quality of " + str(choice[0]))

if __name__ == "__main__":
  r1 = AiRequest({'board':"0,0,0,0, 0,0,0,0, 2,8,0,0, 16,4,2,4", 'score':60, 'prior':'lu', 'drop':'1,1,4'})
  print
  print "Test: " + str(r1)
  print "Response:  " + str(AiQuality(r1))
  print
