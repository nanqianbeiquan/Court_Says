# coding=utf-8
import os
import sys
import time
import requests
import MySQLdb
from bs4 import BeautifulSoup
import re

from SpiderMan import SpiderMan
from Mysql_Config_Fyh import data_to_mysql
from Mysql_Config_Fyh import logger


class TianJinCrawler(SpiderMan):

    def __init__(self):
        super(TianJinCrawler, self).__init__(keep_session=False)

    def log_info(self, message):
        self
        log_name = 'tj_fy.log'
        logger(log_name, message)

    def run(self):
        log_name = 'tj_fy.log'
        start_time = time.strftime('%Y-%m-%d %H:%M:%S')
        start_sql = "update ktgg_job set start_time='" + start_time + "', status = '0' where name = 'tianjin2nd'"
        data_to_mysql(log_name, 1, start_sql)
        shi_qu = u'天津市'
        updatetime = time.strftime('%Y-%m-%d')
        host = 'http://tjfy.chinacourt.org'
        repeat_time = 0
        max_repeat_time = 2000
        for i in range(1, 2):
            url = 'http://tjfy.chinacourt.org/article/index/id/MzDIMTCwMDAwNCACAAA%3D/page/' + str(i) + '.shtml'
            r = self.get(url)
            r.encoding = 'utf-8'
            soup = BeautifulSoup(r.text, 'html5lib')
            list_div = soup.findAll('div', {'id': 'list'})
            if len(list_div) == 2:
                lis = list_div[1].findAll('li')
                self.log_info('lis: ' + str(len(lis)))
                for j in range(0, len(lis)):
                    break_condition = repeat_time > max_repeat_time
                    if break_condition:
                        self.log_info('break_condition: repeat_time > ' + str(max_repeat_time))
                        break
                    href = lis[j].a['href']
                    url_inner = host + href
                    i_d = re.search(r'\d{5,}', href).group()
                    r_inner = self.get(url_inner)
                    r_inner.encoding = 'utf-8'
                    soup_inner = BeautifulSoup(r_inner.text, 'html5lib')
                    # print soup_inner
                    content_div = soup_inner.findAll('div', {'class': 'text'})
                    if content_div:
                        contents = content_div[0].text.strip().split('\n')
                        new_contents = [content for content in contents if content]
                        rq_fy_list = [new_content for new_content in new_contents if u'定于' in new_content]
                        an_you_list = []
                        temp_c = []
                        # for c in range(len(new_contents)):
                        #     if u'定于' not in new_contents[c]:
                        #         if new_contents[c] == u'在交通巡回第二法庭审理林作斌与宋尊如,吕凤英,曲明华' or \
                        #                         new_contents[c] == u'在交通巡回第二法庭审理李书华与宋尊如,吕凤英,曲明华' or \
                        #                         new_contents[c] == u'在交通巡回第二法庭审理王先飞与宋尊如,吕凤英,曲明华' or \
                        #                         new_contents[c] == u'在第十八小法庭审理班秀军,中国人民财产保险股份有限公司' \
                        #                                            u'辛集支公司与辛集市久诚运输队':
                        #             an_you_list.append(new_contents[c] + new_contents[c + 1])
                        #             temp_c.append(c + 1)
                        #         elif c not in temp_c:
                        #             an_you_list.append(new_contents[c])
                        rq_fy_list = new_contents[::2]
                        an_you_list = new_contents[1::2]
                        self.log_info('j + 1, len(rq_fy_list), len(an_you_list)')
                        self.log_info(str(j + 1) + ',' + str(len(rq_fy_list)) + ',' + str(len(an_you_list)))
                        # print j + 1, len(rq_fy_list), len(an_you_list)
                        for k in range(len(rq_fy_list)):
                            if u'定于' not in rq_fy_list[k]:
                                self.log_info('rq_fy_list[k]: ' + rq_fy_list[k])
                                # print rq_fy_list[k]
                                break
                            ri_qi = rq_fy_list[k].split(u'定于')[1]
                            fa_yuan = rq_fy_list[k].split(u'定于')[0]
                            an_you = an_you_list[k]
                            sql = "insert into tianjin2nd VALUES('%s','%s','%s','%s','%s','%s')" % \
                                  (i_d, fa_yuan, ri_qi, an_you, updatetime, shi_qu)
                            repeat_time = data_to_mysql(log_name, 0, sql, repeat_time=repeat_time)
                    else:
                        self.log_info('content_div not found: ' + str(j + 1) + ',' + url_inner)
                stop_time = time.strftime('%Y-%m-%d %H:%M:%S')
                end_sql = "update ktgg_job set stop_time = '" + stop_time + "',updatetime = '" + updatetime + \
                          "',status = '1' where name = 'tianjin2nd'"
                data_to_mysql(log_name, 1, end_sql)
            else:
                self.log_info('list_div not found: ' + str(i + 1) + ',' + url)


if __name__ == '__main__':
    crawler = TianJinCrawler()
    crawler.run()