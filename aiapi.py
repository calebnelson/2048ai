# Define objects to talk to different AIs, 
# and things common to the whole system

# Map between direction names and numbers
from board import Board

DirectionMap = { 0:'up',    'up':0,    'u':0,
                 1:'right', 'right':1, 'r':1, 
                 2:'down',  'down':2,  'd':2,
                 3:'left',  'left':3,  'l':3 }

class AiRequest:
  """The arguments passed to the AI"""
  ai     = ""   # which ai
  arg    = ""   # optional args for the AI passed on url from the game
  gid    = ""   # id of game
  b  = Board(None)   # current board as [row][col]
  prior  = []   # recent prior moves as stack of 'u' 'd' 'l' 'r'
  drop   = ""   # cell dropped by game after last move as [row, col, value]

  # Build an empty request, or one parsed from a dictionary of URL params
  def __init__(self, query = None):

    drop = "0,0,4"
    prior = "u"
    if(query != None): 
      # fetch params from URL
      self.ai     = query.get('ai', "")
      self.arg    = query.get('arg', "")
      self.gid    = query.get('gid', "noid")
      self.b = Board(query.get('board', "4,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0"), query.get('score', 0))
      drop  = query.get('drop', "0,0,4")
      prior = query.get('prior', "u")

    # remove spaces, turn into array of ints at least 16 long, then 2D board

    # map expected one letter codes to name (e.g. prior=udlruu)
    ptab = { 'u':'up', 'r':'right', 'd':'down', 'l':'left' }
    self.prior = []
    for p in prior:
      if p in ptab:
        self.prior.append(ptab[p])

    # remember where last tile was droppped
    drop = map(int, drop.replace(' ', '').split(','))
    if (len(drop) != 3):
      self.drop = { 'r':0, 'c':0, 'v':0 }
    else:
      self.drop = {'r':drop[0], 'c':drop[1], 'v':drop[2] }

  # Show the id, the board, and the priors
  def __str__(self):
    prior = ','.join(self.prior)
    return self.gid + str(self.b) + prior + str(self.drop)


class AiResponse:
  """The response back to the game"""
  dir = ""
  msg = ""

  def __init__(self, dir, msg = None):
    self.dir = dir
    self.msg = msg if msg is not None else ""

  def __str__(self):
    return "Direction: " + self.dir + " | Message: " + self.msg

# For testing
if __name__ == "__main__":
  qry = {'gid':'hello', 'board':'4,4,8,0,2', 'prior':'lrddu', 'drop':'1,0,2'}
  req = AiRequest(qry)
  rsp = AiResponse('left', 'testing\nsecond line')
  print "Query:    " + str(qry)
  print "Request:  " + str(req)
  print "Response: " + str(rsp)
