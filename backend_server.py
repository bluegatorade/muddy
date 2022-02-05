# Python 3 server example
import cgi
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import manager
import res
from res_config import ResConfig

class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        errs = []
        try: 
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={'REQUEST_METHOD': 'POST'}
            )
            res = form.getvalue('res')
            c = ResConfig.FromString(form.getvalue('res'))
            errs = manager.PlanRes(c)

            self.send_response(200)
        except Exception as e: 
            errs.append(str(e))
            self.send_response(500)
        self.end_headers()
        if len(errs) == 0:
            self.wfile.write(bytes(str(f"scheduled {c.firstname} {c.lastname} for {c.size} on {c.date}, look for email three days before"), 'utf8')) 
        else:
            self.wfile.write(bytes(str(errs), 'utf8')) 

def Start():
    host = "localhost"
    port = 8000
    server = HTTPServer((host, port), Handler)
    print("server started http://%s:%s" % (host, port))

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass

    server.server_close()
    print("server stopped.")