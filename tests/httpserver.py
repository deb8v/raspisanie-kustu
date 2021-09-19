from http.server import HTTPServer, BaseHTTPRequestHandler

from io import BytesIO


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    # определяем метод `do_GET` 
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        #self.end_headers('content-length','1000')
        self.wfile.write(b'Hello, world!<br>')
        txt=self.path
        try:
            self.wfile.write(bytes(txt.encode('utf8')))
            reqggroup=txt.split('/icsshudle/?',1)[1].split('=',1)[1]
            print(reqggroup)
            
        except:
            
            self.wfile.write(bytes('error'.encode('utf8')))
        pass

httpd = HTTPServer(('192.168.2.195', 8000), SimpleHTTPRequestHandler)
httpd.serve_forever()