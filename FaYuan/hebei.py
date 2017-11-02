# coding=utf-8
# import requests
import datetime
import threading
import time

import MSSQL
import MySQLdb
from bs4 import BeautifulSoup

from ShuiWu.SpiderMan import SpiderMan


# reload(sys)
# sys.setdefaultencoding('utf8')


class HeBeiSearcher(SpiderMan):
    # DateBegin = None
    def __init__(self):
        super(HeBeiSearcher, self).__init__(keep_session=True)

    def set_config(self):
        self.DateBegin = datetime.datetime.now().strftime('%Y-%m-%d')
        start_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.conn_2 = MySQLdb.connect(host='172.16.0.20', port=3306, user='zhangxiaogang', passwd='gangxiaozhang',
                                      db='job_info', charset='utf8')
        self.cursor_2 = self.conn_2.cursor()
        sql_1 = "UPDATE ktgg_job set start_time= '%s' , updatetime= '%s' where name='hebei' " % (
        start_time, self.DateBegin)
        try:
            self.cursor_2.execute(sql_1)
            self.conn_2.commit()
        except:
            print u'更改监控开始时间报错'
        m_list = []
        m1 = threading.Thread(target=self.run,args=(1,1000))
        m_list.append(m1)
        m2 = threading.Thread(target=self.run,args=(1000,2000))
        m_list.append(m2)
        m3 = threading.Thread(target=self.run,args=(2000,3000))
        m_list.append(m3)
        m4 = threading.Thread(target=self.run,args=(3000,4000))
        m_list.append(m4)
        m5 = threading.Thread(target=self.run,args=(4000,5000))
        m_list.append(m5)
        for m in m_list:
            m.setDaemon(True)
            m.start()
        m.join()

    def run(self,n_start,n_end):
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:45.0) Gecko/20100101 Firefox/45.0'}
        host = 'http://hbgy.hbsfgk.org/ktggPage.jspx'
        conn_1 = MySQLdb.connect(host='172.16.0.20', port=3306, user='zhangxiaogang', passwd='gangxiaozhang',
                                 db='court_notice',charset='utf8')
        cursor_1 = conn_1.cursor()
        for p in range(n_start, n_end):
            param={'channelId': 431, 'listsize': 59840, 'pagego': p}
            try:
                for i in range(3):
                    try:
                        r = self.get(url=host, params=param, headers=headers)
                        if r.status_code == 200:
                            break
                    except:
                        continue
                # print r.text
                soup = BeautifulSoup(r.text, 'html5lib')
                href_list = soup.find('div', class_='sswy_sub_con_box').find('ul', class_='sswy_news').find_all('li')
                for i,item in enumerate(href_list):
                    nei_rong = item.a['title']
                    # print u'第%d页%d条'%(p, i), item.a['title']
                    sql = "insert into hebei VALUES('%s','%s')" %(nei_rong,self.DateBegin)
                    print u'第%d页%d条'%(p, i),sql.encode('gbk', 'ignore')
                    # print u'第%d页%d条'%(p, i),sql.encode('utf8', 'ignore')
                    try:
                        cursor_1.execute(sql)
                        conn_1.commit()
                    except:
                        print u'数据库已有该数据'
            except:
                print n_start,'bbb'
                pass
        time.sleep(0.5)


if __name__ == '__main__':
    searcher = HeBeiSearcher()
    searcher.set_config()
    d1 = datetime.datetime.now()
    # searcher.run(1, 2)
    MSSQL.execute_sop('hebei')
    d2 = datetime.datetime.now()
    dd = d2-d1
    print dd, u'一共运行%s秒'%dd