from json.decoder import JSONDecodeError
import requests
import json
import hashlib
import time
import sys

CACHE_DIR="docs/"



def cacheDir(cachedir="docs/"):
    CACHE_DIR=cachedir
    return CACHE_DIR
def journalD(pex,source,meta):

    print(source,'\t',meta,end=str(pex))


def getFromCache(url,expieri,checkError=True):
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
                return "ERR"
                        
            if total_length is None: # no content length header
                
                fileStructure={"modified":time.time(),'url':url,'path':path,'text':r.text}
                f.write(json.dumps(fileStructure))
                
                
            
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
                    

                    linesize=10
                    done=int(mapd(dl,0,int(total_length),0,linesize))
                    undone=linesize-done
                    print("\r>"+str(fSize)+"МБ [%s%s] %s Мб/с, %s" % ('=' * done, ' ' * undone, dl*0.0000076//(time.time() - start),filename)+""+"\r",end='')
                    sys.stdout.flush()
                
                fileStructure={"modified":time.time(),'url':url,'path':path,'text':str(filetemp.decode('cp1251'))}
                f.write(json.dumps(fileStructure))
                f.close()
                print()        
#    
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
    '''
    Тут вот ебануть мол доколе не можем скачать выкидываем нахуй.
    Т.е. качаем по умолчанию в md5.temp.txt если всё збс копируем.
    Иначе высылаем то что есть с пометкой
    '''
    if(fileStatus): #если доступен на запись
        mtime=getModifTime(path)
        deltatime=timenow-mtime
        deltatime=abs(deltatime)
        print('NOW:',int(timenow),"MOD: ",int(mtime), "DT: ",int(deltatime),'EXPFOR: ',int(expieri),'HASH: ',hashbyurlname)
        if(deltatime>expieri):
            download(url=url,path=path)
        return getFile(path)

def test():
    print("R1t")
    teachersJSON=getFromCache('https://portal.kuzstu.ru/api/teachers',3600*24)
    print("R2t")
    teachersJSON=getFromCache('https://portal.kuzstu.ru/api/teachers',3600*24)
    getFromCache('https://portal.kuzstu.ru/file/get/169315.rtf',200)
            
#test();
    ## 1 - проверяем наличие файла
    ## 2 - проверяем его актуальность
    ## 3 - качаем
    ## 4 - если нет кэша и ошибка загрузки выдаём ошибку в journal