from json.decoder import JSONDecodeError
from re import I
from typing import Counter, Type
import main
import icalendar
import os
import json
import time
from http.server import HTTPServer, BaseHTTPRequestHandler

from io import BytesIO
from requests import utils as rutils
import datetime
def processor(gl):
    
    f=main.makeResponse(gl,limit=1)
    #open("tests/democal.json",'w').write(json.dumps(f))
    s=icalendar.genCalendar(f)
    return s

class webapi():
    def procFindIDsBySearch(rqString):
        rqars=rqString.split('tgt=',1)[1]
        ret=dict()
        if(rqars.find(',')>0):
           ret = main.compileGroupList(rqars.split(','))
        else:
           ret= main.compileGroupList([rqars])
        ret=list(ret)
        out=list()
        
        for i in ret:
            out.append({'ID':i,'NAME':main.getFNameByID(i)})
        return json.dumps(out[0:10])

    def procGetRaspListByID(rqString):
        rqars=rqString.split('tgt=',1)[1]
        ret=list()
        psid=0
        if(rqars.find(',')>0):
        #if(1==0):
           psid = int(rqars.split(',')[0])
           pass
        else:
            psid=int(rqars)
            if(psid>0):
                temp=main.getByGroup_ID(psid)
            if(psid<0):
                temp=main.getTeacherShudleByUID(psid*-1)

            alldates=[]
            byDates=list()
            ret=temp
            now = datetime.datetime.today()-datetime.timedelta(days=1)
            #ret['content']=[]
            allLessNubers=list()
            for f in temp['content']:
                caha=datetime.datetime.strptime(f['date_lesson'], "%Y-%m-%d")
                if(caha>=now):
                    alldates.append( f['date_lesson'])
                    allLessNubers.append(f['lesson_number'])
            alldates=list(set(alldates))
            allLessNubers=sorted(list(set(allLessNubers)))
            #print 
            alldates=sorted(alldates)
            exportlist=list()
            dn='7'
            for g in alldates:
                educlist=list()
                expeduclist=list()
                
                for i in temp['content']:
                    if(i['date_lesson']==g):
                        educlist.append(i)
                        dn=i['day_number']
                        
                        pass
                
                for d in allLessNubers:
                    for edl in educlist:
                        if(d==edl['lesson_number']):
                           expeduclist.append(edl) 

                exportlist.append({'date':g,'day_number':dn,'content':expeduclist})
            #добавить шапку перед экспортом
            temp['content']=exportlist
            print(alldates)
            #print(psid,temp)
            return json.dumps(temp)
            pass
            
        
        

    def getAbout():
        print(icalendar.dictCallstring)
        print(icalendar.addresses)
        return json.dumps({'calls':icalendar.dictCallstring,'addresses':icalendar.addresses})

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    # определяем метод `do_GET` 
    def do_GET(self):
        self.send_response(200)
        time0=time.time()
        
        txt=rutils.unquote(self.path)
        try:
            #self.wfile.write(bytes(txt.encode('utf8')))
            #http://192.168.2.195:8000/icsshudle/?tgt=G6265,T2343
            print(txt)
            #main.validStatic()
            if(txt!='/favicon.ico'):
                if(txt.find('/icsshudle/?')>-1):
                    self.send_header('Content-type', 'text/plain; charset=utf-8')
                    self.end_headers()
                    reqggroup=txt.split('/icsshudle/?',1)[1].split('tgt=',1)[1].split(',')
                    print(reqggroup)
                    self.wfile.write(bytes(str(processor(reqggroup)).encode("utf8")))
                
                st1='/icsshudle/web-api/v1.1d/'

                if(txt.find(st1)>-1):
                    self.send_header('Content-type', 'application/json; charset=utf-8')
                    self.send_header("Access-Control-Allow-Methods", '*')
                    self.send_header("Access-Control-Allow-Origin", '*')
                    
                    
                    self.end_headers()
                    reqggroup=txt.split(st1,1)
                    rqroute=reqggroup[1].split('?',1)
                    if(len(rqroute)==2):
                        route=rqroute[0]
                        args=rqroute[1]
                    else:
                        route='dummy'
                        args='null'
                    print(route)
                    #reqggroup[1].split('tgt=',1)[1]
                    if(route=='search'):
                        self.wfile.write(bytes(str(webapi.procFindIDsBySearch(args)).encode("utf8")))
                    if(route=='rasp'):
                        self.wfile.write(bytes(str(webapi.procGetRaspListByID(args)).encode("utf8")))
                    if(route=='about'):
                        self.wfile.write(bytes(str(webapi.getAbout()).encode("utf8")))
            time1=time.time()    
            print('dt ms:',-1000*(time0-time1))
        except JSONDecodeError:
            
            self.wfile.write(bytes('error'.encode('utf8')))
        pass
#webapi.procGetRaspListByID("?tgt=-18920")

httpd = HTTPServer(('', 8000), SimpleHTTPRequestHandler)

httpd.serve_forever()


