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
    def is_accessible(path, mode='w'):
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
        cont=open(path,'r')
        try:
            editt=json.loads(cont.read())['modified']
        except JSONDecodeError:
            cont.close();
            return 0;
        cont.close();
        return editt

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
    deltatime=None
    if(fileStatus): #если доступен на запись
        mtime=getModifTime(path)
        deltatime=timenow-mtime
        deltatime=abs(deltatime)
        
    print(timenow,mtime,deltatime)
    if(not notWritable):
     if(deltatime>expieri or downloadEnyvere):
        download(url=url,path=path)
        mtime=getModifTime(path)
        deltatime=timenow-mtime
        deltatime=abs(deltatime)
        print(timenow,mtime,deltatime)
     else:
        if(notWritable):
            return readFromUrl(url=url)
        else:
            return getFile(path)
    ## 1 - проверяем наличие файла
    ## 2 - проверяем его актуальность
    ## 3 - качаем
    ## 4 - если нет кэша и ошибка загрузки выдаём ошибку в journal