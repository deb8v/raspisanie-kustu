import requests
from bs4 import BeautifulSoup as bs
import hashlib
import re



###################################
### ПЕРЕКАЧИВАЕМ ВСЁ РАСПИСАНИЕ ###
###################################

http_proxy  = "http://192.168.2.1:8080"
https_proxy = "http://192.168.2.1:8080"


proxyDict = { 
              "http"  : http_proxy, 
              "https" : https_proxy 
            }


URL_TEMPLATE="https://kuzstu.ru/web-content/sitecontent/studentu/raspisanie/raspisan.html"
r = requests.get(URL_TEMPLATE)
print(r.status_code)
if(r.status_code==404):exit();
parserdoc = bs(r.text, "html.parser")

froupsFile = open('rasplist/groups.txt','w')  # открытие в режиме записи

allurls= parserdoc.find_all("a")#[1].text.split("  ")[0].strip()
for url in allurls:
    alsa=re.fullmatch('\D\D\D\W\d\d\d', url.text)
    if url['href'].strip()!='1.htm':
        print(url.text,url['href'])
        rurl_rurl='http://kuzstu.ru/web-content/sitecontent/studentu/raspisanie/'+url['href']
        cr=requests.get(rurl_rurl,proxies=proxyDict)
        yob=open("rasplist/"+url.text.strip()+'.html','w',encoding='cp1251')
        yob.write(cr.text)
    
        yob.close()
        
        froupsFile.write(url.text.strip()+"$"+str(hashlib.md5(cr.text.encode('cp1251')).hexdigest())+"\n")
        print(str(hashlib.md5(cr.text.encode('cp1251')).hexdigest()))

froupsFile.close()        

