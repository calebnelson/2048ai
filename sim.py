from ailookahead import AiLookahead
from aibasic import AiRand, AiLeft
from aiquality import AiQuality
from aitensorflow import AiTensorFlow
from aiapi import AiRequest, AiResponse
from board import Board
from quality import Model
import sys

if __name__ == "__main__":
    m = Model("mnist-model.meta")
    print "model loaded"
	aireq = AiRequest({'board':"2,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0", 'gid':1, 'prior':""})
	moveNum = 0
	lines = []
	while (True):
		moveNum += 1
        #sys.stdout.write(str(moveNum) + str(aireq.b))
		airesp = AiQuality(aireq, m)
		aireq.b = aireq.b.move(airesp.dir)
		lines.append(str(moveNum) + "," + str(aireq.b) + "," + str(airesp.dir))
		aireq.b = aireq.b.drop()
		if (aireq.b.canMove() == False):
			break
	for i in range(0, len(lines)):
		lines[i] = lines[i] + "," + str(len(lines)-(i+1)) + "," + str(aireq.b.score) + "\n"
		sys.stdout.write(lines[i])
