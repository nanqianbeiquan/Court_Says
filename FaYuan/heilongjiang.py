# coding=utf-8
import re
import os
import traceback
import gevent
import gevent.monkey
import datetime
import requests
from lxml import html
import urlparse
from xml.etree import ElementTree

class ShuiWu(object):
    def __init__(self,province,key,two=False,dishui_type=None):
        self.pinyin='hei_long_jiang'
        self.key=key
        if not two:
            self.data={
                'col':'1',
                'appid':'1',
                'webid':'1',
                'path':'/',
                'columnid':config_one[province][key]['columnid'],
                'sourceContentType':'1',
                'unitid':config_one[province][key]['unitid'],
                'webname':config_one[province][key]['webname'],
                'permissiontype':'0'
            }
            self.url=config_one[province][key]['domain']
        else:
            self.url=config_two[province][key][dishui_type]['url']
            self.div_class=config_two[province][key][dishui_type]['divclass']
            self.encoding=config_two[province][key][dishui_type]['encoding']
        self.headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36'
            }
        self.province=province
        result=urlparse.urlparse(self.url)
        self.href_ahead=result.scheme+'://'+result.netloc
        self.oldest_time='2015-01-01'

    def do_guoshui(self):
        root = self.get_root()
        lst_node = root.getiterator("totalrecord")[0].text
        params={
            'startrecord':'0',
            'endrecord':str(int(lst_node)-1),
            'perpage':str(lst_node)
        }
        root = self.get_root(params=params)
        results = root.getiterator("record")
        for node in results:
            self.print_node(node)

    def get_root(self,params=False):
        if params:
            a=requests.post(self.url,data=self.data,params=params,headers=self.headers)
        else:
            a=requests.post(self.url,data=self.data,headers=self.headers)
        root = ElementTree.fromstring(a.text)
        return root

    def print_node(self,node):

        self.title_time=re.findall("\d{4}-\d{2}-\d{2}",node.text)[0]
        if self.title_time>self.oldest_time:
            try:
                self.title=re.findall("title='(.*?)'",node.text)[0]
            except:self.title=re.findall('title="(.*?)"',node.text)[0]
            re_words=u'(?:欠税公告|欠税.*公告|欠缴税款|非正常户|欠费公告|关于清缴欠税的通告|非正户)'
            if re.search(u'%s' %(re_words,),self.title):
                sql = "select * from taxplayer_all_filename where title='%s' and fbrq='%s' and region='%s'" % (
                self.title, self.title_time, self.key)
                is_exist = MySQL.execute_query(sql)
                if not is_exist:
                    href=re.findall("href='(.*?)'",node.text)[0]
                    self.page_name=href.split('/')[-1]
                    real_href=self.href_ahead+href
                    self.write_html(real_href)

    def write_html(self,url):
        count=0
        page_content=requests.get(url,headers=self.headers)
        if page_content.status_code==200:
            page_content.encoding='utf8'
            tree=html.fromstring(page_content.text)
            all_a=tree.xpath('//a/@href')
            for a in all_a:
                if a.endswith('.doc') or a.endswith('.xls') or a.endswith('.xlsx'):
                    count+=1
                    if a.startswith('..'):
                        a='/'+a.replace('../','')
                    self.doc_url=self.href_ahead+a
                    #print self.doc_url
                    try:
                        r=requests.get(self.doc_url,headers=self.headers)

                    except:
                        logf.write(self.doc_url+' 无法下载'+'\n')
                        #print self.doc_url+' 无法下载'
                    else:
                        try:
                            self.filename=re.findall('filename=(.*)',a)[0]
                        except:
                            self.filename=a.split('/')[-1]

                        if not os.path.exists('%s/%s' %(self.pinyin,self.filename)):
                            with open('%s/%s' %(self.pinyin,self.filename), 'wb') as f:
                                for chunk in r.iter_content(chunk_size=1024):
                                    if chunk:  # filter out keep-alive new chunks
                                        f.write(chunk)
                                        f.flush()
                            f.close()
                            self.insert_sql()
                        else:
                            logf.write('出现相同文件名'+self.filename+'来自'+url+'\n')
                            #print '出现相同文件名'+self.filename+'来自'+url

            if count==0:
                self.filename=self.page_name
                self.doc_url=url
                if not os.path.exists('%s/%s' %(self.pinyin,self.filename)):
                    f=open('%s/%s' %(self.pinyin,self.filename),'w+')
                    f.write(page_content.text.encode('utf8'))
                    f.close()
                    self.insert_sql()
                else:
                    logf.write('出现相同页面名'+self.filename+'来自'+url+'\n')
                    #print '出现相同页面名'+self.filename+'来自'+url
    def insert_sql(self):
        time_now= datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sql="insert into taxplayer_all_filename(province,region,fbrq,title,filename,url,last_update_time) values('%s','%s','%s','%s','%s','%s','%s')" %(\
            self.province,self.key,self.title_time,self.title,self.filename,self.doc_url,time_now )
        try:
            MySQL.execute_update(sql)
        except:
            logf.write('数据库插入有问题：'+'\n')
            logf.write(sql+'\n')
            logf.write(traceback.format_exc()+'\n')
        else:
            logf.write('插入成功：'+self.title_time+self.title+self.doc_url+ '\n')


    def do_dishui(self):
        page_content=requests.get(self.url,headers=self.headers)
        page_content.encoding=self.encoding
        tree=html.fromstring(page_content.text)
        try:
            self.get_dishui_title(tree)
        except MyException.TitleOverTimeException:
            pass
        else:
            startpage=2
            while True:
               #print '正在抓取page'+str(startpage)
               param='_'+str(startpage)+'.'
               url=re.sub('_\d{1}\.',param,self.url)
               #print url
               page_content=requests.get(url,headers=self.headers)
               page_content.encoding=self.encoding
               tree=html.fromstring(page_content.text)
               try:
                   self.get_dishui_title(tree)
               except MyException.TitleOverTimeException:
                   break
               else:startpage+=1

    def get_dishui_title(self,tree):
        str='//div[@class="'+self.div_class+'"]/ul/li'
        news=tree.xpath(str)
        for gonggao in news:
            url=gonggao.xpath('a/@href')[0]
            self.title=gonggao.xpath('a/text()')[0].replace('\r','').replace('\n','')
            self.title_time=gonggao.xpath('span/text()')[0].replace('(','').replace(')','')
            if self.title_time < self.oldest_time:
                raise MyException.TitleOverTimeException
            url='http://www.hljtax.gov.cn/tax/ww/'+re.findall('art.*',url)[0]
            re_words=u'欠税公告'
            if re.search(u'%s' %(re_words,),self.title):
                self.deal_title(url)
            
    def deal_title(self,url):
        sql="select * from taxplayer_all_filename where title='%s' and fbrq='%s' and region='%s' "%(self.title,self.title_time,self.key)
        is_exist=MySQL.execute_query(sql)
        if not is_exist:
            self.page_name=url.split('/')[-1]
            self.write_html(url)


if __name__ == '__main__':
    if __package__ is None:
        import sys
        from os import path
        sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
        from tax import MyException,MySQL
        from tax.config import config_one,config_two
    gevent.monkey.patch_all()
    tasks=[]
    today=datetime.date.today()
    file_name = os.path.basename(__file__).split('.')[0]
    logf = open("log/%s.txt" % ( str(today)), 'a')
    logf.write(str(today) +'开始爬虫'+ '\n')

    m='黑龙江省'
    #返回内容都是xml格式，比较容易处理
    for n in config_one[m].keys():
        shuiwu=ShuiWu(m,n)
        cc=shuiwu.do_guoshui
        tasks.append(gevent.spawn(cc))
    #网站数据为html，需要分析页面结构抓取数据
    for n in config_two[m].keys():
         for x in config_two[m][n].keys():
             shuiwu=ShuiWu(m,n,two=True,dishui_type=x)
             dd=shuiwu.do_dishui
             tasks.append(gevent.spawn(dd))
    gevent.joinall(tasks)
    logf.close()






