# coding=utf-8
import os
import requests
import time
import re
from bs4 import BeautifulSoup

from SpiderMan import SpiderMan
from Mysql_Config_Fyh import data_to_mysql
from Mysql_Config_Fyh import logger


class GuangXiYuLinCrawler(SpiderMan):
    def __init__(self):
        super(GuangXiYuLinCrawler, self).__init__(keep_session=False)

    def log_info(self, message):
        self
        log_name = 'gx_yl_fy.log'
        logger(log_name, message)

    def run(self):
        log_name = 'gx_yl_fy.log'
        start_time = time.strftime('%Y-%m-%d %H:%M:%S')
        start_sql = "update ktgg_job set start_time='" + start_time + "', status = '0' where name = 'gx_yl_fy'"
        data_to_mysql(log_name, 1, start_sql)
        host = 'http://ylszy.chinacourt.org'
        repeat_time = 0
        max_repeat_time = 300
        updatetime = time.strftime('%Y-%m-%d')
        for i in range(1, 10):
            url = 'http://ylszy.chinacourt.org/article/index/id/M8g0NzAwMTAwMiACAAA%3D/page/' + str(i) + '.shtml'
            r = self.get(url)
            r.encoding = 'utf-8'
            res = BeautifulSoup(r.text, 'html5lib')
            break_condition = repeat_time > max_repeat_time
            if break_condition:
                self.log_info('break_condition: repeat_time > ' + str(max_repeat_time))
                break
            lis_div = res.findAll('div', {'id': 'list'})
            if lis_div:
                lis = lis_div[-1].findAll('li')
                a_list = [li.find('a') for li in lis if u'开庭公告' in li.text.replace(' ', '')]
                for a_tag in a_list:
                    href = a_tag.get('href')
                    inner_url = host + href
                    r_inner = self.get(inner_url)
                    r_inner.encoding = 'utf-8'
                    res_inner = BeautifulSoup(r_inner.text, 'html5lib')
                    content_div = res_inner.findAll('div', {'class': 'text'})
                    if content_div:
                        contents = content_div[0].text.strip().split(u'\n\n')
                        choose_condition = len(contents) % 5 == 0
                        if choose_condition:
                            data_num = len(contents) / 5
                            self.log_info(str(i) + ',' + inner_url + ',' + str(len(contents)) + ',' + str(data_num))
                            for j in range(data_num):
                                an_hao = re.subn(ur'\d+、', u'', contents[j * 5])[0].replace(u'案号：', u'').strip()
                                nei_rong = contents[j * 5 + 1]
                                if u'开庭时间' in contents[j * 5 + 2]:
                                    kai_ting_shi_jian = contents[j * 5 + 2].replace(u'开庭时间：', u'')
                                else:
                                    self.log_info('not kai_ting_shi_jian, break')
                                    break
                                kai_ting_di_dian = contents[j * 5 + 3].replace(u'开庭地点：', u'')
                                he_yi_ting_cheng_yuan = contents[j * 5 + 4].replace(u'合议庭成员：', u'')
                                sql = "insert into gx_yl_fy VALUES('%s','%s','%s','%s','%s','%s','%s')" % \
                                      (an_hao, nei_rong, kai_ting_shi_jian, kai_ting_di_dian, he_yi_ting_cheng_yuan,
                                       inner_url, updatetime)
                                repeat_time = data_to_mysql(log_name, 0, sql, repeat_time)
                    else:
                        self.log_info(str(i) + ',' + inner_url)
            else:
                self.log_info(url + ', this page not found lis_div')
        stop_time = time.strftime('%Y-%m-%d %H:%M:%S')
        end_sql = "update ktgg_job set stop_time = '" + stop_time + "',updatetime = '" + updatetime + \
                  "',status = '1' where name = 'gx_yl_fy'"
        data_to_mysql(log_name, 1, end_sql)


if __name__ == '__main__':
    crawler = GuangXiYuLinCrawler()
    crawler.run()
