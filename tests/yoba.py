# -*- coding: utf8 -*-
import re
import requests
from bs4 import BeautifulSoup as bs
import os
import json
import datetime
import hashlib
import codecs

WEB_ROOT_DIR="/var/www/raspisanie/"
#WEB_ROOT_DIR=""
ENABLE_REDOWNLOAD=True

http_proxy  = "http://192.168.2.1:8080"
https_proxy = "http://192.168.2.1:8080"


proxyDict = { 
              "http"  : http_proxy, 
              "https" : https_proxy 
            }

if(ENABLE_REDOWNLOAD):
    URL_TEMPLATE="https://kuzstu.ru/web-content/sitecontent/studentu/raspisanie/raspisan.html"
    r = requests.get(URL_TEMPLATE)
    print(r.encoding)
    print(r.status_code)
    if(r.status_code==404):exit();
    parserdoc = bs(r.text, "html.parser")

    froupsFile = open(WEB_ROOT_DIR+'groups.txt','w') 

    allurls= parserdoc.find_all("a")
    for url in allurls:
        alsa=re.fullmatch('\D\D\D\W\d\d\d', url.text)
        if url['href'].strip()!='1.htm':
            print(url.text,url['href'])
            rurl_rurl='http://kuzstu.ru/web-content/sitecontent/studentu/raspisanie/'+url['href']
            #cr=requests.get(rurl_rurl,proxies=proxyDict)
            cr=requests.get(rurl_rurl)
            yob=open("rasplist/"+url.text.strip()+'.html','w',encoding='cp1251')
            yob.write(cr.text)
        
            yob.close()
            
            froupsFile.write(url.text.strip()+"$"+str(hashlib.md5(cr.text.encode('cp1251')).hexdigest())+"\n")
            print(str(hashlib.md5(cr.text.encode('cp1251')).hexdigest()))

    froupsFile.close()       



retaray = []
array = os.listdir('/home/ensem/raspisanie/rasplist') # получаем список папок из \NN
def gref(strs):
        
    text=open("/home/ensem/raspisanie/rasplist/"+strs,'r',encoding='cp1251')
    soup = bs(text, "html.parser")

    cgrname = soup.find_all("font")[1].text.split("  ")[0].strip()

    vacancies_names = soup.find_all('tr')

    disception={}
    dickspetion={}
    stopwords=["\nЧасы","\nВремя","\nПары"]
    for name in vacancies_names:
        disception[0]=cgrname

        giros=name.contents[0].text
        if str(giros) in stopwords:
            pass
        else:
            pado=0
            for i in name.contents:
                cblock=0
               
                if(i!='\n' and i!='\nтекст' and i!='' and str(type(i))=='''<class 'bs4.element.Tag'>'''):
                    pos=int(pado/2)+1
                    if(pos>10):pos=10
                    gordon=i.text
                    
                    disception[pos]=gordon.strip()
                pado+=1
               
            if(cblock==0):
                disception[1]=disception[1].split(',')[1]
                retaray.append(str(json.dumps([disception])).encode('utf8').decode('unicode-escape','utf8'))

                
fileactual=open(WEB_ROOT_DIR+"now.txt",'a',encoding='utf8')
today = datetime.datetime.now().strftime("%Y-%m-%d-%H.%M")


fileall=open(WEB_ROOT_DIR+today+".txt",'w',encoding='utf8')

retards=[]
for i in range(len(array)):
    print(len(array)-i)
    
#for i in range((10)):
    ger=array[i].strip().split(".")
    if ger[1]=='html':
        devblk=gref(array[i])
        retards.append(devblk)
        
#txt=str(json.dumps(retards,ensure_ascii=False).encode('utf8'))
#txt=

#print(txt);
rbim={}
rbim['datetime']=today
rbim['raspisanie']=retaray
fileall.write(str(json.dumps(rbim,ensure_ascii=False)))
fileall.close();
fileactual.write(today+"\n")
fileactual.close();
#print(json.load((json.dumps(rbim))))