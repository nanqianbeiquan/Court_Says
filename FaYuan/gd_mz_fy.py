# coding=utf-8
import os
import sys
import requests
import time
import re
from bs4 import BeautifulSoup

from SpiderMan import SpiderMan
from Mysql_Config_Fyh import data_to_mysql
from Mysql_Config_Fyh import logger


class GuangDongMeiZhouCrawler(SpiderMan):
    def __init__(self):
        super(GuangDongMeiZhouCrawler, self).__init__(keep_session=False)

    def log_info(self, message):
        self
        log_name = 'gd_mz_fy.log'
        logger(log_name, message)

    def find_table(self, tag):
        table = tag.find('table')
        if table:
            table = self.find_table(table)
            return table
        else:
            return tag

    def run(self):
        log_name = 'gd_mz_fy.log'
        start_time = time.strftime('%Y-%m-%d %H:%M:%S')
        start_sql = "update ktgg_job set start_time='" + start_time + "', status = '0' where name = 'gd_mz_fy'"
        data_to_mysql(log_name, 1, start_sql)
        updatetime = time.strftime('%Y-%m-%d')
        host = 'http://www.mzcourt.gov.cn'
        min_content_tag_length = 6
        repeat_time = 0
        max_repeat_time = 300
        for i in range(1, 3):
            url = 'http://www.mzcourt.gov.cn/fayuangonggao/kaitinggonggao/list_43_' + str(i) + '.html'
            r = self.get(url)
            r.encoding = 'gbk'
            res = BeautifulSoup(r.text, 'html5lib')
            break_condition = repeat_time > max_repeat_time
            if break_condition:
                self.log_info('break_condition: repeat_time > ' + str(max_repeat_time))
                break
            lis_div = res.findAll('div', {'class': 'news_pic_list'})
            if lis_div:
                lis = lis_div[0].findAll('li')
                a_list = [li.find('a') for li in lis]
                for a_tag in a_list:
                    href = a_tag.get('href')
                    inner_url = host + href
                    link_id = re.findall('\d+', inner_url)[2]
                    self.log_info(inner_url + ',' + str(link_id))
                    r_inner = self.get(inner_url)
                    r_inner.encoding = 'gbk'
                    res_inner = BeautifulSoup(r_inner.text, 'html5lib')
                    inner_div = res_inner.findAll('div', {'class': 'article_content_wrap'})
                    if inner_div:
                        tag = self.find_table(inner_div[0])
                        trs = tag.findAll('tr')
                        if trs:
                            new_trs = [tr for tr in trs if len(tr.findAll('td')) > min_content_tag_length]
                            for tr in new_trs[1:]:
                                tds = tr.findAll('td')
                                an_hao = tds[1].text.strip()
                                dang_shi_ren = tds[2].text.strip()
                                an_you = tds[3].text.strip()
                                cheng_ban_fa_guan = tds[4].text.strip()
                                kai_ting_shi_jian = tds[5].text.strip()
                                kai_ting_di_dian = tds[7].text.strip()
                                sql = "INSERT INTO gd_mz_fy VALUES ('%s','%s','%s','%s','%s','%s','%s','%s')" \
                                      % (link_id, an_hao, dang_shi_ren, an_you, cheng_ban_fa_guan, kai_ting_shi_jian,
                                         kai_ting_di_dian, updatetime)
                                repeat_time = data_to_mysql(log_name, 0, sql, repeat_time)
                        else:
                            divs = tag.findAll('div')
                            if divs:
                                new_divs = [div for div in divs if len(div.findAll('span')) > min_content_tag_length]
                                for div in new_divs:
                                    contents = div.text.strip().split('	')
                                    an_hao = contents[1]
                                    dang_shi_ren = contents[2]
                                    an_you = contents[3]
                                    cheng_ban_fa_guan = contents[4]
                                    kai_ting_shi_jian = contents[5]
                                    kai_ting_di_dian = contents[7]
                                    sql = "INSERT INTO gd_mz_fy VALUES ('%s','%s','%s','%s','%s','%s','%s','%s')" \
                                          % (link_id, an_hao, dang_shi_ren, an_you, cheng_ban_fa_guan,
                                             kai_ting_shi_jian, kai_ting_di_dian, updatetime)
                                    repeat_time = data_to_mysql(log_name, 0, sql, repeat_time)
                            else:
                                p = tag.findAll('p')
                                if p:
                                    p_str = p[0].encode('utf-8')
                                    contents = p_str.split('<br/>')
                                    new_contents = contents[1:]
                                    for content in new_contents:
                                        content_pieces = content.split(' ')
                                        if len(content_pieces) > min_content_tag_length:
                                            an_hao = content_pieces[1]
                                            dang_shi_ren = content_pieces[2]
                                            an_you = content_pieces[3]
                                            cheng_ban_fa_guan = content_pieces[4]
                                            kai_ting_shi_jian = content_pieces[6]
                                            kai_ting_di_dian = content_pieces[7].replace('</p>', '')
                                            sql = "INSERT INTO gd_mz_fy VALUES " \
                                                  "('%s','%s','%s','%s','%s','%s','%s','%s')" \
                                                  % (str(link_id), an_hao, dang_shi_ren, an_you, cheng_ban_fa_guan,
                                                     kai_ting_shi_jian, kai_ting_di_dian, updatetime)
                                            repeat_time = data_to_mysql(log_name, 0, sql, repeat_time)
                                        else:
                                            self.log_info(inner_url + 'other ways')
                                else:
                                    self.log_info('no p')
                    else:
                        self.log_info('no inner_div')
            else:
                self.log_info(url + ', this page has no lis_div')
        stop_time = time.strftime('%Y-%m-%d %H:%M:%S')
        end_sql = "update ktgg_job set stop_time = '" + stop_time + "',updatetime = '" + updatetime + \
                  "',status = '1' where name = 'gd_mz_fy'"
        data_to_mysql(log_name, 1, end_sql)


if __name__ == '__main__':
    crawler = GuangDongMeiZhouCrawler()
    crawler.run()
