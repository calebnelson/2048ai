from aiapi import AiRequest, AiResponse, DirectionMap

def AiScore(aireq):
	possibleBoards = [Board(None), Board(None), Board(None), Board(None)]
	highestScore = -1
	highestIndex = -1
	for i in range(0, 4):
		possibleBoards[i] = aireq.b.move(DirectionMap[i])
		if (possibleBoards[i].score > highestScore):
			highestScore = possibleBoards[i].score
			highestIndex = i
	return AiResponse(DirectionMap[highestIndex], "with a potential score of " + str(highestScore))