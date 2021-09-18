# -*- coding: utf8 -*-
from json.decoder import JSONDecodeError
import re
from asyncio.runners import run
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



teachersJSON=json.loads(modules.getFromCache('https://portal.kuzstu.ru/api/teachers',3600*24))
groupsJSON=json.loads(modules.getFromCache('https://portal.kuzstu.ru/api/group',3600*24*7))

#TIME_FORMAT='%X %x %Z'
TIME_FORMAT='0:%Y-%m-%d %H:%M:%S'
#YYYY-MM-DD HH:mm

#SUBSCRIBERS_LIST=["G6265","КСс-211","УКб",'ТЭ',"T17453","Малюгин",' ']
#SUBSCRIBERS_LIST=["G6265","КСс-211","T17453","Мал"]
SUBSCRIBERS_LIST=["G6265"]
SUBSCOMPILED_LIST=list()


def getByGroup_ID(group_id):
   
    RQ_STATUS=201; # в будущем указыввает источник, из каши или прямым запросом
    
    
    TIME_NOW=time.strftime(TIME_FORMAT)

    CONTENT_SOURCE="GROUP_PARSER"
    URL="https://portal.kuzstu.ru/api/student_schedule?group_id={group_id}".format(group_id=group_id)
    
    def getGroupNameByID(pripoduid):
        for i in groupsJSON:
            if i['dept_id']==str(pripoduid):
                return i['name']

    JQ=json.loads(modules.getFromCache(URL,1000))
    RETURN_CONTENT={'timestamp':time.time(),'time':TIME_NOW,'status':RQ_STATUS,'id':group_id,'name':getGroupNameByID(group_id),'content':JQ}

    return RETURN_CONTENT

def getTeacherShudleByUID(teacher_id):
    RQ_STATUS=201;
    CONTENT_SOURCE="GET_TEACHER_BY_UID"
    TIME_NOW=time.strftime(TIME_FORMAT)

    def getTeacherNameByID(pripoduid):
        for i in teachersJSON:
            if i['person_id']==str(pripoduid):
                return i['name']

    #https://portal.kuzstu.ru/api/teacher_schedule?teacher_id=101040
    URL='https://portal.kuzstu.ru/api/teacher_schedule?teacher_id={teacher_id}'.format(teacher_id=teacher_id)
    
    JQ=json.loads(modules.getFromCache(URL,1000))
    JQo=list()
    teacherName=getTeacherNameByID(teacher_id)
    for i in JQ:
        i['teacher_id']=teacher_id
        i['teacher_name']=teacherName
        #print(i)
        JQo.append(i)
        pass
    RETURN_CONTENT={'timestamp':time.time(),'time':TIME_NOW,'status':RQ_STATUS,'id':teacher_id,'name':teacherName,'content':JQo}
    return RETURN_CONTENT


def compileGroupList(sublist, grouplist):
    #1## Группа по номеру G6265 // 'G\d+'
    #2## Группа по тексту КСс-211
    #3## Лист по своей регулярке

    returnlist=[]
    returnlistBeta=[]
    regexpType1="G\d+"
    regexpType1T="T\d+"
    regexpType2="\w{0,6}-\d{3}"
    regexpType3="R\*+"


    def getTeacherIDByName(pripoduname):
        for i in teachersJSON:
            ra=i['name'].find(pripoduname)
            if ra>-1:
                returnlist.append(-int( "".join(re.findall("\d+", i['person_id']))))    
                
    
    

    def findNumByText(text):
        for d in grouplist:
            name=str(d["name"])
            #\D{3,5}-\d{3}
            ax = re.search(text+regexpType2, name)
            at=1
            if ax!=None:
                conntent=d["dept_id"]
                returnlist.append(int( "".join(re.findall("\d+", conntent))))    
                
        
    for subject in sublist:
        
        for rt1 in re.findall(regexpType1,subject):
            returnlist.append(int( "".join(re.findall("\d+", rt1))))
        for rt1T in re.findall(regexpType1T,subject):
            returnlist.append(-int( "".join(re.findall("\d+", rt1T))))
        findNumByText(subject)
        getTeacherIDByName(subject)
            
    return set(returnlist)


def makeResponse(SUBSCRIBERS_LIST=SUBSCRIBERS_LIST):
    SUBSCOMPILED_LIST = compileGroupList(SUBSCRIBERS_LIST,groupsJSON)
    print(SUBSCRIBERS_LIST)
    print(SUBSCOMPILED_LIST)

    output=list()
    for i in SUBSCOMPILED_LIST:
        temp=list();
        if(i>0):
            temp=getByGroup_ID(i)
        if(i<0):
            temp=getTeacherShudleByUID(i*-1)
        output.append(temp)
    return output

def makeICS(id):
    temp=dict()
    if(id>0):
        temp=getByGroup_ID(id)
    if(id<0):
        temp=getTeacherShudleByUID(id*-1)
#    for 


#print(groupsJSON)


#print(tsopa['content'])
#tsopa=getByGroup_ID(5833)

        
f=(makeResponse(SUBSCRIBERS_LIST))
open("tests/democal.json",'w').write(json.dumps(f))

pass