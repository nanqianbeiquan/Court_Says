# coding=utf-8
import os
import requests
import time
from bs4 import BeautifulSoup

from SpiderMan import SpiderMan
from Mysql_Config_Fyh import data_to_mysql
from Mysql_Config_Fyh import logger


class JiangSuJiangYinCrawler(SpiderMan):
    def __init__(self):
        super(JiangSuJiangYinCrawler, self).__init__(keep_session=False)

    def log_info(self, message):
        self
        log_name = 'js_jy_fy.log'
        logger(log_name, message)

    def run(self):
        log_name = 'js_jy_fy.log'
        start_time = time.strftime('%Y-%m-%d %H:%M:%S')
        start_sql = "update ktgg_job set start_time='" + start_time + "', status = '0' where name = 'js_jy_fy'"
        data_to_mysql(log_name, 1, start_sql)
        host = 'http://jsjyfy.chinacourt.org'
        shi_qu = u'江阴市'
        add_time = time.strftime('%Y-%m-%d')
        last_update_time = time.strftime('%Y-%m-%d %H:%M:%S')
        repeat_time = 0
        max_repeat_time = 300
        for i in range(1, 18):
            url = 'http://jsjyfy.chinacourt.org/article/index/id/MygqNzDINiAOAAA%3D/page/' + str(i) + '.shtml'
            headers = {
                'Referer': url
            }
            break_condition = repeat_time > max_repeat_time
            if break_condition:
                self.log_info('break_condition: repeat_time > ' + str(max_repeat_time))
                break
            r = self.get(url, headers=headers)
            r.encoding = 'utf-8'
            res = BeautifulSoup(r.text, 'html5lib')
            lis_div = res.findAll('div', {'class': 'list_br'})
            if lis_div:
                lis = lis_div[-1].findAll('li')
                a_list = [li.find('a') for li in lis if u'开庭公告' in li.text.strip()]
                for a_tag in a_list:
                    href = a_tag.get('href')
                    inner_url = host + href
                    self.log_info(str(i) + ',' + inner_url)
                    r_inner = self.get(inner_url)
                    r_inner.encoding = 'utf-8'
                    res_inner = BeautifulSoup(r_inner.text, 'html5lib')
                    text_div = res_inner.findAll('div', {'class': 'text'})
                    if text_div:
                        p_list = text_div[0].findAll('p', {'class': 'MsoNormal'})
                        new_p_list = [p for p in p_list if p.text.strip()]
                        p_combinations = []
                        temp = 0
                        for j in range(len(new_p_list)):
                            if u'案  号' in new_p_list[j].text.strip() and j > 1:
                                p_combinations.append(new_p_list[temp: j])
                                temp = j
                        p_combinations.append(new_p_list[temp:])
                        for ps in p_combinations:
                            an_hao = u''
                            an_you = u''
                            dang_shi_ren = u''
                            cheng_ban_ren = u''
                            ri_qi = u''
                            shi_jian = u''
                            shu_ji_yuan = u''
                            for p in ps:
                                if u'案  号' in p.text.strip().split(u'：')[0]:
                                    an_hao = p.text.strip().split(u'：')[1]
                                elif u'案  由' in p.text.strip().split(u'：')[0]:
                                    an_you = p.text.strip().split(u'：')[1]
                                elif u'当事人' in p.text.strip().split(u'：')[0]:
                                    dang_shi_ren = p.text.strip().split(u'：')[1]
                                elif u'地  点' in p.text.strip().split(u'：')[0]:
                                    di_dian = p.text.strip().split(u'：')[1]
                                elif u'日  期' in p.text.strip().split(u'：')[0]:
                                    ri_qi = p.text.strip().split(u'：')[1]
                                elif u'时  间' in p.text.strip().split(u'：')[0]:
                                    shi_jian = p.text.strip().split(u'：')[1]
                                elif u'承办人' in p.text.strip().split(u'：')[0] \
                                        or u'审判长' in p.text.strip().split(u'：')[0] \
                                        or u'主审法官' in p.text.strip().split(u'：')[0]:
                                    cheng_ban_ren = p.text.strip().split(u'：')[1]
                                elif u'书记员' in p.text.strip().split(u'：')[0]:
                                    shu_ji_yuan = p.text.strip().split(u'：')[1]
                                else:
                                    print p.text.strip()
                            if not an_hao:
                                continue
                            sql = "insert into js_jy_fy VALUES" \
                                  "('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (
                                      shi_qu, an_hao, an_you, dang_shi_ren, cheng_ban_ren, ri_qi, shi_jian, shu_ji_yuan,
                                      inner_url, add_time, last_update_time)
                            repeat_time = data_to_mysql(log_name, 0, sql, repeat_time)
            else:
                self.log_info(url + ', this page has no lis_div')
        stop_time = time.strftime('%Y-%m-%d %H:%M:%S')
        end_sql = "update ktgg_job set stop_time = '" + stop_time + "',updatetime = '" + add_time + \
                  "',status = '1' where name = 'js_jy_fy'"
        data_to_mysql(log_name, 1, end_sql)


if __name__ == '__main__':
    crawler = JiangSuJiangYinCrawler()
    crawler.run()
