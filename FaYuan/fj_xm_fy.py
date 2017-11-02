# coding=utf-8
import os
import sys
import requests
import time
from bs4 import BeautifulSoup
import datetime
import MySQLdb
import threading
import re

from SpiderMan import SpiderMan
from Mysql_Config_Fyh import data_to_mysql
from Mysql_Config_Fyh import logger


class FuJianXiaMenCrawler(SpiderMan):
    def __init__(self):
        super(FuJianXiaMenCrawler, self).__init__(keep_session=False)

    def log_info(self, message):
        self
        log_name = 'fj_xm_fy.log'
        logger(log_name, message)

    def run(self):
        log_name = 'fj_xm_fy.log'
        start_time = time.strftime('%Y-%m-%d %H:%M:%S')
        start_sql = "update ktgg_job set start_time='" + start_time + "', status = '0' where name = 'xiamenfy'"
        data_to_mysql(log_name, 1, start_sql)
        updatetime = datetime.datetime.now().strftime('%Y-%m-%d')
        today = datetime.datetime.now().strftime('%Y-%m-%d')
        host = 'http://202.101.105.162:8099/court/ktgg/'
        repeat_time = 0
        max_repeat_time = 30000
        for p in range(0, 50):
            url = 'http://202.101.105.162:8099/court/ktgg/ktgg_list_' + str(p) + '.xhtml?page=' + str(p)
            r = requests.get(url)
            rbs = BeautifulSoup(r.text, 'html5lib')
            tr_list = rbs.find_all(class_='xmfyw_sxl_ctab f_c t14 h14')[1].find_all('tr')
            if len(tr_list) > 1:
                break_condition = repeat_time > max_repeat_time
                if break_condition:
                    self.log_info('break_condition: repeat_time > ' + str(max_repeat_time))
                    break
                for i in range(1, len(tr_list)):
                    td = tr_list[i].find_all('td')[5].a
                    linp = td['href']
                    if '=' in linp:
                        link_id = linp.split('=')[1]
                    else:
                        link_id = re.search(r'\d{6,}', linp).group()
                    # link_id = re.search(r'\d{6,}', linp).group()
                    link = host + linp
                    # print i,tr_list[i].text,link
                    self.log_info(str(p) + ',' + str(i) + ',' + link)
                    r1 = requests.get(link)
                    r1bs = BeautifulSoup(r1.text, 'html5lib')
                    r_tr = r1bs.find(class_='xmfyw_sxl_ctab t14').find_all('tr')
                    if r_tr:
                        fa_yuan_ming_cheng = r_tr[0].find_all('td')[1].text.strip()
                        an_hao = r_tr[1].find_all('td')[1].text.strip()
                        kai_ting_shi_jian = r_tr[2].find_all('td')[1].text.strip()
                        kai_ting_di_dian = r_tr[3].find_all('td')[1].text.strip()
                        fa_guan = r_tr[4].find_all('td')[1].text.strip()
                        cheng_ban_ting = r_tr[5].find_all('td')[1].text.strip()
                        shu_ji_yuan = r_tr[6].find_all('td')[1].text.strip()
                        an_jian_shuo_ming = r_tr[7].find_all('td')[1].text.strip()
                        sql = "insert into xiamenfy VALUES('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (
                            link_id, an_hao, fa_yuan_ming_cheng, kai_ting_shi_jian, kai_ting_di_dian, fa_guan,
                            cheng_ban_ting, shu_ji_yuan, an_jian_shuo_ming, today)
                        repeat_time = data_to_mysql(log_name, 0, sql, repeat_time)
                    else:
                        self.log_info(str(i) + ',' + link + ', no r_tr')
            elif p > 9:
                stop_time = time.strftime('%Y-%m-%d %H:%M:%S')
                end_sql = "update ktgg_job set stop_time = '" + stop_time + "',updatetime = '" + updatetime + \
                          "',status = '1' where name = 'xiamenfy'"
                data_to_mysql(log_name, 1, end_sql)
                break


if __name__ == '__main__':
    crawler = FuJianXiaMenCrawler()
    crawler.run()
