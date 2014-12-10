import sys
from os import chdir
import getopt
from urlparse import urlparse, parse_qs
from BaseHTTPServer import HTTPServer as ServerClass
from SimpleHTTPServer import SimpleHTTPRequestHandler

from aiapi import AiRequest, AiResponse
from aibasic import AiRand, AiLeft
from aicorner import AiCorner
from aiscore import AiScore
from aiquality import AiQuality
from ailookahead import AiLookahead

class AiServer:
    port = 8008
    verbosity = 0
    root = "../2048web"

    def usage(self):
        '''Show usage, then exit'''
        print "Usage: [-port=8000 -root=../2048web -v=verbosity]"
        sys.exit()

    def cmdline(self):
        '''Parse command line '''
        try:
            opts, args = getopt.getopt(sys.argv[1:], "hv:", ["help", "port=", "root=" ])
        except getopt.GetoptError as err:
            print str(err) 
            self.usage()

        for o, a in opts:
            if o in ("-h", "--help"):
                self.usage()
            elif o == "--port":
                self.port = int(a)
            elif o == "--root":
                self.root = a
            elif o == "-v":
                self.verbosity = int(a)
            else:
                assert False, "unhandled option: " + o
    
    def __init__(self):
        '''Start and run the server '''
        self.cmdline()
        chdir(self.root)
        server_address = ('127.0.0.1', self.port)
        httpd = ServerClass(server_address, myHandler)
        sa = httpd.socket.getsockname()
        print "Serving HTTP on", sa[0], "port", sa[1], "..."
        httpd.serve_forever()

###

class myHandler(SimpleHTTPRequestHandler):
    '''Mostly a file server, but handle /ai? by calling the AI'''

    protocol_version = "HTTP/1.0"

    # Hander for /ai? URLs
    def gameAi(self):
        # URL params. Each element in dict is an array, just want the first
        url = parse_qs(urlparse(self.path).query)
        qdict = {}
        for key in url:
            qdict[key] = url[key][0]

        # Build an aireq from the args
        aireq = AiRequest(qdict)

        # Call the proper AI
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

        # Send results to the client
        self.send_response(200)
        self.send_header('Content-type', 'text/text')
        self.end_headers()
        self.wfile.write(airesp.dir + "\n" + airesp.msg + "\n")

    # Override do_GET to send /ai? to special handler, otherwise serve files
    def do_GET(self):
        if self.path[:4] in ("/ai?", "/ai/"):
            self.gameAi()
        else:
            SimpleHTTPRequestHandler.do_GET(self)
        return

# Run it
AiServer()


