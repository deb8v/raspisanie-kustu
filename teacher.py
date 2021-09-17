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
import modules
#PERSONS_PATH=

CACHE_DIR="docs/"
modules.cacheDir(CACHE_DIR);



teachersJSON=modules.getFromCache('https://portal.kuzstu.ru/api/teachers',3600*24)
groupsJSON=modules.getFromCache('https://portal.kuzstu.ru/api/group',3600*24*7)

TIME_FORMAT='%X %x %Z'

SUBSCRIBERS_LIST=["G6265","КСс-211","УКб",'ТЭ',"T17453","Яковлева"]
SUBSCOMPILED_LIST=list()







def getTeacherIDByName(pripoduname):
    for i in teachersJSON:
        if i['name']==pripoduname:
            return i['person_id']
    
def getTeacherNameByID(pripoduid):
    for i in teachersJSON:
        if i['person_id']==pripoduid:
            return i['name']


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
        modules.journalD(1,CONTENT_SOURCE,ERROR_CONTEXT)
        #проверка в кэше если не найден
    if(RQ_STATUS!=200):
        ERROR_CONTEXT="URL: "+URL+", CODE: "+RQ_STATUS+";"
        modules.journalD(6,CONTENT_SOURCE,ERROR_CONTEXT)
        #высылка в сисьлох
    JQ=json.loads(CURL.text)
    RETURN_CONTENT={'timestamp':time.time(),'time':TIME_NOW,'status':RQ_STATUS,'content':JQ}

    return RETURN_CONTENT

def getTeacherShudleByUID(teacher_id):
    CONTENT_SOURCE="GET_TEACHER_BY_UID"
    TIME_NOW=time.strftime(TIME_FORMAT)

    #https://portal.kuzstu.ru/api/teacher_schedule?teacher_id=101040
    URL='https://portal.kuzstu.ru/api/teacher_schedule?teacher_id={teacher_id}'.format(teacher_id=teacher_id)
    CURL=requests.get(URL)
    RQ_STATUS=CURL.status_code
    if(RQ_STATUS==404):
        ERROR_CONTEXT="URL: "+URL+", CODE: "+RQ_STATUS+"; NOT FOUND;"
        modules.journalD(1,CONTENT_SOURCE,ERROR_CONTEXT)
        #проверка в кэше если не найден
    if(RQ_STATUS!=200):
        ERROR_CONTEXT="URL: "+URL+", CODE: "+RQ_STATUS+";"
        modules.journalD(6,CONTENT_SOURCE,ERROR_CONTEXT)
        #высылка в сисьлох
    JQ=json.loads(CURL.text)
    JQa=JQ
    for i in JQa:
        i['teacher_id']=teacher_id
        i['teacher_name']=getTeacherNameByID(teacher_id)
        print(i)
        
        pass
    RETURN_CONTENT={'timestamp':time.time(),'time':TIME_NOW,'status':RQ_STATUS,'content':JQ}


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




'''
teachersList=json.loads(teachersJSON)
groupsList=json.loads(groupsJSON)

SUBSCOMPILED_LIST = compileGroupList(SUBSCRIBERS_LIST,groupsList)
print(SUBSCRIBERS_LIST)
print(SUBSCOMPILED_LIST)
#print(groupsList)
tsopa=getByGroup_ID(5833)
'''
#print(tsopa['content'])
#getTeacherShudleByUID(101040)




#modules.getFromCache("https://portal.kuzstu.ru/api/group",3600*24)
pass