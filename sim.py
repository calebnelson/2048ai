from ailookahead import AiLookahead
from aibasic import AiRand, AiLeft
from aiquality import AiQuality
from aiapi import AiRequest, AiResponse
from board import Board

if __name__ == "__main__":
	aireq = AiRequest({'board':"2,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0", 'gid':1, 'prior':""})
	moveNum = 0
	lines = []
	f = open(str(aireq.gid)+".txt", "w+")
	while (True):
		moveNum += 1
		airesp = AiQuality(aireq)
		aireq.b = aireq.b.move(airesp.dir)
		lines.append(str(moveNum) + "," + str(aireq.b) + "," + str(airesp.dir))
		aireq.b = aireq.b.drop()
		if (aireq.b.canMove() == False):
			break
	for i in range(0, len(lines)):
		lines[i] = lines[i] + "," + str(len(lines)-(i+1)) + "," + str(aireq.b.score) + "\n"
		f.write(lines[i])
	f.write(str(moveNum+1) + "," + str(aireq.b) + ",final")
	f.close()
