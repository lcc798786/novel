from urllib import parse
from urllib import request
from urllib import error
from http import cookiejar
import ssl
import time
from lxml import etree
import re
import os
class url:
    def get_novel():
            txt='cookie.txt'
            head = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                    'Accept-Encoding':'gzip, deflate',
                    'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
                    'Cache-Control':'max-age=0',
                    'Connection':'keep-alive',
                    'Cookie':'__cdnuid=7110cf0a863310a4adc7f25a71b4706b',
                    'Host':'www.biquge.com.tw',
                    'If-Modified-Since':'Tue, 11 Sep 2018 04:32:00 GMT',
                    'If-None-Match':'"8072905263ad41:0"',
                    'Referer':'http://www.biquge.com.tw/14_14055/9192349.html',
                    'Upgrade-Insecure-Requests':'1',
                    'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36'}
            ssl._create_default_https_context = ssl._create_unverified_context
            cookie = cookiejar.CookieJar()
            cookie_hander = request.HTTPCookieProcessor(cookie)
            http_hander = request.HTTPHandler()
            https_hander = request.HTTPSHandler()
            opener = request.build_opener(https_hander,https_hander,cookie_hander)
            for i in range(100):
                for j in range(20000):
                    novel_number=str(i)+"_"+str(j)
                    url = 'http://www.biquge.com.tw/'+novel_number+"/"
                    try:
                        req=request.Request(url=url, headers=head)
                        get_response = opener.open(req)
                        cc = get_response.read().decode('gbk')
                        portal=cc.encode('utf-8').decode('utf-8')
                        portal=etree.HTML(portal)
                        category=portal.xpath(u"/html/head/meta[13]/@content")
                        name=portal.xpath(u"/html/head/meta[15]/@content")
                        path=u"/home/cc/PycharmProjects/novel_file/"+category[0]+"/"+name[0]
                        if os.path.exists(path) is False:
                            os.makedirs(path)
                        locate = 'href="/'+novel_number+'/(.*?)"'
                        list_url = re.findall(locate, cc)
                        for number in list_url:
                            get_url = url + number
                            try:
                                result = opener.open(get_url)
                            except Exception as e:
                                time.sleep(0.1)
                            txt = result.read().decode('gbk')
                            cc = txt.encode('utf-8').decode('utf-8')
                            cc = cc.replace('<br />', '')
                            result = etree.HTML(cc)
                            titles = result.xpath(u"//h1")
                            for title in titles:
                                novel_name=title.text
                                novel_name=novel_name.replace(" ","")
                                filename = novel_name+ '.txt'
                            result1 = result.xpath(u"//div[@id='content']")
                            for content in result1:
                                if os.path.isfile(path +'/'+ filename) is False:
                                    f = open(path +'/'+ filename, 'w')
                                    f.write(content.text)
                                    print(j)
                                    f.close()
                                else:
                                    print(os.path.isfile(path +'/'+ filename))
                    except error.HTTPError as e:
                        print(e.reason)


