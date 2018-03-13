from aiscore import AiScore
#from aiquality import AiQuality
from aiapi import AiRequest
#from quality import Model
#import sys

if __name__ == "__main__":
	aireq = AiRequest({'board':"2,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0", 'gid':1, 'prior':""})
	moveNum = 0
	score = 0
	scoreDiff = 0
	lines = []
	while (True):
		moveNum += 1
		airesp = AiScore(aireq)
		aireq.b = aireq.b.move(airesp.dir)
		scoreDiff = aireq.b.score - score
		score = aireq.b.score
		line = str(aireq.b.board) + "," + str(airesp.dir) + "," + str(scoreDiff)
		aireq.b = aireq.b.drop()
		line = line + "," + str(aireq.b.board) + "," + str(1 if aireq.b.canMove() else 0)
		lines.append(line)
		if (aireq.b.canMove() == False):
			break
	for i in range(0, len(lines)):
		#lines[i] = lines[i] + "," + str(len(lines)-(i+1)) + "," + str(aireq.b.score) + "\n"
		#sys.stdout.write(lines[i])
		print lines[i]
