import csv
import sys
import tensorflow as tf
from collections import Counter

class Board:
    def __init__(self, row):
       self.dir = row[18]
       row[18] = 0
       rowi = [ int(n) for n in row ]
       self.level = rowi[0]
       self.board = rowi[1:17]
       self.curScore = rowi[17]
       self.remainingMoves = rowi[19]
       self.maxScore = rowi[20]
class Column:
   def __init__(self):
      self.d = Counter()
   def stats(self):
      minV, maxV, meanV, total = 0,0,0,0
      for val,cnt in self.d.items():
         if (total == 0 or val < minV):
            minV = val
         if (total == 0 or val > maxV):
            maxV = val
         total += cnt
         meanV += val*cnt
      return [minV, maxV, meanV/total]

csvfile = open('gtrain.csv', 'rb')
reader = csv.reader(csvfile, delimiter=',', quotechar='|')
cLevel, cMoves, cScore, cMax = Column(), Column(), Column(), Column()
dirs = { 'up':0, 'left':0, 'right':0, 'down':0 }

x = tf.placeholder(tf.float32, [None, 16])
W = tf.Variable(tf.zeros([16, 16]), name='W')
b = tf.Variable(tf.zeros([16]), name = 'b')
y = tf.nn.softmax(tf.matmul(x, W) + b)
y_ = tf.placeholder(tf.float32, [None, 16])
cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=y_, logits=y))
train_step = tf.train.GradientDescentOptimizer(0.5).minimize(cross_entropy)
sess = tf.InteractiveSession()
tf.global_variables_initializer().run()

boards = []
labels = []
i = 0
for row in reader:
    bo = Board(row)
    boards.append(bo.board)
    temp = [0]*16
    temp[(int(bo.maxScore)/1000 - 1)] = 1
    labels.append(temp)
    i += 1
    if (i >= 100):
        sess.run(train_step, feed_dict={x: boards, y_: labels})
        boards = []
        labels = []
        i = 0
sess.run(train_step, feed_dict={x: boards, y_: labels})
boards = []
labels = []
print "Trained."
csvfile.close()

csvfile = open('gtest.csv', 'rb')
reader = csv.reader(csvfile, delimiter=',', quotechar='|')
for row in reader:
    bo = Board(row)
    boards.append(bo.board)
    temp = [0]*16
    temp[(int(bo.maxScore)/1000 - 1)] = 1
    labels.append(temp)
csvfile.close()

correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
print(sess.run(accuracy, feed_dict={x: boards, y_: labels}))

saver = tf.train.Saver({'W': W, 'b': b})
saver.save(sess, 'mnist-model')
