# -*- coding: utf8 -*-
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
#PERSONS_PATH=



TIME_FORMAT='%X %x %Z'

SUBSCRIBERS_LIST=["G6265","КСс-211","УКб",'ТЭ']
SUBSCOMPILED_LIST=list()

CACHE_DIR="docs/"




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
     if(deltatime<expieri or downloadEnyvere):
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

    


def journalD(pex,source,meta):

    print(source,'\t',meta,end=str(pex))


def getByGroup_ID(group_id):
    #5833
    RQ_STATUS=0;
    
    
    TIME_NOW=time.strftime(TIME_FORMAT)

    CONTENT_SOURCE="GROUP_PARSER"
    URL="https://portal.kuzstu.ru/api/student_schedule?group_id={group_id}".format(group_id=group_id)
    CURL=requests.get(URL)
    RQ_STATUS=CURL.status_code
    if(RQ_STATUS==404):
        ERROR_CONTEXT="URL: "+URL+", CODE: "+RQ_STATUS+"; NOT FOUND;"
        journalD(1,CONTENT_SOURCE,ERROR_CONTEXT)
        #проверка в кэше если не найден
    if(RQ_STATUS!=200):
        ERROR_CONTEXT="URL: "+URL+", CODE: "+RQ_STATUS+";"
        journalD(6,CONTENT_SOURCE,ERROR_CONTEXT)
        #высылка в сисьлох
    JQ=json.loads(CURL.text)
    RETURN_CONTENT={'timestamp':time.time(),'time':TIME_NOW,'status':RQ_STATUS,'content':JQ}

    return RETURN_CONTENT

def compileGroupList(sublist, grouplist):
    #1## Группа по номеру G6265 // 'G\d+'
    #2## Группа по тексту КСс-211
    #3## Лист по своей регулярке

    returnlist=[]
    returnlistBeta=[]
    regexpType1="G\d+"
    regexpType2="\W{2,4}\s\d{2,4}"
    regexpType3="R\*+"

    def findNumByText(text):
        #print(text)
        counter=0
        findlist=[]
        for d in grouplist:

            #print(d)
            name=str(d["name"])
            #\D{3,5}-\d{3}
            ax = re.search(text+"\w{0,6}-\d{3}", name)
            at=1
            #if(ax!=1 and text.find(name)!=-1):at=1
            #print(name)
            #print(d["dept_id"],d["name"],'text:',text)
            if ax!=None:
                #print(ax)
                conntent=d["dept_id"]
                returnlist.append(int( "".join(re.findall("\d+", conntent))))    
                
        
    for subject in sublist:
        
        for rt1 in re.findall(regexpType1,subject):
            returnlist.append(int( "".join(re.findall("\d+", rt1))))
        findNumByText(subject)
        #for rt2 in re.findall(regexpType2,subject):
        #    returnlist.append(int(rt1))
        
    
    return set(returnlist)

teachersJSON=getFromCache('https://portal.kuzstu.ru/api/teachers',3600*24)
groupsJSON=getFromCache('https://portal.kuzstu.ru/api/group',3600*24*7)

teachersList=json.loads(teachersJSON)
groupsList=json.loads(groupsJSON)

SUBSCOMPILED_LIST = compileGroupList(SUBSCRIBERS_LIST,groupsList)
print(SUBSCRIBERS_LIST)
print(SUBSCOMPILED_LIST)
#print(groupsList)
tsopa=getByGroup_ID(5833)

#print(tsopa['content'])

#getFromCache("https://portal.kuzstu.ru/api/group",3600*24)
pass