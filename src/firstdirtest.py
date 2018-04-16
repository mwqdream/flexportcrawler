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

def getFirstDir(url=""):   #open link and deal error
    # url = 'https://itunes.apple.com/cn/genre/ios-%E5%9B%BE%E4%B9%A6/id6018?mt=8'
    #https://itunes.apple.com/us/genre/ios-books/id6018?mt=8
    #html1 = str(urllib.request.urlopen(url).read().decode('utf-8'))

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
            #user_agent2='Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36'
            #user_agent3='Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
            #user_agent=[user_agent1,user_agent2,user_agent3]
            #Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36
            #Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36
            #Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.10240
            #Mozilla/5.0 (Windows NT 10.0; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0
            #Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.87 Safari/537.36 OPR/37.0.2178.31
            #Opera/9.80 (Windows NT 6.1) Presto/2.12.388 Version/12.16
            #Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko
            #Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)
            #Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)
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

getFirstDir()


'''
65.0.3325.146
64.0.3282.167
62.0.3202.62
61.0.3163.100
58.0.3029.110
58.0.3029.96
58.0.3029.81
57.0.2987.113
57.0.2987.110 
'''