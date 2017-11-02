# coding=utf-8
import os
import sys
import time
from bs4 import BeautifulSoup
import requests
import re

from SpiderMan import SpiderMan
from Mysql_Config_Fyh import data_to_mysql
from Mysql_Config_Fyh import logger


class JiangSuWuXiCrawler(SpiderMan):
    def __init__(self):
        super(JiangSuWuXiCrawler, self).__init__(keep_session=False)

    def log_info(self, message):
        self
        log_name = 'js_wx_fy.log'
        logger(log_name, message)

    def run(self):
        today = time.strftime('%Y-%m-%d')
        updatetime = today
        shi_jian_pattern = r'\d{4}-\d{2}-\d{2}.*?\d{2}:\d{2}'
        log_name = 'js_wx_fy.log'
        start_time = time.strftime('%Y-%m-%d %H:%M:%S')
        start_sql = "update ktgg_job set start_time='" + start_time + "', status = '0' where name = 'wxfy'"
        data_to_mysql(log_name, 1, start_sql)
        shi_qu = u'无锡市'
        repeat_time = 0
        max_repeat_time = 300
        for p in range(1, 2):
            url = 'http://wxzy.chinacourt.org/public/more.php?p=' + str(p) + '&LocationID=1001000000&sub='
            host = 'http://wxzy.chinacourt.org'
            r = self.get(url)
            r.encoding = 'gb2312'
            rbs = BeautifulSoup(r.text, 'html5lib')
            td = rbs.findAll('td', {'class': 'xihei_141'})
            if td:
                link_list = td[0].findAll('a')
                new_link_list = link_list[:-2]
                self.log_info('link_list: ' + str(len(new_link_list)))
                for i in range(0, len(new_link_list)):
                    break_condition = repeat_time > max_repeat_time
                    if break_condition:
                        self.log_info('break_condition: repeat_time > ' + str(max_repeat_time))
                        break
                    linp = new_link_list[i]['href']
                    link = host + linp
                    # print i ,link_list[i],link
                    # link = 'http://wxzy.chinacourt.org/public/detail.php?id=6464'
                    bt = self.get(link)
                    btbs = BeautifulSoup(bt.text, 'html5lib')
                    # print btbs
                    span = btbs.findAll('span', {'class': 'detail_content'})
                    if span:
                        # print span[0]
                        # os._exit(1)
                        span_str = span[0].encode('utf-8')
                        p = span[0].find('p')
                        p_str = p.encode('utf-8')
                        chip_list = p_str.split('<br/>')
                        if len(chip_list) < 7:
                            chip_list = span_str.split('</p><p></p><p>')
                        if len(chip_list) < 7:
                            chip_list = span_str.split('</p><p>')
                        if len(chip_list) > 7:
                            temp_chip = []
                            for c in range(len(chip_list)):
                                if '</p><p>' in chip_list[c]:
                                    for temp_temp_chip in chip_list[c].split('</p><p>'):
                                        if temp_temp_chip.strip():
                                            temp_chip.append(temp_temp_chip)
                                elif '<p>' in chip_list[c]:
                                    for temp_temp_chip in chip_list[c].split('<p>'):
                                        if temp_temp_chip.strip() and temp_temp_chip != '<span class="detail_content">':
                                            temp_chip.append(temp_temp_chip)
                                else:
                                    if '本信息获取时间' in chip_list[c] or '页次' in chip_list[c]:
                                        continue
                                    elif chip_list[c].strip():
                                        temp_chip.append(chip_list[c])
                            if len(temp_chip) % 7 == 0:
                                new_chip_list = temp_chip
                            else:
                                new_chip_list = temp_chip[: -(len(temp_chip) % 7)]
                            data_num = int(len(new_chip_list) / 7)
                            self.log_info(str(i + 1) + ',data_num_1,' + str(data_num))
                            for j in range(data_num):
                                shi_jian = re.findall(shi_jian_pattern, new_chip_list[j * 7])
                                if shi_jian:
                                    shi_jian = shi_jian[0]
                                else:
                                    self.log_info('shi_jian match wrong: ' + str(j + 1) +
                                                  ',' + link + new_chip_list[j * 7])
                                    continue
                                an_hao = new_chip_list[j * 7 + 1].replace('案号：', '').strip()
                                an_jian_ming_cheng = new_chip_list[j * 7 + 2].replace('案件名称：', '').strip()
                                fa_ting = new_chip_list[j * 7 + 3].replace('审判法庭：', '').strip()
                                shen_pan_zhang = new_chip_list[j * 7 + 4].replace('审判长：', '').strip()
                                he_yi_ting = new_chip_list[j * 7 + 5].replace('合议庭成员：', '').strip()
                                shu_ji_yuan = new_chip_list[j * 7 + 6].replace('书记员：', '').strip()
                                sql = "insert into wxfy VALUES('%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (
                                    shi_qu.encode('utf8'), an_hao, an_jian_ming_cheng, shi_jian, fa_ting, shen_pan_zhang, he_yi_ting,
                                    shu_ji_yuan, today)
                                repeat_time = data_to_mysql(log_name, 0, sql, repeat_time, link)
                        elif len(chip_list) < 7:
                            chip_list = span[0].findAll('div')
                            if len(chip_list) > 10:
                                shi_jian_div = chip_list[::2]
                                other_div = chip_list[1::2]
                                self.log_info(str(i + 1) + ',len(shi_jian_div): ' + str(len(shi_jian_div)))
                                for j in range(len(shi_jian_div)):
                                    shi_jian = re.findall(shi_jian_pattern, shi_jian_div[j].text.encode('utf-8'))
                                    if shi_jian:
                                        shi_jian = shi_jian[0].decode('utf-8')
                                    else:
                                        self.log_info('div condition shi_jian match wrong: ' + str(j + 1) +
                                                      link + shi_jian_div[j])
                                        continue
                                    p_list = other_div[j].findAll('p')
                                    an_hao = p_list[0].text.replace(u'案号：', '').strip()
                                    an_jian_ming_cheng = p_list[1].text.replace(u'案件名称：', '').strip()
                                    fa_ting = p_list[2].text.replace(u'审判法庭：', '').strip()
                                    shen_pan_zhang = p_list[3].text.replace(u'审判长：', '').strip()
                                    he_yi_ting = p_list[4].text.replace(u'合议庭成员：', '').strip()
                                    shu_ji_yuan = p_list[5].text.replace(u'书记员：', '').strip()
                                    sql = "insert into wxfy VALUES('%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (
                                        shi_qu, an_hao, an_jian_ming_cheng, shi_jian, fa_ting, shen_pan_zhang,
                                        he_yi_ting, shu_ji_yuan, today)
                                    repeat_time = data_to_mysql(log_name, 0, sql, repeat_time, link)
                                    # print other_div[j], shi_jian_div[j]
                                    # print shi_jian, an_hao, an_jian_ming_cheng, fa_ting, shen_pan_zhang, he_yi_ting, shu_ji_yuan
                                    # os._exit(1)
                            else:
                                chip_list = span[0].findAll('p')
                                if len(chip_list) > 25:
                                    temp_chip = []
                                    temp_c = []
                                    for c in range(len(chip_list)):
                                        if u'开庭公告' in chip_list[c].text.strip():
                                            continue
                                        elif chip_list[c].text.strip() == u'案号：(2016)苏02民终' \
                                                or chip_list[c].text.strip() == u'案号：(':
                                            temp_chip.append(chip_list[c].text.strip() + chip_list[c + 1].text.strip())
                                            temp_c.append(c + 1)
                                        elif chip_list[c].text.strip() and c not in temp_c:
                                            temp_chip.append(chip_list[c])
                                    if len(temp_chip) % 7 == 0:
                                        new_chip_list = temp_chip
                                    else:
                                        new_chip_list = temp_chip[: -(len(temp_chip) % 7)]
                                    data_num = int(len(new_chip_list) / 7)
                                    self.log_info(str(i + 1) + 'data_num_2,' + str(data_num))
                                    for j in range(data_num):
                                        shi_jian = new_chip_list[j * 7].text.strip()
                                        if type(new_chip_list[j * 7 + 1]) == unicode:
                                            an_hao = new_chip_list[j * 7 + 1].replace(u'案号：', '').strip()
                                        else:
                                            an_hao = new_chip_list[j * 7 + 1].text.replace(u'案号：', '').strip()
                                        an_jian_ming_cheng = new_chip_list[j * 7 + 2].text.replace(u'案件名称：', '').strip()
                                        fa_ting = new_chip_list[j * 7 + 3].text.replace(u'审判法庭：', '').strip()
                                        shen_pan_zhang = new_chip_list[j * 7 + 4].text.replace(u'审判长：', '').strip()
                                        he_yi_ting = new_chip_list[j * 7 + 5].text.replace(u'合议庭成员：', '').strip()
                                        shu_ji_yuan = new_chip_list[j * 7 + 6].text.replace(u'书记员：', '').strip()
                                        sql = "insert into wxfy VALUES('%s','%s','%s','%s','%s','%s','%s','%s','%s')" \
                                              % (shi_qu, an_hao, an_jian_ming_cheng, shi_jian, fa_ting,
                                                 shen_pan_zhang, he_yi_ting, shu_ji_yuan, today)
                                        repeat_time = data_to_mysql(log_name, 0, sql, repeat_time, link)
                                else:
                                    self.log_info('second condition chip_l ist get exception: ' + link)
                        else:
                            self.log_info('chip_list get exception: ' + link)
                    else:
                        self.log_info('this page has no span: ' + link)
            else:
                self.log_info('this page has no td table: ' + url)
        stop_time = time.strftime('%Y-%m-%d %H:%M:%S')
        end_sql = "update ktgg_job set stop_time = '" + stop_time + "',updatetime = '" + updatetime + \
                  "',status = '1' where name = 'wxfy'"
        data_to_mysql(log_name, 1, end_sql)


if __name__ == '__main__':
    crawler = JiangSuWuXiCrawler()
    crawler.run()
