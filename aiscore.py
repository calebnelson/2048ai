from aiapi import AiRequest, AiResponse, DirectionMap
from board import Board

def AiScore(aireq):
	possibleBoards = [Board(None), Board(None), Board(None), Board(None)]
	choice = (-1,-1) #choice[0] is the best score, choice[1] is the direction you have to move to achieve that score
	for i in range(0, 4):
		possibleBoards[i] = aireq.b.move(DirectionMap[i])
		if (choice == (-1,-1)):
			if (aireq.b.tryDir(DirectionMap[i])):
				choice = (possibleBoards[i].score, i)
		elif (possibleBoards[i].score > choice[0]):
			choice = (possibleBoards[i].score, i)
	return AiResponse(DirectionMap[choice[1]], "with a potential score of " + str(choice[0]))

if __name__ == "__main__":
  r1 = AiRequest({'board':"0,0,0,0, 0,0,0,0, 2,8,0,0, 16,4,2,4", 'score':60, 'prior':'lu', 'drop':'1,1,4'})
  print
  print "Test: " + str(r1)
  print "Response:  " + str(AiScore(r1))
  print