from aiapi import AiRequest, AiResponse
from aibasic import AiLeft

def AiCorner(aireq):
	priority = { 'up':"lurd", 'right':"lurd", 'down':"uldr", 'left':"uldr" }
	name = { 'u':'up', 'r':'right', 'd':'down', 'l':'left' }
	if (len(aireq.prior) == 0):
		return AiLeft(aireq)
	for d in priority[aireq.prior[0]]:
		if (aireq.b.tryDir(d)):
			return AiResponse(name[d], "by prio: " + priority[aireq.prior[0]] + " with board " + str(aireq.b.board))
