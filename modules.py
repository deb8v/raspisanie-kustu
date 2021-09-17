from json.decoder import JSONDecodeError
import re
import requests
from bs4 import BeautifulSoup as bs
import os
import json
import datetime
import hashlib
import codecs
import time
import re

CACHE_DIR="docs/"



def cacheDir(cachedir="docs/"):
    CACHE_DIR=cachedir
    return CACHE_DIR
def journalD(pex,source,meta):

    print(source,'\t',meta,end=str(pex))


def getFromCache(url,expieri):
    CONTENT_SOURCE="CACHE_MODULE"
    def is_accessible(path, mode='a'):
        try:
            f = open(path, mode)
            f.close()
        except IOError:
            return False
        return True
    def readFromUrl(url):
        CURL=requests.get(url)
        RQ_STATUS=CURL.status_code
        if(RQ_STATUS==404):
            ERROR_CONTEXT="URL: "+url+", CODE: "+RQ_STATUS+"; NOT FOUND;"
            journalD(1,CONTENT_SOURCE,ERROR_CONTEXT)
            #проверка в кэше если не найден
            return None
        else:
            if(RQ_STATUS==200):
                return CURL.text
        return

    def download(path,url):
        print("downloading")
        CURL=requests.get(url)
        RQ_STATUS=CURL.status_code
        if(RQ_STATUS==404):
            ERROR_CONTEXT="URL: "+url+", CODE: "+RQ_STATUS+"; NOT FOUND;"
            journalD(1,CONTENT_SOURCE,ERROR_CONTEXT)
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
                journalD(1,CONTENT_SOURCE,ERROR_CONTEXT)
                return "ERR"
    def getModifTime(path):
        #cont=open('docs/e621c5499e18d482dbc52c2c666344c8.bak','r')
        #print(os.listdir('docs'))
        cont=open(path,'r')
        ra=cont.read()
        try:
            editt=json.loads(ra)
            rra=editt['modified']
            #print(rra)
            
        except TypeError:
            pass
        except JSONDecodeError:
        #    cont.close();
            return 0;
        cont.close();
        return rra

    def getFile(path):
        cont=open(path,'r')
        try:
            jsontext=cont.read()
            editt=json.loads(jsontext)['text']
        except JSONDecodeError:
            cont.close();
            return 0;
        cont.close();
        return editt

    ### СВЕРХУ ФУНКЦИИ
    ### СНИЗУ ЛОГИКА
    
    hashbyurlname=hashlib.md5(str(url).encode()).hexdigest()
    print(hashbyurlname)
    timenow=time.time()
    path=CACHE_DIR+hashbyurlname+'.bak'
        
    downloadEnyvere=False
    notWritable=False

    fileStatus=is_accessible(path)
    if(not fileStatus): #если не доступен на запись
        ERROR_CONTEXT="PATH: "+path+", CODE: NOT AVAILABLE;"
        journalD(3,CONTENT_SOURCE,ERROR_CONTEXT)
        notWritable=True
        downloadEnyvere=True
        return readFromUrl(url=url)
    deltatime=None
    if(fileStatus): #если доступен на запись
        mtime=getModifTime(path)
        deltatime=timenow-mtime
        deltatime=abs(deltatime)
        print('NOW:',timenow,"MOD: ",mtime, "DT:",deltatime,'EXPFOR:',expieri)
        if(deltatime>expieri):
            download(url=url,path=path)
        return getFile(path)

def test():
    print("R1t")
    teachersJSON=getFromCache('https://portal.kuzstu.ru/api/teachers',3600*24)
    print("R2t")
    teachersJSON=getFromCache('https://portal.kuzstu.ru/api/teachers',3600*24)
            
#test();
    ## 1 - проверяем наличие файла
    ## 2 - проверяем его актуальность
    ## 3 - качаем
    ## 4 - если нет кэша и ошибка загрузки выдаём ошибку в journal