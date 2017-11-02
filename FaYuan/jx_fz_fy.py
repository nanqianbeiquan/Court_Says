# coding=utf-8
import requests
import os
import HTMLParser
import re
import time
from bs4 import BeautifulSoup

from SpiderMan import SpiderMan
from Mysql_Config_Fyh import data_to_mysql
from Mysql_Config_Fyh import logger


class JiangXiFuZhouCrawler(SpiderMan):
    def __init__(self):
        super(JiangXiFuZhouCrawler, self).__init__(keep_session=False)

    def get_right_url(self, url):
        self
        html_parser = HTMLParser.HTMLParser()
        url_new = html_parser.unescape(url)
        return url_new

    def log_info(self, message):
        self
        log_name = 'jx_fz_fy.log'
        logger(log_name, message)

    def run(self):
        log_name = 'jx_fz_fy.log'
        start_time = time.strftime('%Y-%m-%d %H:%M:%S')
        start_sql = "update ktgg_job set start_time='" + start_time + "', status = '0' where name = 'jx_fz_fy'"
        data_to_mysql(log_name, 1, start_sql)
        shi_qu = u'抚州市'
        url_dict_list = [
            {u'抚州中级人民法院': 'http://fzzy.susong51.com/ktgg/index.jhtml'},  # 抚州中级人民法院
            {u'抚州市临川区人民法院': 'http://fzlcfy.susong51.com/ktgg/index.jhtml'},  # 抚州市临川区人民法院
            {u'南城县人民法院': 'http://fzncfy.susong51.com/ktgg/index.jhtml'},  # 南城县人民法院
            {u'黎川县人民法院': 'http://fzlchfy.susong51.com/ktgg/index.jhtml'},  # 黎川县人民法院

            # {u'南丰县人民法院': 'http://fznffy.susong51.com/ktgg/index.jhtml'},  # 南丰县人民法院  数据只有2015年，
            # {u'崇仁县人民法院': 'http://fzcrfy.susong51.com/ktgg/index.jhtml'},  # 崇仁县人民法院  暂无数据

            {u'乐安县人民法院': 'http://fzlafy.susong51.com/ktgg/index.jhtml'},  # 乐安县人民法院 里面的页码不可点
            {u'宜黄县人民法院': 'http://fzyhfy.susong51.com/ktgg/index.jhtml'},  # 宜黄县人民法院
            {u'金溪县人民法院': 'http://fzjxfy.susong51.com/ktgg/index.jhtml'},  # 金溪县人民法院
            {u'资溪县人民法院': 'http://fzzxfy.susong51.com/ktgg/index.jhtml'},  # 资溪县人民法院 里面的页码不可点
            {u'东乡县人民法院': 'http://fzdxfy.susong51.com/ktgg/index.jhtml'},  # 东乡县人民法院
            {u'广昌县人民法院': 'http://fzgcfy.susong51.com/ktgg/index.jhtml'},  # 广昌县人民法院

        ]
        filter_fa_yuans = [u'宜黄县人民法院', u'金溪县人民法院', u'广昌县人民法院', u'乐安县人民法院',
                           u'资溪县人民法院']
        shi_jian_pattern = r'\d{4}-\d{2}-\d{2}.*?\d{2}:\d{2}'
        add_time = time.strftime('%Y-%m-%d')
        max_repeat_time = 100
        for url_dict in url_dict_list:
            fa_yuan = url_dict.keys()[0]
            fa_yuan_str = fa_yuan.encode('utf-8')
            url = url_dict.values()[0]
            host = url.split('/ktgg/')[0]
            self.log_info(fa_yuan_str + ': ' + url)
            r = self.get(url)
            r.encoding = 'utf-8'
            res = BeautifulSoup(r.text, 'html5lib')
            if fa_yuan not in filter_fa_yuans:
                page_div = res.findAll('div', {'class': 'turn_page'})
                if page_div:
                    a_list = page_div[0].findAll('a', {'class': 'zt_02'})
                    if a_list:
                        fa_yuan_pages = a_list[-1].text.strip()
                        page_part = a_list[-1]['href'].replace('pagego=' + fa_yuan_pages, '').encode('utf-8')
                        repeat_time = 0
                        for i in range(int(fa_yuan_pages)):
                            break_condition = repeat_time > max_repeat_time
                            if break_condition:
                                self.log_info('break_condition: repeat_time > ' + str(max_repeat_time))
                                break
                            url_page = host + page_part + 'pagego=' + str(i + 1)
                            new_url_page = self.get_right_url(url_page)
                            r_page = self.get(new_url_page)
                            r_page.encoding = 'utf-8'
                            res_inner = BeautifulSoup(r_page.text, 'html5lib')
                            ul = res_inner.findAll('ul', {'class': 'sswy_news'})
                            if ul:
                                lis = ul[0].findAll('li')
                                self.log_info(fa_yuan_str + url_page)
                                for li in lis:
                                    a = li.find('a')
                                    href = a['href'].strip()
                                    bh = href.split('=')[-2].replace(u'&isapp', '')
                                    title = a['title'].strip()
                                    kai_ting_shi_jian = re.findall(shi_jian_pattern, title)
                                    if kai_ting_shi_jian:
                                        kai_ting_shi_jian = kai_ting_shi_jian[0]
                                        gong_gao_nei_rong = title.replace(kai_ting_shi_jian, '')
                                        sql = "insert into jx_fz_fy VALUES('%s','%s','%s','%s','%s','%s')" % \
                                              (shi_qu, bh, fa_yuan, gong_gao_nei_rong, kai_ting_shi_jian, add_time)
                                        repeat_time = data_to_mysql(log_name, 0, sql, repeat_time)
                                    else:
                                        self.log_info(href + 'this page not found kai_ting_shi_jian')
                            else:
                                self.log_info(url_page + 'this page not found ul')
                    else:
                        self.log_info(fa_yuan_str + 'not found page turn a_list')
                else:
                    self.log_info(fa_yuan_str + 'not found page_div')
            else:
                res = BeautifulSoup(r.text, 'html5lib')
                ul = res.findAll('ul', {'class': 'sswy_news'})
                if ul:
                    lis = ul[0].findAll('li')
                    for li in lis:
                        a = li.find('a')
                        href = a['href'].strip()
                        if fa_yuan == u'广昌县人民法院':
                            bh = href.split('/')[-1].split('.')[0]
                            shi_jian_pattern = '\d.*\d'
                        else:
                            bh = href.split('=')[-2].replace(u'&isapp', '')
                        title = a['title'].strip()
                        kai_ting_shi_jian = re.findall(shi_jian_pattern, title)
                        if kai_ting_shi_jian:
                            kai_ting_shi_jian = kai_ting_shi_jian[0]
                            gong_gao_nei_rong = title.replace(kai_ting_shi_jian, '')
                            sql = "insert into jx_fz_fy VALUES('%s','%s','%s','%s','%s','%s')" % \
                                  (shi_qu, bh, fa_yuan, gong_gao_nei_rong, kai_ting_shi_jian, add_time)
                            # print bh, href, title
                            # print gong_gao_nei_rong
                            data_to_mysql(log_name, 0, sql)
                        else:
                            self.log_info(href + 'this page not found kai_ting_shi_jian')
                else:
                    self.log_info(url + 'this page not found ul')
        stop_time = time.strftime('%Y-%m-%d %H:%M:%S')
        end_sql = "update ktgg_job set stop_time = '" + stop_time + "',updatetime = '" + add_time + \
                  "',status = '1' where name = 'jx_fz_fy'"
        data_to_mysql(log_name, 1, end_sql)


if __name__ == '__main__':
    crawler = JiangXiFuZhouCrawler()
    crawler.run()
