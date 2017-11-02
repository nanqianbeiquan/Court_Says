#coding=utf-8
import datetime
import sys
import threading
import time

import MySQLdb
from bs4 import BeautifulSoup

from ShuiWu.SpiderMan import SpiderMan

reload(sys)
sys.setdefaultencoding('utf-8')
updatetime=datetime.datetime.now().strftime('%Y-%m-%d')

class AnHuiSearcher(SpiderMan):
    def __init__(self):
        super(AnHuiSearcher, self).__init__(keep_session=True)

    def set_config(self):
        t_start=datetime.datetime.now()
        conn_2 = MySQLdb.connect(host='172.16.0.20', port=3306, user='zhangxiaogang', passwd='gangxiaozhang', db='job_info',
                         charset='utf8')
        cursor_2 = conn_2.cursor()
        print 't_start:', t_start
        sql_3 = "UPDATE ktgg_job set start_time='%s' where name='ah_susong2nd' " % (t_start)
        cursor_2.execute(sql_3)
        conn_2.commit()
        m_list = []
        m1 = threading.Thread(target=self.run,args=(1,400))
        m_list.append(m1)
        m2 = threading.Thread(target=self.run,args=(400,800))
        m_list.append(m2)
        # m3 = threading.Thread(target=self.run,args=(400,600))
        # m_list.append(m3)
        # m4 = threading.Thread(target=self.run,args=(600,800))
        # m_list.append(m4)
        # m5 = threading.Thread(target=self.run,args=(800,1000))
        # m_list.append(m5)
        for m in m_list:
            m.setDaemon(True)
            m.start()
        m.join()
        stop_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sql_4 = "UPDATE ktgg_job set status=1 ,stop_time='%s' where name='ah_susong2nd' " % (stop_time)
        cursor_2.execute(sql_4)
        conn_2.commit()
        t_end = datetime.datetime.now()
        t = t_end-t_start
        print 'the program time is :%s' %t

    def run(self,n_start,n_end):
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:45.0) Gecko/20100101 Firefox/45.0'}
        conn_1 = MySQLdb.connect(host='172.16.0.20', port=3306, user='zhangxiaogang', passwd='gangxiaozhang', db='court_notice',
                             charset='utf8')
        cursor_1 = conn_1.cursor()
        for p in range(n_start,n_end):
            self.page = p
            url = 'http://www.ahgyss.cn/ktgg/index_'+str(p)+'.jhtml'
            for i in range(3):
                try:
                    r = self.get(url=url, headers=headers, timeout=50)
                    if r.status_code == 200:
                        break
                except:
                    continue
            soup = BeautifulSoup(r.text,'html5lib')
            try:
                zhu_ye = soup.find(class_='sswy_news').find(class_='c1-body')
                li_list = zhu_ye.find_all('li')
                for n in range(len(li_list)):
                    self.num = n
                    self.an_hao = li_list[n].a['title']
                    href = li_list[n].a['href']
                    # print an_hao, href
                    print p, n
                    if u'(20' in self.an_hao:
                        tag_a = self.get_href_from_db(href)
                        # print 'tag_a', tag_a
                        if tag_a:
                            print u'数据库已有该数据'
                        else:
                            self.parse_detail(href)
            except:
                with open('C:\Users\huaixuan.guan\Desktop\\222.txt', 'a') as f:
                    bt = u'主页空'+'%d, %s'%(p, url) + "\r\n"
                    # print bt, type(bt)
                    f.write(bt)
                    f.close()
                    print u'主页空'
        time.sleep(0.5)

    def parse_detail(self, href):
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:45.0) Gecko/20100101 Firefox/45.0'}
        conn_1 = MySQLdb.connect(host='172.16.0.20', port=3306, user='zhangxiaogang', passwd='gangxiaozhang',
                                 db='court_notice',charset='utf8')
        cursor_1 = conn_1.cursor()
        for i in range(5):
            try:
                cc = self.get(url=href, headers=headers)
                if u'特此公告' or u'我院定于' in cc.text:
                    break
                else:
                    continue
            except:
                with open('C:\Users\huaixuan.guan\Desktop\\222.txt', 'a') as f:
                    bt = u'网页有问题'+'%d, %d, %s'%(self.page, i, href) + "\r\n"
                    # print bt, type(bt)
                    f.write(bt)
                    f.close()
                    print u'网页有问题'
        xiang_qing = BeautifulSoup(cc.text,'html5lib')
        try:
            nei_rong3 = xiang_qing.find(style='text-align: center').find_all('p')
            fa_yuan = nei_rong3[0].text.strip().split(': ')[1]
            nei_rong1 = xiang_qing.find('div',id='ggnr').find_all_next()
            nei_rong = nei_rong1[2].get('value').split(u'ሴ')[0].strip()
            # print fa_yuan, nei_rong
            if nei_rong.endswith(u'开庭审理。'):
                print u'没有当事人'
            else:
                sql = "insert into ah_susong2nd VALUES('%s','%s','%s','%s','%s','%s')" \
                      %(self.an_hao,href,fa_yuan,nei_rong,updatetime,1)
                print self.page,self.num,sql.encode('gbk', 'ignore')
                # print self.page,self.num,sql
                try:
                    cursor_1.execute(sql)
                    conn_1.commit()
                except:
                    print 'aaaaa'
        except:
            with open('C:\Users\huaixuan.guan\Desktop\\222.txt', 'a') as f:
                bt = u'网页有问题'+'%d, %d, %s'%(self.page, i, href) + "\r\n"
                # print bt, type(bt)
                f.write(bt)
                f.close()
                print u'网页有问题'

    def get_href_from_db(self, href):
        conn_2 = MySQLdb.connect(host='172.16.0.20', port=3306, user='zhangxiaogang', passwd='gangxiaozhang',
                                 db='court_notice', charset='utf8')
        cursor_2 = conn_2.cursor()
        sql_2 = "select * from ah_susong2nd where link='%s'" % (href)
        cursor_2.execute(sql_2)
        res_2 = cursor_2.fetchall()
        if len(res_2) > 0:
            tag_a = res_2[0][1]
            return tag_a
        else:
            return None

    def update_detail(self, href):
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:45.0) Gecko/20100101 Firefox/45.0'}
        conn_1 = MySQLdb.connect(host='172.16.0.20', port=3306, user='zhangxiaogang', passwd='gangxiaozhang',
                                 db='court_notice',charset='utf8')
        cursor_1 = conn_1.cursor()
        for i in range(5):
            try:
                cc = self.get(url=href, headers=headers)
                if u'特此公告' or u'我院定于' in cc.text:
                    break
                else:
                    continue
            except:
                pass
        xiang_qing = BeautifulSoup(cc.text,'html5lib')
        try:
            # nei_rong3 = xiang_qing.find(style='text-align: center').find_all('p')
            # fa_yuan = nei_rong3[0].text.strip().split(': ')[1]
            nei_rong1 = xiang_qing.find('div',id='ggnr').find_all_next()
            nei_rong = nei_rong1[2].get('value').split(u'ሴ')[0].strip()
            # print fa_yuan, nei_rong
            if nei_rong.endswith(u'开庭审理。'):
                print u'没有当事人'
            else:
                sql = "update ah_susong2nd set nei_rong = %s, zhuang_tai= 1 " % nei_rong
                print self.page,self.num,sql.encode('gbk', 'ignore')
                # print self.page,self.num,sql
                try:
                    cursor_1.execute(sql)
                    conn_1.commit()
                except:
                    print 'aaaaa'
        except:
            pass

    def update_db(self):
        conn_2 = MySQLdb.connect(host='172.16.0.20', port=3306, user='zhangxiaogang', passwd='gangxiaozhang',
                                 db='court_notice', charset='utf8')
        cursor_2 = conn_2.cursor()
        # sql_2 = """update ah_susong2nd set zhuang_tai = 3 where zhuang_tai = 0 and nei_rong like '%2017年%' \
        # and (nei_rong like '%05月%' or nei_rong like'%06月%' or nei_rong like'%07月%' or nei_rong like'%08月%'\
        #  or nei_rong like'%09月%' or nei_rong like'%10月%' or nei_rong like'%11月%' or nei_rong like'%12月%')"""
        # cursor_2.execute(sql_2)
        # conn_2.commit()
        sql_3 = "select * from ah_susong2nd where zhuang_tai = 3"
        cursor_2.execute(sql_3)
        res_3 = cursor_2.fetchall()
        for row in res_3:
            tag_a = row[1]
            print tag_a
            self.update_detail(tag_a)

if __name__ == '__main__':
    searcher = AnHuiSearcher()
    searcher.set_config()
    # searcher.update_db()
    # searcher.run()