from json.decoder import JSONDecodeError
from typing import Type
import main
import icalendar
import os
import json
from http.server import HTTPServer, BaseHTTPRequestHandler

from io import BytesIO
from requests import utils as rutils

def processor(gl):
    
    f=main.makeResponse(gl)
    #open("tests/democal.json",'w').write(json.dumps(f))
    s=icalendar.genCalendar(f)
    return s


        

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    # определяем метод `do_GET` 
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        #self.end_headers('content-length','1000')
        
        txt=rutils.unquote(self.path)
        try:
            #self.wfile.write(bytes(txt.encode('utf8')))
            #http://192.168.2.195:8000/icsshudle/?tgt=G6265,T2343
            print(txt)
            main.validStatic()
            if(txt!='/favicon.ico'):
                reqggroup=txt.split('/icsshudle/?',1)[1].split('tgt=',1)[1].split(',')
                print(reqggroup)
                self.wfile.write(bytes(str(processor(reqggroup)).encode("utf8")))
                
            
        except JSONDecodeError:
            
            self.wfile.write(bytes('error'.encode('utf8')))
        pass

httpd = HTTPServer(('192.168.2.195', 8000), SimpleHTTPRequestHandler)
httpd.serve_forever()
