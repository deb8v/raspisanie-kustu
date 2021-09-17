import requests
import sys
import time


import json

from time import sleep
from sys import stdout

def journalD(pex,source,meta):

    print(source,'\t',meta,end=str(pex))

def download(path,url, name=None):
    CONTENT_SOURCE="DOWNLOAD"
    def mapd(x,in_min,in_max,out_min,out_max):
        return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
    JUMP_LEFT_SEQ = '\u001b[100D'
    with open(path, 'w') as f:
        start = time.time()
        r = requests.get(url, stream=True)
        total_length = r.headers.get('content-length')
        dl = 0
        RQ_STATUS=r.status_code
        filetemp=bytes()
        encoding = 'ansi'
        if(RQ_STATUS!=200):
            ERROR_CONTEXT="URL: "+url+", CODE: "+RQ_STATUS
            journalD(1,CONTENT_SOURCE,ERROR_CONTEXT)
                    
        if total_length is None: # no content length header
            f.write(r.text)
        
        else:
            for chunk in r.iter_content(1024):
                dl += len(chunk)
                #f.write(chunk)
                filetemp+=chunk
                done = int( dl / int(total_length))
                print(JUMP_LEFT_SEQ, end='')
                filename=name
                sizee=int(total_length)
                fSize='%.1fМБ: ' % (sizee*0.00000095)
                

                linesize=15
                done=int(mapd(dl,0,int(total_length),0,linesize))
                undone=linesize-done
                print("\r>"+str(fSize)+"МБ [%s%s] %s Мб/с, %s" % ('=' * done, ' ' * undone, dl*0.0000076//(time.time() - start),filename)+""+"\r",end='')
                stdout.flush()
            
            fileStructure={"modified":time.time(),'url':url,'path':path,'text':str(filetemp.decode())}
            f.write(json.dumps(fileStructure))
            f.close()
    print()        


def download2(path,url):
        print("downloading")
        CURL=requests.get(url)
        RQ_STATUS=CURL.status_code
        if(RQ_STATUS==404):
            ERROR_CONTEXT="URL: "+url+", CODE: "+RQ_STATUS+"; NOT FOUND;"
            journalD(1,3443,ERROR_CONTEXT)
            #проверка в кэше если не найден
            return "ERR"
        else:
            if(RQ_STATUS==200):
                fileStructure={"modified":time.time(),'url':url,'path':path,'text':CURL.text}
                cont=open(path,'w');
                cont.write(json.dumps(fileStructure))
                cont.close()
                return "OK"
            else:
                ERROR_CONTEXT="URL: "+url+", CODE: "+RQ_STATUS
                journalD(1,3443,ERROR_CONTEXT)
                return "ERR"
#url='https://portal.kuzstu.ru/file/get/169315.rtf'
url='https://portal.kuzstu.ru/api/group'

download('tests/trash/temp.bak',url)

download2('tests/trash/temp2.bak',url)

pass

