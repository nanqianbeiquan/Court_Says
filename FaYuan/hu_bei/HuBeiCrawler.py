# coding=utf-8

import PackageTool
from bs4 import BeautifulSoup
from SpiderMan import SpiderMan, get_param_value
import MySQL
import TimeUtils
import re
import json
import traceback
import os
from codecs import open


class HuBeiCrawler(SpiderMan):
    log_name = u'湖北开庭公告'

    fy_dict = None

    def __init__(self):
        super(HuBeiCrawler, self).__init__(keep_session=False)
        start_time = TimeUtils.get_cur_time()
        start_sql = "update ktgg_job set start_time='" + start_time + "', status = '0' where name = 'hu_bei'"
        MySQL.data_to_mysql(start_sql)
        self.load_court_info()

    def submit_search_request(self, fy_id):

        fy = self.fy_dict[fy_id]
        page_no = 1
        curr_channel_id = None
        site_id = None
        while True:
            self.info(json.dumps({'fy_id': fy_id, 'page_no': page_no}))
            try:
                if page_no == 1:
                    url = "http://www.hbfy.org/gfcms/site/court/%s/ggxxkt/index.html" % fy_id
                    r = self.get(url)
                    r.encoding = 'utf-8'
                    soup = BeautifulSoup(r.text, 'lxml')
                    query_info = soup.select('form#overtbeginPage')[0].attrs['action']
                    site_id = get_param_value(query_info, 'siteid')
                    curr_channel_id = get_param_value(query_info, 'currChannelid')
                    # return
                else:
                    url = "http://www.hbfy.org/gfcms/templetPro.do?templetPath=overtbegin/overtbeginPage.html"
                    params = {
                        'currChannelid': curr_channel_id,
                        'currUnitId': fy_id,
                        'dsr': '',
                        'page': page_no,
                        'pageNum': page_no - 1,
                        'siteid': site_id
                    }
                    r = self.post(url, params=params)
                    soup = BeautifulSoup(r.text, 'lxml')
                    # print r.text
                # print r.text

                tr_list = soup.select('table.zebra > tr')
                for tr in tr_list:
                    td_list = tr.select('td')
                    detail_url = 'http://www.hbfy.org' + td_list[0].select('a')[0].attrs['href']
                    ft = td_list[0].text.strip()
                    ktrq = td_list[1].text.strip()
                    dsr = td_list[2].text.strip().replace("'", "\\'")
                    ay = td_list[3].text.strip()
                    sql = "select add_date from court_notice.hu_bei where url='%s'" % detail_url
                    res = MySQL.execute_query(sql)
                    if len(res) == 0:
                        self.info(detail_url + '[new]')
                        sql = "insert into court_notice.hu_bei" \
                              "(url,fa_yuan,fa_ting,kai_ting_ri_qi,dang_shi_ren,an_you,add_date,last_update_time)" \
                              " values('%s','%s','%s','%s','%s','%s',date(now()),now())" % \
                              (detail_url, fy, ft, ktrq, dsr, ay)
                        MySQL.execute_update(sql)
                    else:
                        self.info(detail_url)
                total_page_no = int(
                    re.search(u'[\d]+', re.search(u'共&nbsp;<b>[\d]+</b>&nbsp;页', r.text).group()).group())
                if page_no >= total_page_no:
                    break
                else:
                    page_no += 1
            except Exception, e:
                traceback.print_exc(e)
                continue

    def load_court_info(self):
        save_path = os.path.join(os.path.dirname(__file__), 'fy_dict.json')
        try:
            self.info(u'加载法院数据')
            self.fy_dict = {}
            url = "http://www.hbfy.org/gfcms/web/unit/allUnit.do"
            self.info('load court info: ' + url)
            r = self.get(url)
            soup = BeautifulSoup(r.text, 'lxml')

            court_list = soup.select('a[href]')
            for court in court_list:
                id_name = court.attrs['href'][len("javascript:closeME('"):-len("')")].split("','")
                self.fy_dict[id_name[0]] = id_name[1]

            area_list = soup.select('area[shape]')
            for area in area_list:
                area_page = area.attrs['href']
                url2 = 'http://www.hbfy.org' + area_page
                self.info('load court info: ' + url2)
                r2 = self.get(url2)
                soup2 = BeautifulSoup(r2.text, 'lxml')

                court_list2 = soup2.select('a[href]')
                for court in court_list2:
                    id_name = court.attrs['href'][len("javascript:closeME('"):-len("')")].split("','")
                    self.fy_dict[id_name[0]] = id_name[1]
            with open(save_path, 'w', encoding='utf-8') as f:
                json.dump(self.fy_dict, f, ensure_ascii=False)
                f.close()
        except Exception, e:
            self.info(traceback.format_exc(e))
            self.info(u'法院信息加载失败，从历史数据中读取')
            self.fy_dict = json.load(open(save_path, 'r', encoding='utf-8'))

            # for fy in self.fy_dict:
            #     print fy, self.fy_dict[fy]

    def run(self):
        for fy_id in self.fy_dict:
            self.info('[' + self.fy_dict[fy_id] + ']')
            self.submit_search_request(fy_id)
        stop_time = TimeUtils.get_cur_time()
        updatetime = TimeUtils.get_today()
        end_sql = "update ktgg_job set stop_time = '" + stop_time + "',updatetime = '" + updatetime + \
                  "',status = '1' where name = 'hu_bei'"
        MySQL.data_to_mysql(end_sql)


if __name__ == "__main__":
    crawler = HuBeiCrawler()
    crawler.run()
    # crawler.submit_search_request('HC0')
    # crawler.load_court_info()
    # for fy_id in crawler.fy_dict:
    #     print fy_id, crawler.fy_dict[fy_id]
