from aiapi import AiRequest, AiResponse, DirectionMap
from board import Board
from quality import tfquality, Model

def AiTensorFlow(aireq, model):
	possibleBoards = [Board(None), Board(None), Board(None), Board(None)]
	choice = (-1,-1) #choice[0] is the highest quality, choice[1] is the direction you have to move to achieve that quality
	for i in range(0, 4):
		possibleBoards[i] = aireq.b.move(DirectionMap[i])
                qual = tfquality(possibleBoards[i], model)
		if (choice == (-1,-1)):
			if (aireq.b.tryDir(DirectionMap[i])):
				choice = (qual, i)
		elif (aireq.b.tryDir(DirectionMap[i]) and qual > choice[0]):
			choice = (qual, i)
	return AiResponse(DirectionMap[choice[1]], "with a potential quality of " + str(choice[0]))

if __name__ == "__main__":
  r1 = AiRequest({'board':"4,8,2,2, 2,4,8,8, 8,16,32,16, 16,32,64,32", 'score':60, 'prior':'lu', 'drop':'1,1,4'})
  m = Model("mnist-model.meta")
  print "Test: " + str(r1)
  print "Response:  " + str(AiTensorFlow(r1, m))
