# coding=utf-8
import os
import sys
import requests
import time
from bs4 import BeautifulSoup
import datetime
import re

from SpiderMan import SpiderMan
from Mysql_Config_Fyh import data_to_mysql
from Mysql_Config_Fyh import logger


class GuangDongShanWeiCrawler(SpiderMan):
    def __init__(self):
        super(GuangDongShanWeiCrawler, self).__init__(keep_session=False)

    def log_info(self, message):
        self
        log_name = 'gd_sw_fy.log'
        logger(log_name, message)

    def run(self):
        log_name = 'gd_sw_fy.log'
        today = datetime.datetime.now().strftime('%Y-%m-%d')
        start_time = time.strftime('%Y-%m-%d %H:%M:%S')
        start_sql = "update ktgg_job set start_time='" + start_time + "', status = '0' where name = 'gd_sw_fy'"
        data_to_mysql(log_name, 1, start_sql)
        shi_qu = u'汕尾市'
        host = 'http://www.swzy.gov.cn'
        repeat_time = 0
        max_repeat_time = 50
        for n in range(13):
            url = 'http://www.swzy.gov.cn/newslist.aspx?page=' + str(n) + '&MenuID=02020401'
            r = self.get(url)
            r.encoding = 'utf-8'
            res = BeautifulSoup(r.text, 'html5lib')
            break_condition = repeat_time > max_repeat_time
            if break_condition:
                self.log_info('break_condition: repeat_time > ' + str(max_repeat_time))
                break
            ul = res.findAll('ul', {'class': 'mlist'})
            if ul:
                lis = ul[0].findAll('li')
                a_list = [li.find('a') for li in lis]
                for a_tag in a_list:
                    href = a_tag.get('href')
                    inner_url = host + href
                    link_id = re.findall('\d+', href)[1]
                    r_detail = self.get(inner_url)
                    self.log_info(link_id + ':' + inner_url)
                    r_detail.encoding = 'utf-8'
                    res_detail = BeautifulSoup(r_detail.text, 'html5lib')
                    div = res_detail.findAll('div', {'class': 'decon'})
                    if div:
                        div_text = div[0].text.strip().replace(u'\n', '')
                        if u'书记员' in div_text:
                            shu_ji_yuan = div_text.split(u'书记员:')[1]
                            p_list = div[0].findAll('p', {'class': 'MsoNormal'})
                            contents = u''
                            for p in p_list:
                                if u'案号' in p.text.strip() or u'案由' in p.text.strip() or u'开庭时间' in p.text.strip() \
                                        or u'开庭地点' in p.text.strip() or u'主审法官' in p.text.strip():
                                    contents += p.text.strip() + u','
                                elif u'立案日期' in p.text.strip():
                                    contents += u',' + p.text.strip() + u','
                                elif u'书记员' not in p.text.strip():
                                    contents += p.text.strip()
                            new_contents = [content for content in contents.split(u',') if content]
                            if len(new_contents) == 7:
                                an_hao = new_contents[0].replace(u'案号:', '')
                                an_you = new_contents[1].replace(u'案由:', '')
                                dang_shi_ren = new_contents[2].replace(u'当事人:', u' ').strip().replace(u' ', u'；')
                                li_an_ri_qi = new_contents[3].replace(u'立案日期:', '')
                                kai_ting_shi_jian = new_contents[4].replace(u'开庭时间:', '')
                                kai_ting_di_dian = new_contents[5].replace(u'开庭地点:', '')
                                zhu_shen_fa_guan = new_contents[6].replace(u'主审法官:', '')
                                sql = "insert into gd_sw_fy VALUES " \
                                      "('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" \
                                      % (shi_qu, link_id, an_hao, an_you, dang_shi_ren, li_an_ri_qi, kai_ting_shi_jian,
                                         kai_ting_di_dian, zhu_shen_fa_guan, shu_ji_yuan, today)
                                repeat_time = data_to_mysql(log_name, 0, sql, repeat_time)
                        else:
                            self.log_info(inner_url + ', this page has no shu_ji_yuan')
                    else:
                        self.log_info(inner_url + ', this page has no target div')
        stop_time = time.strftime('%Y-%m-%d %H:%M:%S')
        end_sql = "update ktgg_job set stop_time = '" + stop_time + "',updatetime = '" + today + \
                  "',status = '1' where name = 'gd_sw_fy'"
        data_to_mysql(log_name, 1, end_sql)


if __name__ == '__main__':
    crawler = GuangDongShanWeiCrawler()
    crawler.run()
