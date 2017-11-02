# coding=utf-8
import PackageTool
import MySQL
from SpiderMan import SpiderMan
from bs4 import BeautifulSoup
import json
import re
import traceback
import TimeUtils


class GuangZhouCrawler(SpiderMan):
    log_name = u'广州开庭公告'

    fydm_dict = {
        '440100': u'广州市中级人民法院',
        '440103': u'广州市荔湾区人民法院',
        '440104': u'广州市越秀区人民法院',
        '440105': u'广州市海珠区人民法院',
        '440107': u'广州市天河区人民法院',
        '440108': u'广州市黄埔区人民法院',
        '440109': u'广州市白云区人民法院',
        '440111': u'广州市花都区人民法院',
        '440112': u'广州市从化区人民法院',
        '440113': u'广州市增城区人民法院',
        '440114': u'广州市番禺区人民法院',
        '440115': u'广州市南沙区人民法院',
        '440141': u'广州市萝岗区人民法院',
    }

    def __init__(self):
        super(GuangZhouCrawler, self).__init__(keep_session=False, max_try_times=5)

    def submit_search_request(self, fydm):
        page_idx = 1
        url = "http://www.gzcourt.gov.cn:8080/ywxt/bulletin/bulletin_1.jsp"
        while True:
            params = {
                'aymc': '',
                'cbrr': '',
                'court_jc': '',
                'dsrc': '',
                'fydm': fydm,
                'ktrqend': '',
                'ktrqstart': '',
                'no': '',
                'pageIndex': page_idx,
                'type1': '',
                'year': '',
            }
            # print url
            try:
                r = self.post(url, params=params)
                self.info(json.dumps({'page_idx': page_idx, 'fydm': fydm}))
                total_page_idx = int(re.search(u'共[\d]+页', r.text).group()[1:-1])
                soup = BeautifulSoup(r.text, 'lxml')
                case_list = soup.select('a.list_alink')
                for case in case_list:
                    # print '-'*100
                    # print case
                    td_list = case.select('tr > td')
                    ktrq = td_list[1].text.strip().replace("'", "\\'")
                    ah = td_list[2].text.strip().replace("'", "\\'")
                    ay = td_list[3].text.strip().replace("'", "\\'")
                    spz = td_list[4].text.strip().replace("'", "\\'")
                    ft = td_list[5].text.strip().replace("'", "\\'")
                    fy = self.fydm_dict[fydm]
                    sql = "select * from court_notice.guang_zhou where an_hao='%s' and fa_yuan='%s'" % (ah, fy)
                    res = MySQL.execute_query(sql)
                    xq = None
                    if len(res) == 0:
                        detail_url = 'http://www.gzcourt.gov.cn:8080/ywxt/bulletin/iframe_detail.jsp?' \
                                     + case.attrs['href'].split('?')[-1]
                        # print self.get(detail_url).text
                        for i in range(3):
                            try:
                                r2 = self.get(detail_url)
                                xq = BeautifulSoup(r2.text, 'html5lib').select('table')[0].text.replace(
                                    u'公　　告', '').strip().replace("'", "\\'")
                                break
                            except Exception, e:
                                traceback.print_exc(e)
                        if not xq:
                            continue
                        sql = "insert into court_notice.guang_zhou" \
                              "(kai_ting_ri_qi,an_hao,an_you,shen_pan_zhang,fa_ting,fa_yuan," \
                              "xq,add_date,last_update_time) " \
                              "values('%s','%s','%s','%s','%s','%s','%s',date(now()),now()) " % (
                                  ktrq, ah, ay, spz, ft, fy, xq)
                        MySQL.execute_update(sql)
                if page_idx >= total_page_idx:
                    break
                else:
                    page_idx += 1
            except Exception, e:
                traceback.print_exc(e)
                continue
                # print r.text

    def run(self):
        start_time = TimeUtils.get_cur_time()
        start_sql = "update ktgg_job set start_time='" + start_time + "', status = '0' where name = 'guang_zhou'"
        MySQL.data_to_mysql(start_sql)
        for fydm in self.fydm_dict:
            self.info(u'开始抓取' + self.fydm_dict[fydm] + u'...')
            self.submit_search_request(fydm)
            self.info(self.fydm_dict[fydm] + u' 抓取完毕！')
        self.info(u'抓取完毕！')
        stop_time = TimeUtils.get_cur_time()
        updatetime = TimeUtils.get_today()
        end_sql = "update ktgg_job set stop_time = '" + stop_time + "',updatetime = '" + updatetime + \
                  "',status = '1' where name = 'guang_zhou'"
        MySQL.data_to_mysql(end_sql)


if __name__ == '__main__':
    crawler = GuangZhouCrawler()
    # crawler.submit_search_request('440107')
    crawler.run()
