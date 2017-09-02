from types import *
import copy
import math
import random

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
        return (', '.join(rowStrs) + ", " + str(self.score))

    #returns true if board[r1][c1] can move onto board[r0][c0], false otherwise
    def moveOk(self, r0, c0, r1, c1):
        a = self.board[r0][c0]
        b = self.board[r1][c1]
        return (a == 0 and b != 0) or (a != 0 and a == b)

    #returns true if dir is a valid move for board, false otherwise
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

    #returns true if the board has any valid moves, false otherwise
    def canMove(self):
        return(self.tryDir('l') or self.tryDir('u') or self.tryDir('r') or self.tryDir('d'))

    #returns a board that would be the result if the current board was moved in direction dir
    def move(self, dir):
        newboard = Board(self.board, self.score)
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

    #returns true if the board can move num times, false if it can't.
    def moveNum(self, num):
        if (num <= 1):
            return self.canMove()
        return(self.move('l').drop().moveNum(num-1) or
               self.move('u').drop().moveNum(num-1) or
               self.move('r').drop().moveNum(num-1) or
               self.move('d').drop().moveNum(num-1))


    #returns an array of tuples that represent empty board locations, namely those that can recieve a random drop
    def possibleDrops(self):
        drops = []
        for row in range(0, 4):
            for col in range(0, 4):
                if (self.board[row][col] == 0):
                    drops.append((row, col))
        return drops

    #returns a board that would be the result if the current board were to recieve a random drop from list drops, or from possibleDrops if drops is null
    def drop(self, drops = None):
        if (drops == None):
            drops = self.possibleDrops()
        newboard = Board(self.board, self.score)
        if (len(drops) == 0):
            return newboard
        choice = random.choice(drops)
        if (random.random() >= .9):
            newboard.board[choice[0]][choice[1]] = 4
        else:
            newboard.board[choice[0]][choice[1]] = 2
        return newboard

#the following are helper functions to make move work
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
    testb = Board("2,4,8,16, 16,8,4,2, 2,4,8,16, 16,8,2,4", 60)
    #print testb.tryDir("left")
    #print testb.tryDir("up")
    #print testb.tryDir("down")
    #print testb.tryDir("right")
    print str(testb)
    #print str(testb.move("r"))
    #print str(testb.possibleDrops())
    #print str(testb.drop(testb.possibleDrops()))
    print (testb.moveNum(10))
