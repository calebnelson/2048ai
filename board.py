from types import *
import copy
import math

class Board:
    board = []
    score = 0

    def __init__(self, grid = None, scr = None):
        self.board = []
        if (scr == None):
            scr = 0
        self.score = int(scr)
        if (grid == None):
            grid = "2,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0"
        if (type(grid) is ListType):
            self.board = copy.deepcopy(grid)
        else:
            grid = map(int, grid.replace(' ', '').split(','))
            if len(grid) < 16:
                grid.extend([0 for x in range(16-len(grid))])
            for row in range(0, 4):
                self.board.append(grid[4*row:4*(row+1)])

    def __str__(self):
      rowStrs = []
      for row in self.board:
       rowStrs.append(','.join(map(str, row)))
      return ("[" + '|'.join(rowStrs) + "] " + str(self.score))

    def moveOk(self, r0, c0, r1, c1):
        a = self.board[r0][c0]
        b = self.board[r1][c1]
        return (a == 0 and b != 0) or (a != 0 and a == b)

    def tryDir(self, dir):
        if (dir == 'l' or dir == "left"):
            for row in range(0,4):
                for col in range(0, 3):
                    if (self.moveOk(row, col, row, col+1)):
                        return True
        elif (dir == 'u' or dir == "up"):
            for col in range(0, 4):
                for row in range(0, 3):
                    if (self.moveOk(row, col, row+1, col)):
                        return True
        elif (dir == 'r' or dir == "right"):
            for row in range(0,4):
                for col in range(1, 4):
                    if (self.moveOk(row, col, row, col-1)):
                        return True
        elif (dir == 'd' or dir == "down"):
            for col in range(0, 4):
                for row in range(1, 4):
                    if (self.moveOk(row, col, row-1, col)):
                        return True
        return False

    def move(self, dir):
        newboard = Board(self.board)
        newscr = self.score
        if (not self.tryDir(dir)):
            return newboard
        else:
            if (dir == 'l' or dir == "left"):
                for row in range(0, 4):
                    vscore = makeMove(newboard.board[row])
                    newboard.board[row] = vscore[0]
                    newscr += vscore[1]
            elif (dir == 'u' or dir == "up"):
                for col in range(0, 4):
                    vector = []
                    for row in range(0, 4):
                        vector.append(newboard.board[row][col])
                    vscore = makeMove(vector)
                    newscr += vscore[1]
                    for row in range(0, 4):
                        newboard.board[row][col] = vscore[0][row]
            elif (dir == 'r' or dir == "right"):
                for row in range(0, 4):
                    vector = []
                    for col in range(0, 4):
                        vector.append(newboard.board[row][3-col])
                    vscore = makeMove(vector)
                    newscr += vscore[1]
                    for col in range(0, 4):
                        newboard.board[row][3-col] = vscore[0][col]
            elif (dir == 'd' or dir == "down"):
                for col in range(0, 4):
                    vector = []
                    for row in range(0, 4):
                        vector.append(newboard.board[3-row][col])
                    vscore = makeMove(vector)
                    newscr += vscore[1]
                    for row in range(0, 4):
                        newboard.board[3-row][col] = vscore[0][row]
            newboard.score = newscr
            return newboard

    def possibleDrops(self):
        drops = []
        for row in range(0, 4):
            for col in range(0, 4):
                if (self.board[row][col] == 0):
                    drops.append((row, col))
        return drops

    def quality(self):
        drops = self.possibleDrops()
        cp = []
        magic = 17.0
        for i in range(0, 17):
            cp.append(math.log(magic-i))
        #map score from f[0] = 99%, f[16]=20%
        cp0, cp16, minp, maxp = cp[0], cp[16], .20, .99
        slope = (maxp-minp) / (cp0 - cp16)
        for i in range(0, 16):
            cp[i] = slope * (cp[i] - cp16) + minp
        return (self.score * cp[16-len(drops)])

def squishZeros(vector):
    index = 0
    for i in range(0, len(vector)):
        if (vector[i] != 0):
            vector[index] = vector[i]
            if (i != index):
                vector[i] = 0
            index += 1
    return vector

def makeFusions(vector):
    newscr = 0
    for i in range(0, len(vector)-1):
        if (vector[i] == vector[i+1]):
            vector[i] += vector[i+1]
            newscr += vector[i]
            vector[i+1] = 0
    return [vector, newscr]

def makeMove(vector):
    vector = squishZeros(vector)
    vscore = makeFusions(vector)
    vscore[0] = squishZeros(vscore[0])
    return vscore

if __name__ == "__main__":
    testb = Board("0,0,0,0, 0,0,0,0, 2,8,0,0, 16,4,2,4", 60)
    print testb.tryDir("left")
    print testb.tryDir("up")
    print testb.tryDir("down")
    print testb.tryDir("right")
    print str(testb)
    print str(testb.move("r"))
    print str(testb.possibleDrops())
    print str(testb.quality())