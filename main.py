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
import icalendar
import random
#PERSONS_PATH=

CACHE_DIR="docs/"
modules.cacheDir(CACHE_DIR)

teachersJSON=json.loads(modules.getFromCache('https://portal.kuzstu.ru/api/teachers',3600*24*3))
groupsJSON=json.loads(modules.getFromCache('https://portal.kuzstu.ru/api/group',3600*24*7*3))

def validStatic():

    teachersJSON=json.loads(modules.getFromCache('https://portal.kuzstu.ru/api/teachers',3600*24*3))
    groupsJSON=json.loads(modules.getFromCache('https://portal.kuzstu.ru/api/group',3600*24*7*3))

#TIME_FORMAT='%X %x %Z'
TIME_FORMAT='%Y-%m-%d %H:%M:%S'
#YYYY-MM-DD HH:mm

#SUBSCRIBERS_LIST=["G6265","КСс-211","УКб",'ТЭ',"T17453","Малюгин",' ']
#SUBSCRIBERS_LIST=["G6265","КСс-211","T17453","Мал"]
SUBSCRIBERS_LIST=["G6265","Малюгин"]
#SUBSCRIBERS_LIST=["УКб"]
SUBSCOMPILED_LIST=list()

def getFNameByID(ID):
    if(ID<0):
        for i in teachersJSON:
            if(i['person_id']==str(ID*-1)):
                return i['name']
        
    else:
        for i in groupsJSON:
            if(i['dept_id']==str(ID)):
                return i['name']
    return None

def editRP(parms):
    editparams={'place':'залупа'}
    #for i in range(0,len(parms)):
        
        #if str(parms[i]['teacher_name']).find("Коротков В")>-1:
        #    parms[i]['comments']=[["Кто видел короткова?",'Никто'],['Да кто такой этот ваш коротков!']][random.randint(0,1)]
        #    pass
        #strd=str(parms[i]['education_group_name'])
        #if(strd.find('з')>-1):
        #    strd
        #    print(strd);
    #Вот тут вот можно что нибудь редактировать, полнлостью, потом это будет в возможностях преподских
    '''
    date_lesson: "2021-10-15"
    day_number: "5"
    education_group_id: "6265"
    education_group_name: "КСс-211"
    id: "2684840"
    lesson_number: "4"
    place: "3001а"
    subgroup: "0"
    subject: "Введение в специальность"
    teacher_id: "18927"
    teacher_name: "Коротков А.Н."
    type: "л."
    '''
    return parms
def getByGroup_ID(group_id):
   
    RQ_STATUS=201; # в будущем указыввает источник, из каши или прямым запросом
    
    
    TIME_NOW=time.strftime(TIME_FORMAT)

    CONTENT_SOURCE="GROUP_PARSER"
    URL="https://portal.kuzstu.ru/api/student_schedule?group_id={group_id}".format(group_id=group_id)
    
    def getGroupNameByID(pripoduid):
        for i in groupsJSON:
            #'source':"Расписание занятий"
            if i['dept_id']==str(pripoduid):
                return i['name']

    JQ=json.loads(modules.getFromCache(URL,8*3600))
    for z in range(0,len(JQ)):
        JQ[z]['source']="Расписание занятий"
    RETURN_CONTENT={'timestamp':time.time(),'time':TIME_NOW,'status':RQ_STATUS,'id':group_id,'name':getGroupNameByID(group_id),'isteacher':False,'content':editRP(JQ)}

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
    
    JQ=json.loads(modules.getFromCache(URL,8*3600))
    JQo=list()
    teacherName=getTeacherNameByID(teacher_id)
    for i in JQ:
        i['source']="Расписание занятий"
        i['teacher_id']=str(teacher_id)
        i['teacher_name']=teacherName
        #print(i)
        JQo.append(i)
        pass
    
    RETURN_CONTENT={'timestamp':time.time(),'time':TIME_NOW,'status':RQ_STATUS,'id':teacher_id,'name':teacherName,'isteacher':True,'content':editRP(JQo),}
    
    return RETURN_CONTENT


def compileGroupList(sublist):
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
            pripoduname=str(pripoduname).lower()
            ra=str(i['name']).lower().find(pripoduname)
            if ra>-1:
                returnlist.append(-int( "".join(re.findall("\d+", i['person_id']))))    
                
    
    

    def findNumByText(text):
        for d in groupsJSON:
            name=str(d["name"]).lower()
            text=str(text).lower()
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


def makeResponse(SUBSCRIBERS_LIST=SUBSCRIBERS_LIST,limit=5):
    SUBSCOMPILED_LIST = compileGroupList(SUBSCRIBERS_LIST)
    print("<<<",SUBSCRIBERS_LIST)
    print("---",SUBSCOMPILED_LIST)
    #if(len(SUBSCOMPILED_LIST)>limit):
    #    return None
    #SUBSCOMPILED_LIST=
    SUBSCOMPILED_LIST=list(SUBSCOMPILED_LIST)[0:limit]
    print(">>>",SUBSCOMPILED_LIST,'l=',limit)
#    DICKTLIMITIED=dict(SUBSCOMPILED_LIST)[0:limit]
    output=list()
    pass

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

        
#f=(makeResponse(SUBSCRIBERS_LIST))
#open("tests/democal.json",'w').write(json.dumps(f))


#pathToIcs='U:/raspis/my.ics'
#icalendar.makeCalendar(f,pathToIcs)

pass