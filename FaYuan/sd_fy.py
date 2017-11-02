# coding=utf-8
import requests
import os
import re
import time
from bs4 import BeautifulSoup

from SpiderMan import SpiderMan
from Mysql_Config_Fyh import data_to_mysql
from Mysql_Config_Fyh import logger


class ShangDongCrawler(SpiderMan):
    def __init__(self):
        super(ShangDongCrawler, self).__init__(keep_session=False)

    def log_info(self, message):
        self
        log_name = 'sd_fy.log'
        logger(log_name, message)

    def run(self):
        log_name = 'sd_fy.log'
        start_time = time.strftime('%Y-%m-%d %H:%M:%S')
        add_time = time.strftime('%Y-%m-%d')
        start_sql = "update ktgg_job set start_time='" + start_time + "', status = '0' where name = 'sd_fy'"
        data_to_mysql(log_name, 1, start_sql)
        fa_yuan_dai_mas = [
            '0F',
            '0F1', '0F11', '0F12', '0F13', '0F14', '0F15', '0F16', '0F17', '0F18', '0F19', '0F1A', '0F1B',
            '0F2', '0F21', '0F22', '0F25', '0F26', '0F27', '0F28', '0F29', '0F2A', '0F2B', '0F2D',
            '0F3', '0F31', '0F32', '0F33', '0F34', '0F35', '0F36', '0F37', '0F38', '0F39',
            '0F4', '0F41', '0F42', '0F43', '0F44', '0F45', '0F46',
            '0F5', '0F51', '0F52', '0F53', '0F54', '0F55', '0F56',
            '0F6', '0F61', '0F62', '0F63', '0F64', '0F65', '0F66', '0F67', '0F68', '0F69', '0F6A', '0F6B', '0F6C',
            '0F6D',
            '0F6E',
            '0F7', '0F71', '0F72', '0F73', '0F74', '0F75', '0F76', '0F77', '0F78', '0F79', '0F7A', '0F7B', '0F7D',
            '0F7E',
            '0F7F',
            '0F8', '0F82', '0F83', '0F84', '0F85', '0F86', '0F87', '0F88', '0F89', '0F8A', '0F8B', '0F8C', '0F8D',
            '0F9', '0F91', '0F92', '0F94', '0F95', '0F96', '0F97', '0F98',
            '0FA', '0FA1', '0FA2', '0FA4', '0FA6',
            '0FB', '0FB2', '0FB3', '0FB4', '0FB5', '0FB6',
            '0FC', '0FC1', '0FC2', '0FC5', '0FC6', '0FC7', '0FC8',
            '0FD', '0FD1', '0FD3', '0FD4', '0FD5', '0FD6', '0FD7', '0FD8', '0FD9', '0FDA', '0FDC',
            '0FE', '0FE1', '0FE2', '0FE3', '0FE4', '0FE5', '0FE6', '0FE7', '0FE8',
            '0FF', '0FF1', '0FF2', '0FF4', '0FF6', '0FF7', '0FF8', '0FF9', '0FFA', '0FFB', '0FFC', '0FFD', '0FFE',
            '0FFF',
            '0FG', '0FG1', '0FG2', '0FG3', '0FG4', '0FG5', '0FG6', '0FG7', '0FG8', '0FG9', '0FGA',
            '0FH1', '0FH2',
            '0FI',
            '0FJ', '0FJ1', '0FJ2'
        ]
        url = 'http://www.sdcourt.gov.cn/sdfy_search/tsxx/list.do'
        for i in range(0, len(fa_yuan_dai_mas)):
            fa_yuan_dai_ma = fa_yuan_dai_mas[i]
            self.log_info('法院代码: ' + fa_yuan_dai_ma + ',' + str(i))
            data = {
                'tsxx.court_no': fa_yuan_dai_ma,
                'Submit1': '检索'
            }
            r = self.post(url=url, data=data)
            r.encoding = 'utf-8'
            res = BeautifulSoup(r.text, 'html5lib')
            span = res.findAll('span', {'class': 'fengye'})
            per_page = 10
            if span:
                if len(span) > 1:
                    records = int(re.findall('\d+', span[1].text)[0])
                    if records:
                        total_page = (records / per_page) + 1
                        self.log_info(str(total_page) + '总页数' + fa_yuan_dai_ma)
                        for j in range(total_page):
                            data = {
                                'tsxx.court_no': fa_yuan_dai_ma,
                                'curPage': j + 1
                            }
                            r_page = self.post(url, data=data)
                            r_page.encoding = 'utf-8'
                            res_page = BeautifulSoup(r_page.text, 'html5lib')
                            table = res_page.findAll('table', {'id': 'tsxxTableId'})
                            if table:
                                trs = table[0].findAll('tr')
                                if trs:
                                    new_trs = trs[1:]
                                    for tr in new_trs:
                                        tds = tr.findAll('td')
                                        fa_yuan = tds[0].text.strip()
                                        fa_ting = tds[1].text.strip()
                                        kai_ting_ri_qi = tds[2].text.strip()
                                        an_you = tds[3].text.strip()
                                        shen_pan_zhang = tds[4].text.strip()
                                        yuan_gao = tds[5].text.strip().replace(u'\n', '')
                                        new_yuan_gao = ''
                                        for yuan_gao_chip in yuan_gao.split():
                                            new_yuan_gao += yuan_gao_chip
                                        bei_gao = tds[6].text.strip().replace(u'\n', '')
                                        new_bei_gao = ''
                                        for bei_gao_chip in bei_gao.split():
                                            new_bei_gao += bei_gao_chip
                                        sql = "insert into sd_fy VALUES('%s','%s','%s','%s','%s','%s','%s','%s')" % \
                                              (fa_yuan, fa_ting, kai_ting_ri_qi, an_you, shen_pan_zhang, new_yuan_gao,
                                               new_bei_gao, add_time)
                                        data_to_mysql(log_name, 0, sql)
                                else:
                                    self.log_info(fa_yuan_dai_ma + str(j + 1) + '有table, 没trs')
                            else:
                                self.log_info(fa_yuan_dai_ma + str(j + 1) + '页no table')
                    else:
                        self.log_info('no record, '+ fa_yuan_dai_ma)
                else:
                    self.log_info('no zongyeshu span, ' + fa_yuan_dai_ma)
            else:
                self.log_info('no span, ' + fa_yuan_dai_ma)
        stop_time = time.strftime('%Y-%m-%d %H:%M:%S')
        end_sql = "update ktgg_job set stop_time = '" + stop_time + "',updatetime = '" + add_time + \
                  "',status = '1' where name = 'sd_fy'"
        data_to_mysql(log_name, 1, end_sql)


if __name__ == '__main__':
    crawler = ShangDongCrawler()
    crawler.run()
