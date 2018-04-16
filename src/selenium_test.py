import os
import sys
import socket
import urllib.request
import urllib.parse
import re
import pymysql
import time
import random
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys

#需求参数配置列表
dcap=dict(DesiredCapabilities.PHANTOMJS)
#user-agent等配置
dcap['phantomjs.page.settings.userAgent'] = ('Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36')
#是否允许加载图片
#dcap['phantomjs.page.settings.loadImages']=False
#设置请求cookie
#dcap['phantomjs.page.customHeaders.Cookie']='一段cookie字符'
# 禁用缓存
#dcap["phantomjs.page.settings.disk-cache"] = True

#service_args设置(基本设置）
service_args0=['--ignore-ssl-errors=true', '--ssl-protocol=any']
#  设置代理
service_args1 = ['--proxy=127.0.0.1:1080', '--proxy-type=socks5']

#dcap['phantomjs.page.settings.userAgent'] = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:25.0) Gecko/20100101 Firefox/25.0 ')
browser=webdriver.PhantomJS(executable_path='../tool/phantomjs/phantomjs2/bin/phantomjs.exe',
                            service_args=service_args0+service_args1,
                            service_log_path='../log/phantomjs/phan.log',
                            desired_capabilities=dcap)

#请求超时设置:
#1.设置页面完全加载的超时时间，完全加载即完全渲染完成，同步和异步脚本都执行完
browser.set_page_load_timeout(10)
#2.设置异步脚本的超时时间
#browser.set_script_timeout(3)
#3.识别对象的智能等待时间
#browser.implicitly_wait(3)

#url='https://www.flexport.com/data/hs-code/98-special-classification-provisions-nesoi'
#url='https://www.flexport.com/data/hs-code/0-all-commodities'
url='https://www.flexport.com/data/hs-code/01'
#url='https://www.flexport.com'
#url='https://www.baidu.com'

#access
try:
    browser.get(url)
except Exception as e:
    print("fail to access the url: " + url)

#get page source
try:
    htmlstr = str(browser.page_source)
    print(htmlstr)
except Exception as e:
    print("fail to get the page source: " + url)



# try:
#     # page title
#     title=browser.title
#     print(title)
#     #全屏
#     #browser.maximize_window()
#     #尺寸设置
#     #browser.set_window_size('800,600')
# except Exception as e:
#     print("Fail to test these things 1!")

#screenshot
# try:
#     browser.save_screenshot('test1.png')
# except Exception as e:
#     print("Fail to get screenshot!")

#元素定位和点击操作
# try:
#     element=browser.find_element_by_link_text('新闻')
#     element.click()
#     print(browser.current_url)
# except Exception as e:
#     print("Fail to index element!")

#搜索框处输入‘tecent'并回车搜索
# try:
#     browser.get('https://www.baidu.com')
#     element=browser.find_element_by_id('kw')
#     element.send_keys('tecent')
#     element.send_keys(Keys.RETURN)
#     print(browser.current_url)
# except Exception as e:
#     print('Fail to test search!')

#前进和后退（在多个页面之间）
# try:
#     browser.get('http://news.baidu.com/')
#     print(browser.current_url)
#     browser.get('http://xueshu.baidu.com/')
#     print(browser.current_url)
#     browser.back()
#     print(browser.current_url)
#     browser.back()
#     print(browser.current_url)
#     browser.forward()
#     print(browser.current_url)
# except Exception as e:
#     print("Fail to forward or back!")

#close--关闭当前浏览器窗口
browser.close()
#quit--关闭所有浏览器窗口，退出浏览器
browser.quit()

'''
关于PhantomJS对象的settings 参数 
phan["phantomjs.page.settings.xxxx"] = xxxx  
该属性存储请求/接收的各种设置：

javascriptEnabled定义是否在页面中执行脚本（默认为true）。

loadImages定义是否加载内联图像（默认为true）。

localToRemoteUrlAccessEnabled定义本地资源（例如从文件）是否可以访问远程URL（默认为false）。

userAgent 定义当网页请求资源时发送到服务器的用户代理。

userName 设置用于HTTP身份验证的用户名。

password 设置用于HTTP身份验证的密码。

XSSAuditingEnabled定义是否应监视加载请求以进行跨站点脚本尝试（默认为false）。

webSecurityEnabled定义是否启用Web安全性（默认为true）。

resourceTimeout（以毫秒为单位）定义超时时间，所请求的资源将停止尝试并继续执行页面的其他部分。onResourceTimeout回调将在超时时调用。


切换到操作iframe
flag = driver.find_element_by_tag_name('iframe')  
driver.switch_to.frame(flag)  
切换回操作主窗口
driver.switch_to.default_content()  


获得session_id  page_source  get_cookies()
browser.session_id  
browser.page_source  
browser.get_cookies()  


另外使用phantomjs多线程会有异常卡死的情况，尽量使用多进程。
from multiprocessing import Pool  
pool = Pool(8)  
data_list = pool.map(func, url_list)  
pool.close()  
pool.join()  


对于有可能异常退出情况，最好加一句driver.quit()，否则程序退出了但是phantomjs没有退出，一直占用资源。
driver.quit()  


使用chrome时，可以隐藏chrome的界面运行
from pyvirtualdisplay import Display  
display = Display(visible=0, size=(800,800))  
display.start()  


设置代理，清空缓存重新打开
利用DesiredCapabilities(代理设置)参数值，重新打开一个sessionId，我看意思就相当于浏览器清空缓存后，加上代理重新访问一次url
proxy=webdriver.Proxy()  
proxy.proxy_type=ProxyType.MANUAL  
proxy.http_proxy='1.9.171.51:800'  
或
proxy.sock_proxy='127.0.0.1:1080'
# 将代理设置添加到webdriver.DesiredCapabilities.PHANTOMJS中  
proxy.add_to_capabilities(webdriver.DesiredCapabilities.PHANTOMJS)  
browser.start_session(webdriver.DesiredCapabilities.PHANTOMJS)  
browser.get('http://1212.ip138.com/ic.asp')  

还原到系统（自己的ip）代理
proxy=webdriver.Proxy()  
proxy.proxy_type=ProxyType.DIRECT  
proxy.add_to_capabilities(webdriver.DesiredCapabilities.PHANTOMJS)  
browser.start_session(webdriver.DesiredCapabilities.PHANTOMJS)  
browser.get('http://1212.ip138.com/ic.asp')  
'''