import os
import sys
import socket
import urllib.request
import urllib.parse
import re
import pymysql
import time
import random

sleep_time=2

#getFirstDir and write to file record.txt and dirname.html
def getFirstDir(url=""):
    baseurl = "https://www.flexport.com/data/hs-code/"
    dirlist=[str(i) for i in range(10,100)]
    for i in range(1,10):
        page='0'+str(i)
        dirlist.append(page)
    dirlist.append('0-all-commodities')
    dirlist.sort()

    recordfile=open('../data/record.txt',encoding='utf-8',mode='a')

    for dirstr in dirlist:
        url=baseurl+dirstr
        print("current url: ", url)
        content = ''
        #sleep,防止block
        time.sleep(sleep_time+random.randint(0,20)/10)

        try:
            dirfile = open('../data/dir-' + dirstr + '.html', encoding='utf-8', mode='a')
            user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3298.4 Safari/537.36'
            headers = {"User-agent": user_agent}
            req = urllib.request.Request(url=url, headers=headers)

            response = urllib.request.urlopen(req)
            responseurl = response.url
            recordfile.write("dirurl: "+dirstr+"    "+"responseurl: "+responseurl)
            content = str(response.read().decode('utf-8'))
            response.close()
            dirfile.write(content)
            dirfile.close()
            print("result: OK")
        except Exception as e:
            tcode=0
            treason=''
            if hasattr(e,"code"):
                tcode=e.code
            if hasattr(e,"reason"):
                treason=e.reason
            errstr="error: "+str(tcode)+":"+str(treason)
            print("error: ",str(tcode)+":"+str(treason))

    recordfile.close()
    return


def parserFirstDir(filename='',content=''):
    if filename!='':
        with open(filename,mode='r',encoding='utf-8') as f:
            content=f.read()

            #get page--hscode and url
            pat = '<meta property="og:url" content="[\s\S]*<meta property="og:description'
            res = str(re.compile(pat).findall(content))
            pageurl=res.split('content="')[1].split('"')[0]
            print(pageurl)
            hscode=pageurl.split('hs-code/')[1].split('-')[0]
            urlends=pageurl.split('hs-code/')[1]
            print(hscode+" "+urlends)

            #get page--subpage-->seconddir and thirddir--hscode and pageurl
            pat='<td class="heading_subheading two wide">[\s\S]*?</td>'
            results=re.compile(pat).findall(content)
            print(len(results))
            print(results)
            secdir=set()
            thirdir=set()

            for res in results:
                hsc=res.split('</td>')[0].split('>')[1]
                parts=hsc.split('.')
                if len(parts)>=1:
                    secdir.add(parts[0])
                    if len(parts)>=2:
                        thirdir.add(parts[0]+parts[1])

            seconddir=list(secdir)
            thirdir=list(thirdir)
            seconddir.sort()
            thirdir.sort()
            print('seconddir:')
            print(seconddir)
            print('thirddir:')
            print(thirdir)



def dealFirstDir():
    filepath="../data/firstdir/"
    flist=os.listdir(filepath)
    for f in flist:
        if f.endswith('.html'):
            parserFirstDir(filename=f)


if __name__=="__main__":
    #execute getFirstDir to get level 1 direction
    #getFirstDir()
    parserFirstDir('../data/firstdir/dir-98.html')