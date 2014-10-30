from mod_python import apache, util
from urlparse import urlparse
from random import randint
import re

# Response from any UI should be {dir:(up|right|down|left), msg:"Optional Reason" }
Directions = [ 'up', 'right', 'down', 'left' ]

def handler(req):
        req.log_error('handler')
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
	board = board.split(',')

	# Log the request (ToDo)

	# Dispatch to the specified AI (ToDo: only supports rand for now)
        move = AIrand(board, scr, arg)

	# Write the response to the client
        req.send_http_header()
        req.write(move['dir'] + '\n' + move['msg'] + '\n')
        return apache.OK

def AIrand(board, score, arg):
	dir = Directions[randint(0, 3)]
	return {'dir':dir, 'msg':"rand [" + ','.join(board) + "] " + arg}
