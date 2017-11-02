# coding=utf-8

import PackageTool
from bs4 import BeautifulSoup
from SpiderMan import SpiderMan
import TimeUtils
import MySQL
import re
import json
import traceback
import os


class JiangXiCrawler(SpiderMan):
    log_name = u'江西开庭公告'
    # log_name = 'jx_ktgg'
    fy_dict = None

    def __init__(self):
        super(JiangXiCrawler, self).__init__(keep_session=False)
        start_time = TimeUtils.get_cur_time()
        start_sql = "update ktgg_job set start_time='" + start_time + "', status = '0' where name = 'jiang_xi'"
        MySQL.data_to_mysql(start_sql)
        self.load_fy_dict()

    def load_fy_dict(self):
        save_path = os.path.join(os.path.dirname(__file__), 'jxfy.json')
        self.info(u'加载法院信息。。。')
        try:
            self.fy_dict = {}
            fy_url_list = [
                'http://www.jxfy.gov.cn/web/root/js/loadliti.js',  # 江西
                'http://www.nccourt.gov.cn/web/ncfy/js/loadliti.js',  # 南昌
                'http://www.jxfy.gov.cn/web/jjfy/js/loadliti.js',  # 九江
                # '',  # 景德镇
                'http://www.jxfy.gov.cn/web/zhushan/js/loadliti.js',  # 景德镇下的珠山区
                'http://www.pxfygk.gov.cn/web/pxfy/js/loadliti.js',  # 萍乡
                'http://www.jxfy.gov.cn/web/xyzy/js/loadliti.js',  # 新余
                'http://www.jxfy.gov.cn/web/yingtan/js/loadliti.js',  # 鹰潭
                'http://www.jxfy.gov.cn/web/gzfy/js/loadliti.js',  # 赣州
                'http://www.ycfysf.gov.cn/web/ycfy/js/loadliti.js',  # 宜春
                'http://www.sfgk.gov.cn/web/srfy/js/loadliti.js',  # 上饶
                'http://www.jfsfw.gov.cn/web/jafy/js/loadliti.js',  # 吉安
                # # '',  # 抚州
                'http://www.jxfy.gov.cn/web/ntzy/js/loadliti.js',  # 南铁
            ]
            for url in fy_url_list:
                self.info(url)
                host = url.split('/web/')[0]
                r = self.get(url)
                if url == 'http://www.jxfy.gov.cn/web/zhushan/js/loadliti.js':
                    self.fy_dict["CF8831B38EC842CBA613FF758478CD0D"] = host
                else:
                    tmp_dict = json.loads(re.search(u'enumORG: [^\}]+}', r.text).group()[len('enumORG:'):])
                    for fy_id in tmp_dict.values():
                        self.fy_dict[fy_id] = host
            if "20111229101704767016000000000000" in self.fy_dict:
                self.fy_dict.pop("20111229101704767016000000000000")
            self.info(u'法院信息加载成功，更新配置文件')
            with open(save_path, 'w') as f:
                json.dump(self.fy_dict, f)
                f.close()
        except Exception, e:
            traceback.print_exc(e)
            self.info(u'法院信息加载失败，从配置文件读取')
            self.fy_dict = json.load(open(save_path))
            print self.fy_dict
            # print self.fy_dict
            # print self.fy_set

    def submit_search_request(self, fy_id):
        page_no = 1
        while True:
            try:
                self.info(json.dumps({'fy_id': fy_id, 'page_no': page_no}))
                url = "%s/api.do?method=" \
                      "http://sf.dolawing.com/liti/TrialOpenCourtNotice/trialopencourtnotice!getAnnouncementAjaxp.action" % \
                      self.fy_dict[fy_id]
                params = {
                    '_t': TimeUtils.get_cur_ts_mil(),
                    'page.order': 'asc,asc',
                    'page.orderBy': 'openCourtDate,id',
                    'page.pageNo': page_no,
                    'page.pageSize': 20,
                    'upCourtId': fy_id
                }
                # print url, params
                r = self.post(url=url, data=params, headers={
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:45.0) Gecko/20100101 Firefox/45.0',
                    # 'Host': 'www.nccourt.gov.cn',
                    'Referer': 'http://www.nccourt.gov.cn/web/ncfy/pjude/ktgg.jsp',
                })
                # print r.text
                data = json.loads(r.text)
                for res in data['message'].get('result', []):
                    case_id = res['id']
                    fy = res.get('courtName', '')
                    ah = res.get('caseNo', '')
                    ay = res.get('cause', '')
                    ft = res.get('openCourtAddr', '')
                    dsr = res.get('plaintiff', '').replace("'", "\\'")
                    cbr = res.get('undertaker', '')
                    ktsj = res.get('openCourtDateString', '')

                    sql = "select add_date from court_notice.jiang_xi where id='%s'" % case_id
                    res = MySQL.execute_query(sql)
                    if len(res) == 0:
                        self.info(case_id + '[new]')
                        sql = "insert into court_notice.jiang_xi(id,fa_yuan,an_hao,an_you,fa_ting,dang_shi_ren," \
                              "cheng_ban_ren,kai_ting_ri_qi,add_date,last_update_time) " \
                              "values('%s','%s','%s','%s','%s','%s','%s','%s',date(now()),now())" \
                              % (case_id, fy, ah, ay, ft, dsr, cbr, ktsj)
                        MySQL.execute_update(sql)
                    else:
                        self.info(case_id)
                total_pages = data['message']['totalPages']
                self.info('%d/%d' % (page_no, total_pages))
                if data['message']['hasNext']:
                    page_no += 1
                else:
                    break
            except Exception, e:
                traceback.print_exc(e)
                continue

    def run(self):
        i = 0
        for fy_id in self.fy_dict:
            i += 1
            self.info('-' * 10 + fy_id + ' [%d/%d]' % (i, len(self.fy_dict)) + '-' * 10)
            self.submit_search_request(fy_id=fy_id)
        stop_time = TimeUtils.get_cur_time()
        updatetime = TimeUtils.get_today()
        end_sql = "update ktgg_job set stop_time = '" + stop_time + "',updatetime = '" + updatetime + \
                  "',status = '1' where name = 'jiang_xi'"
        MySQL.data_to_mysql(end_sql)


if __name__ == '__main__':
    crawler = JiangXiCrawler()
    # crawler.load_fy_dict()

    crawler.run()
    # crawler.submit_search_request('1FE8F9CA8DEB454DA3D81E3FD0B58F10')
