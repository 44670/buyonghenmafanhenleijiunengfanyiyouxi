from struct import pack, unpack
import SimpleHTTPServer
import SocketServer
import sys
import json
import importlib

PORT = 8052

class MyRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def handleGameStringApi(self):
        global backend

        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.send_header('Access-Control-Allow-Origin', 'http://44670.org')
        self.end_headers()
        ret = backend.readGameStringForHttpApi()
        if (ret is None):
            ret = {'status': 'failed'}
        else:
            lastSuccessReadForHttpApi = ret
        self.wfile.write(json.dumps(ret))
        return

    #def log_message(self, format, *args):
        #return

    def do_GET(self):
        if self.path.startswith('/str'):
            self.handleGameStringApi()
            return
            
        if self.path == '/':
            self.path = 'index.html'
            return SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

if len(sys.argv) < 2:
    print("""
        Usage:
        python server.py backend_name

        Example:
        python server.py psp.lxzs1
    """)
    exit(0)

backend = importlib.import_module('backends.' + sys.argv[1])

Handler = MyRequestHandler
httpd = SocketServer.TCPServer(("", PORT), Handler)
print "Text extraction service started at port: ", PORT
print "Visit http://44670.org/fanyi for translations!"
httpd.serve_forever()
