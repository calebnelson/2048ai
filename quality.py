from board import Board
import math
import tensorflow as tf
import numpy as np

class Model:
        def __init__(self, name):
                self.sess = tf.Session()
                self.saver = tf.train.import_meta_graph(name)
                self.saver.restore(self.sess, tf.train.latest_checkpoint('./'))
                self.W = np.array(self.sess.run("W:0"))
                self.bias = np.array(self.sess.run("b:0"))

#returns the quality of board b
def oldquality(b):
	cp = []
	magic = 17.0
	for i in range(0, 17):
		cp.append(math.log(magic-i))
	#map score from f[0] = 99%, f[16]=20%
	cp0, cp16, minp, maxp = cp[0], cp[16], .20, .99
	slope = (maxp-minp) / (cp0 - cp16)
	for i in range(0, 17):
		cp[i] = slope * (cp[i] - cp16) + minp
	drops = b.possibleDrops()
	return (b.score * cp[16-len(drops)])

def tfquality(b, m):
        barray = np.array(b.board).flatten()
        probs = tf.nn.softmax(np.add(np.dot(m.W, barray), m.bias)).eval(session=m.sess).reshape(1, 16)
        labels = np.array([np.arange(1,17)]).reshape((16, 1))
        return np.dot(probs, labels).astype(float)
        
def quality(b):
	quality = 0
	for i in range(0, 4):
		for j in range(0, 4):
			if (b.board[i][j] == 0 or 
				((i != 3 and b.moveOk(i+1, j, i, j)) or 
				(j != 3 and b.moveOk(i, j+1, i, j)))):
				quality += 1
	return quality

# For testing
if __name__ == "__main__":
	testb = Board("0,0,0,0, 0,0,0,0, 2,8,0,0, 16,4,2,4", 60)
        print tfquality(testb)
