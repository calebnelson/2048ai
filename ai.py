from mod_python import apache, util
from urlparse import urlparse
from random import randint
import re

# Response from any UI should be {dir:(up|right|down|left), msg:"Optional Reason" }
Directions = [ 'up', 'right', 'down', 'left' ]

def handler(req):
        req.content_type = 'text/text'

	# get url parameters, and parse into dictionary
	queryStr = req.parsed_uri[apache.URI_QUERY]
        queryDct = util.parse_qs(queryStr) if queryStr is not None else {}

	# fetch and clean up the four params: ai, arg, board, score
        ai  = queryDct['ai'][0] if 'ai' in queryDct else 'rand'
        arg = queryDct['arg'][0] if 'arg' in queryDct else ''
        scr = queryDct['score'][0] if 'score' in queryDct else ''
        # clean up the board by turning runs of spc comma bar into comma
	board = re.sub('[ ,]+', ',', queryDct['board'][0]) if 'board' in queryDct else ''
	# split into array
	board = map(int, board.split(','))
	grid = boardToGrid(board)
	# Log the request (ToDo)

	# Dispatch to the specified AI (ToDo: only supports rand for now)
        if ai == 'left':
		move = AIleft(req, grid, scr, arg)
	else:
		move = AIrand(req, grid, scr, arg)

	# Write the response to the client
        req.send_http_header()
        req.write(move['dir'] + '\n' + move['msg'] + '\n')
        return apache.OK

def boardToGrid(board):
	grid = []
	for row in range(0, 4):
		grid.append([])
		for col in range(0, 4):
			grid[row].append(board[row*4+col])
	return grid

def gridToString(grid):
	return "[" + ','.join(map(str, grid[0])) + " | " + ','.join(map(str, grid[1])) + " | " + ','.join(map(str, grid[2])) + " | " + ','.join(map(str, grid[3])) + "]"  

def AIrand(req, grid, score, arg):
	dir = Directions[randint(0, 3)]
	return {'dir':dir, 'msg':"rand" + gridToString(grid)}

def AIleft(req, grid, score, arg):
	moveLeft = {'dir':'left', 'msg':"left works " + gridToString(grid)}
	for row in grid:
		for tile in range(0, 3):
			if (row[tile] == 0):
				if (row[tile+1] != 0):
					return moveLeft
			else:
				if (row[tile] == row[tile+1]):
					return moveLeft
	moveUp = {'dir':'up', 'msg':"up works " + gridToString(grid)}
	for col in range(0, 4):
                for row in range(0, 3):
                        if (grid[row][col] == 0):
                                if (grid[row+1][col] != 0):
                                        return moveUp
                        else:
                                if (grid[row][col] == grid[row+1][col]):
                                        return moveUp
	dir = Directions[randint(1, 2)]
	return {'dir':dir, 'msg':"left and up don't work " + gridToString(grid)}
