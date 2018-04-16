import os
import sys
import socket
import urllib.request
import urllib.parse
import re
import pymysql
import time
import random
import selenium
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
import pymongo
from pymongo import MongoClient


'''
获取element部分的html代码
ybh=ybs.get_attribute('innerHTML')
dc=browser.find_element_by_css_selector('div[class="ui stackable grid segment chart_by_area chart_countries_wrap"]')
dch=dc.get_attribute('innerHTML')

os.chdir("D://pycode//crawl//flexport//core")
os.path.abspath('.')
'''

sleep_time=2
phantomjspath='../tool/phantomjs/phantomjs2/bin/phantomjs.exe'

def startBrowser():
    #load browser
    # 需求参数配置列表
    dcap = dict(DesiredCapabilities.PHANTOMJS)
    # user-agent等配置
    dcap['phantomjs.page.settings.userAgent'] = (
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36')

    # service_args设置(基本设置）
    service_args0 = ['--ignore-ssl-errors=true', '--ssl-protocol=any']
    #  设置代理
    service_args1 = ['--proxy=127.0.0.1:1080', '--proxy-type=socks5']

    # dcap['phantomjs.page.settings.userAgent'] = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:25.0) Gecko/20100101 Firefox/25.0 ')
    browser = webdriver.PhantomJS(executable_path=phantomjspath,
                                  service_args=service_args0 + service_args1,
                                  service_log_path='../log/phantomjs/phan.log',
                                  desired_capabilities=dcap)
    browser.set_page_load_timeout(10)
    return browser

def startMongodb():
    '''
    conn = MongoClient('127.0.0.1', 27017)
    db = conn.flexport
    '''
    conn = MongoClient('127.0.0.1', 27017)
    # 使用url形式
    # conn=MongoClient('mongodb://127.0.0.1:27017')
    db = conn.flexport  # 链接flexport数据库
    #my_set = db.users  # 选定users集合（相当于mysql表）
    return db

def getSeconddirUrl(browser=webdriver.PhantomJS(executable_path=phantomjspath)):
    # if not(type(browser) is selenium.webdriver.phantomjs.webdriver.WebDriver):
    #     return []
    urllist=[]
    elements=browser.find_elements_by_class_name('seo-link')
    for ele in elements:
        urlstr = str(ele.get_attribute('href'))
        if 2 < len(urlstr.split('hs-code/')[1].split('-')[0]) < 6:
            list.append(urlstr)

    return urllist

#getRootdir  and write to file record.txt and dirname.html
#rooturl='https://www.flexport.com/data/hs-code/0-all-commodities'
def dealRootdirPage():
    url='https://www.flexport.com/data/hs-code/0-all-commodities'
    recordfilename = '../data/rootdir/record.txt'
    pagefilename = '../data/rootdir/dir-' + '0' + '.html'

    try:
        recordfile=open(recordfilename,mode='a',encoding='utf-8')
        pagefile= open(pagefilename, mode='a', encoding='utf-8')
        print("Finish open 2 file!")
    except Exception as e:
        print("Fail to open files!")
        return

    browser=startBrowser()
    # access
    try:
        browser.set_page_load_timeout(30)
        browser.get(url)
        print('Finish to get page')
    except Exception as e:
        print("fail to access the url: " + url)
        #print(e)

    time.sleep(2)
    #find special element to ensure web ajax finish loading
    findres=-10      #max try num is 10
    while findres<0:
        elements=browser.find_elements_by_class_name("seo-link")
        print(len(elements))
        if len(elements) > 90:
            print("Finish to load page! Elements num is " + str(len(elements)))
            findres=1
            break

        findres=findres+1
        print("Into next while!")
        time.sleep(2)

    firstdirlist=[]
    #not finish load page all
    if findres==1:
        #finish to load page
        elements = browser.find_elements_by_class_name("seo-link")
        for ele in elements:
            urlstr=ele.get_attribute('href')
            hscode=urlstr.split('hs-code/')[1].split('-')[0]
            if len(hscode)==2:
                #url='https://www.flexport.com/data/hs-code/60-knitted-or-crocheted-fabrics'
                urlends = urlstr.split('hs-code/')[1]
                diritem={}
                diritem['hscode']=hscode
                diritem['level']='1'
                diritem['urlends']=urlends
                diritem['url']=urlstr
                firstdirlist.append(diritem)

    rootdiritem={'hscode':'0','level':'0','urlends':'0-all-commodities',
                 'url':'https://www.flexport.com/data/hs-code/0-all-commodities'}

    #save to mongodb: firstdir-info-->all firstdir url
    conn = MongoClient('127.0.0.1', 27017)
    db = conn.flexport
    dirset=db.dirs  #save 3 level hscode and their url(and leveo 0->0)
    #result_insert=dirset.insert_many(firstdirlist)
    dirset.update({'hscode':'0'},rootdiritem,True,True)
    for firstd in firstdirlist:
        #base -upsert--update(,,{'upsert':true}
        dirset.update({'hscode':firstd['hscode']},firstd,True,True)

    '''
    do main work:
    interact with server to get more data
    '''
    #Titel: text

    #Overvie: import and exports pic is js charts; 4 country pic is png files.

    #主段落： text

    #Destination Countries and Origin States:   need click
    #   import/Export and years(2008/.../2017) and show-more/less
    #   to get ajax data---》need 异步加载
    #ajax test：
    #find two show-more button and click them
    button1=browser.find_elements_by_class_name("show_more_areas")[0]
    if button1.text=='Show more':
        button1.click()
        time.sleep(1)
    button2=browser.find_elements_by_class_name("show_more_areas")[1]
    if button2.text=='Show more':
        button2.click()
        time.sleep(1)
    #find 4 import/export buttons
    #find active button export and click-->not click
    # buttons_ex=browser.find_elements_by_css_selector('button[class="ui active button filter_trigger"]')
    # for but in buttons_ex:
    #     but.click()
    #find button year
    #browser.find_elements_by
    yearbuttons=browser.find_element_by_class_name("years_buttons")
    yearnums=str(yearbuttons.text).split()
    for yearnum in yearnums:
        if len(yearnum)!=4:
            continue
        #选定特定年份
        yearelem1 = browser.find_elements_by_css_selector(
            'div[class="years_buttons"] button[data-value="' + yearnum + '"]')[0]
        yearelem1.click()
        yearelem1.get_attribute('Html')
        time.sleep(0.5)
        yearelem2 = browser.find_elements_by_css_selector(
            'div[class="years_buttons"] button[data-value="' + yearnum + '"]')[1]
        yearelem2.click()
        time.sleep(0.5)
        # find and save data from page source

    #switch to import
    # find not active button import and click
    buttons_im1 = browser.find_elements_by_css_selector('button[class="ui  button filter_trigger"]')[0]
    buttons_im1.click()
    time.sleep(1)
    buttons_im2 = browser.find_elements_by_css_selector('button[class="ui  button filter_trigger"]')[1]
    buttons_im2.click()
    time.sleep(1)
    #find button year
    #browser.find_elements_by
    yearbuttons=browser.find_element_by_class_name("years_buttons")
    yearnums=str(yearbuttons.text).split()
    for yearnum in yearnums:
        if len(yearnum)!=4:
            continue
        #选定特定年份
        yearelem = browser.find_elements_by_css_selector(
            'div[class="years_buttons"] button[data-value="' + yearnum + '"]')[0]
        yearelem.click()
        time.sleep(0.5)
        yearelem = browser.find_elements_by_css_selector(
            'div[class="years_buttons"] button[data-value="' + yearnum + '"]')[1]
        yearelem.click()
        time.sleep(0.5)
        # find and save data from page source

    #finished to deal destination/origin country

    #右侧：常规文本数据 and jquery tree



    # get page source
    htmlstr=''
    try:
        htmlstr = str(browser.page_source)
        print('success to get pagesource!')
        #print(htmlstr)
    except Exception as e:
        print("fail to get the page source: " + url)

    try:
        responseurl = browser.current_url
        recordfile.write("requesturl: " + url + "   " + "responseurl: " + responseurl+" \n")
        pagefile.write(htmlstr)
        print("result: OK")
    except Exception as e:
        tcode = 0
        treason = ''
        if hasattr(e, "code"):
            tcode = e.code
        if hasattr(e, "reason"):
            treason = e.reason
        errstr = "error: " + str(tcode) + ":" + str(treason)
        print("error: ", str(tcode) + ":" + str(treason))

    try:
        # close--关闭当前浏览器窗口
        conn.close()
        browser.close()
        recordfile.close()
        pagefile.close()
    except Exception as e:
        print("Fail to close page or file!")

#getFirstDir and write to file record.txt and dirname.html
def dealFirstdirPage(url='',recordfilename='',pagefilename=''):

    try:
        recordfile=open(recordfilename,mode='a',encoding='utf-8')
        pagefile= open(pagefilename, mode='a', encoding='utf-8')
        print("Finish open 2 file!")
    except Exception as e:
        print("Fail to open files!")
        return

    browser=startBrowser()
    # access
    try:
        browser.set_page_load_timeout(10)
        browser.get(url)
        print('Finish to get page')
    except Exception as e:
        print("fail to access the url: " + url)
        print(e)

    time.sleep(2)
    #find special element to ensure web ajax finish loading
    findres=0
    while findres==0:
        elements=browser.find_elements_by_class_name("seo-link")
        for ele in elements:
            urlstr=ele.get_attribute('href')
            if len(urlstr.split('hs-code/')[1].split('-')[0])>2:
                findres=1
                print('Finish load page')
                break
        print("Into next while...")
        time.sleep(2)

    # get page source
    htmlstr=''
    try:
        htmlstr = str(browser.page_source)
        print('success to get pagesource!')
        print(htmlstr)
    except Exception as e:
        print("fail to get the page source: " + url)

    try:
        responseurl = browser.current_url
        recordfile.write("requesturl: " + url + "   " + "responseurl: " + responseurl+" \n")
        pagefile.write(htmlstr)
        print("result: OK")
    except Exception as e:
        tcode = 0
        treason = ''
        if hasattr(e, "code"):
            tcode = e.code
        if hasattr(e, "reason"):
            treason = e.reason
        errstr = "error: " + str(tcode) + ":" + str(treason)
        print("error: ", str(tcode) + ":" + str(treason))

    try:
        # close--关闭当前浏览器窗口
        browser.close()
        recordfile.close()
        pagefile.close()
    except Exception as e:
        print("Fail to close page or file!")


def getFirstDir():
    baseurl = "https://www.flexport.com/data/hs-code/"
    dirlist=[]
    #dirlist=[str(i) for i in range(10,100)]
    for i in range(1,10):
        page='0'+str(i)
        dirlist.append(page)
    dirlist.append('0-all-commodities')
    dirlist.sort()

    for dirstr in dirlist:
        time.sleep(sleep_time + random.randint(0, 20) / 10)
        url=baseurl+dirstr
        print("current url: ", url)
        content = ''
        #sleep,防止block
        recordfilename='../data/firstdir/record.txt'
        pagefilename='../data/firstdir/dir-' + dirstr + '.html'

        dealFirstdirPage(url=url,recordfilename=recordfilename,pagefilename=pagefilename)

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
        if f.endswith('.html') and (f!='dir-0-all-commodities.html'):
            parserFirstDir(filename=f)

#test every function
def UnitTest():
    #test dealRootdirPage()
    dealRootdirPage()
    #test dealFirstDirPage()
    #firstdirurl='https://www.flexport.com/data/hs-code/02'
    #dealFirstdirPage(url=firstdirurl,recordfilename='../log/unittest/firdirpage.txt',pagefilename='../log/unittest/firdirpage2.txt')

if __name__=="__main__":
    # url='https://www.flexport.com/data/hs-code/98-special-classification-provisions-nesoi'
    #url = 'https://www.flexport.com/data/hs-code/0-all-commodities'
    # url='https://www.flexport.com'

    # execute getFirstDir to get level 1 direction
    #getFirstDir()
    UnitTest()
    #parserFirstDir('../data/firstdir/dir-98.html')
    #pass