import os
import sys
import socket
import urllib.request
import urllib.parse
import re
import pymysql
import time

sleep_time=1

baseurl="https://www.flexport.com/data/hs-code/"
#starturl="https://www.flexport.com/data/hs-code/0-all-commodities"
#starturl="https://www.flexport.com/data/hs-code/01-live-animals"
#starturl="https://www.flexport.com/data/hs-code/01-live-animals"
starturl="https://www.flexport.com/data/hs-code/01"

url=starturl

print("current url: ", url)
content = ''


user_agent='Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3298.4 Safari/537.36'
headers={"User-agent":user_agent}
#headers={"User-agent":user_agent,'Referer':referer,'host':host,'origin':origin,
#         'Connection':connection,'Content-Length':70,'X-Requested-With':'XMLHttpRequest','Content-Type':contenttype}
#url='https://jsondata.25pp.com'
#data=urllib.parse.urlencode(values)
#注意只是针对values进行了解码，而headers没有。
#bianary_data=data.encode('utf-8')
req=urllib.request.Request(url=url,headers=headers)


print(req.full_url)
print(req.get_method())
print(req.data)
print(req.headers)
print("result:")

try:
    response = urllib.request.urlopen(req)
    responseurl=response.url
    content = str(response.read().decode('utf-8'))
    response.close()
except Exception as e:
    tcode = 0
    treason = ''
    if hasattr(e, "code"):
        tcode = e.code
    if hasattr(e, "reason"):
        treason = e.reason
    errstr = "error: " + str(tcode) + ":" + str(treason)
    print("error: ",str(tcode)+":"+str(treason))

print(content)