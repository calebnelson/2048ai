# Defines the web handler to parse request, call the AI, send anwser
#
# request params on the URL are defined in AiRequest, including:
#   ai, arg, gid, prior, drop, board, score
#
# response back to client is a text web page in format:
#   move\nmessage\n
# where move is oneof up/right/down/left and message is optional
#
from mod_python import apache, util
from aiapi import AiRequest, AiResponse
from aibasic import AiRand, AiLeft
from aicorner import AiCorner
from aiscore import AiScore
from aiquality import AiQuality
from ailookahead import AiLookahead

def handler(req):
  # Get URL paramaters from apache web server as dictionary
  url = util.parse_qs(req.parsed_uri[apache.URI_QUERY])
  # Each element in this dict is actually an array, just want the first
  qdict = {}
  for key in url:
    qdict[key] = url[key][0]

  # Build an aireq from the args, and call the proper AI
  aireq = AiRequest(qdict)
  if aireq.ai == 'lookahead':
    airesp = AiLookahead(aireq)
  elif aireq.ai == 'quality':
    airesp = AiQuality(aireq)
  elif aireq.ai == 'score':
    airesp = AiScore(aireq)
  elif aireq.ai == 'corner' or aireq.ai == 'ul':
    airesp = AiCorner(aireq)
  elif aireq.ai == 'left':
    airesp = AiLeft(aireq)
  else:
    airesp = AiRand(aireq)

  # Write the response back to the game
  req.content_type = 'text/text'
  req.send_http_header()
  req.write(airesp.dir + "\n" + airesp.msg + "\n")
  return apache.OK
