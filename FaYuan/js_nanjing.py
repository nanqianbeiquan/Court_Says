# coding=utf-8
import datetime
import sys

import requests
from bs4 import BeautifulSoup

from ShuiWu import MSSQL

print datetime.datetime.now().strftime('%Y-%m-%d')
# print str(datetime.datetime.now())[0:10]
reload(sys)
sys.setdefaultencoding('utf8')
updatetime = datetime.datetime.now().strftime('%Y-%m-%d')

MSSQL.execute_start('js_nanjing')
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'Connection': 'keep-alive',
    'Host': 'www.njfy.gov.cn',
    'Referer': 'http://www.njfy.gov.cn/www/njfy/fygg.htm',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0',
}
for s in range(1, 3):
    # 	url = "http://www.njfy.gov.cn/www/njfy/lcgkKtgg.jsp?pageNo=s"
    url = "http://www.njfy.gov.cn/www/njfy/lcgkKtgg.jsp?pageNo=" + str(s)
    r = requests.get(url, headers=headers)
    # 	r.encoding = 'gb2312'
    soup = BeautifulSoup(r.text, 'html5lib')
    td_list = soup.find_all("td", align="center")
    for i in range(1, (len(td_list) + 7) / 7 - 1):
        fa_yuan = td_list[7 * i + 1].text.strip()
        ri_qi = td_list[7 * i + 2].text
        an_hao = td_list[7 * i + 3].text.strip()
        an_you = td_list[7 * i + 4].text.strip()
        # print type(an_you)
        zhu_shen = td_list[7 * i + 5].text.strip()
        dang_shi_ren = td_list[7 * i + 6].text.strip()
        shi_qu = '南京市'
        # 		print i,fa_yuan,ri_qi,an_hao,an_you,zhu_shen,dang_shi_ren
        sql = "INSERT INTO js_nanjing VALUES('%s','%s','%s','%s','%s','%s','%s','%s')" % (
        fa_yuan, ri_qi, an_hao, an_you, zhu_shen, dang_shi_ren, updatetime, shi_qu)
        # print s, sql.encode('gbk', 'ignore') + ";"
        print s, sql.replace(u'\ufffd', '') + ";"
        MSSQL.execute_insert(sql)
MSSQL.execute_sop('js_nanjing')
