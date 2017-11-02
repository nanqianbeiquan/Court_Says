# coding=utf-8
import sys
import SpiderMan
from lxml import html
import re
from mysql_db.UpdateStatus import *
from log_conf.LogConf import *
import logging
import traceback
reload(sys)
sys.setdefaultencoding('utf8')
order_nbr = '5fe6cf97-5592-11e7-be16-f45c89a63279'
requests = SpiderMan.SpiderMan(order_nbr, keep_session=True)
url='http://www.yfzy.gov.cn:8080/icourt/pri/yfzy/ktgg/ktgg.jsp?fjm=JN0'
shi_qu=u'云浮市'
pinyin='gd_yunfu'

update_start_status(pinyin)



import multiprocessing as mp
lock=mp.Lock()
def get_pageno():
    page_html=requests.get(url)
    code=page_html.status_code
    if not code==200:
        logging.error(url + ' ****http:状态码为：' + str(code) )
        return 'bad'
    tree=html.fromstring(page_html.text)
    table_tr=tree.xpath('//table[@class="font10_black"]/tr')[1:]
    pageno=tree.xpath('//select[@class="form1"]/option[last()]/@value')[0]
    return pageno

def get_content(x):

    data={
        'pageIndex':str(x)
    }

    page_html=requests.post(url,data=data)
    tree=html.fromstring(page_html.text)
    table_tr=tree.xpath('//table[@class="font10_black"]/tr')[1:]

    for one_tr in table_tr:
        kt_date=one_tr.xpath('td[2]/text()')[0]
        print kt_date
        kt_time=one_tr.xpath('td[3]/text()')[0]
        an_hao=one_tr.xpath('td[4]/div/a/text()')[0]
        fa_yuan=one_tr.xpath('td[5]/text()')[0]
        open_detail=re.findall("'(.*?)'",one_tr.xpath('td[4]/div/a/@onclick')[0])
        xh= open_detail[0];ahdm=open_detail[-1]
        turn_url='http://www.yfzy.gov.cn:8080/icourt/pri/yfzy/ktgg/ktgg_detail.jsp?xh='+xh+'&ahdm='+ahdm
        turn_page_html=requests.get(turn_url)
        turn_tree=html.fromstring(turn_page_html.text)
        all_inform=turn_tree.xpath('//table/tr')
        for one_inform in all_inform:
            if len(one_inform.xpath('td'))==2:
                gg_word=one_inform.xpath('string(.)')

                one_inform_word= gg_word.replace(' ','').replace('\r\n','').replace(u'\xa0','')

                try:
                    inform=one_inform_word.split(u'：')
                    inform_name=inform[0]
                    inform_detail=inform[1]
                except Exception,e:
                    logging.error( '云浮市公告详情分隔出现问题'+turn_url+str(e))
                else:
                    if inform_name==u'案由':
                        an_you=inform_detail
                    elif inform_name==u'当事人':
                        dsr=inform_detail
                    elif inform_name==u'主审法官':
                        zsfg=inform_detail
                    elif inform_name==u'书记员':
                        sjy=inform_detail
                    elif inform_name==u'适用程序':
                        sycx=inform_detail
                    else:
                        pass
        select_sql="select * from gd_yunfu where an_hao='%s' and kt_date='%s' " % (an_hao,kt_date)
        has_result=MySQL_court.execute_query(select_sql)
        if not has_result:
            try:
                sql="insert into gd_yunfu values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" %(an_hao,\
                                                                kt_date,kt_time,fa_yuan,an_you,dsr,zsfg,sjy,sycx,today,shi_qu)
                MySQL_court.execute_update(sql)
            except:
                logging.error(sql+'\n')
                logging.error(traceback.format_exc()+'\n')
            else:
                logging.info(kt_date+kt_time+an_hao+fa_yuan+an_you+dsr+zsfg+sjy+sycx+'\n')
                print '----------------------------------------------'
                print '开庭日期：'+kt_date
                print '开庭时间：'+kt_time
                print '案号：'+an_hao
                print '法院：'+fa_yuan
                print '案由：'+an_you
                print '当事人：'+dsr
                print '主审法官：'+zsfg
                print '书记员：'+sjy
                print '适用程序：'+sycx
if __name__ == '__main__':
    create_logfile(pinyin)

    p=mp.Pool(processes=4)
    try:
        pageno=int(get_pageno())
    except:
        logging.error('get total page ------->bad')
        logging.error(traceback.format_exc()+'\n')
    else:
        try:
            for i in range(1,pageno+1):
                 p.map_async(get_content,(i,))
            p.close()
            p.join()
        except:
            logging.error(traceback.format_exc())
        else:
            update_end_status(pinyin)





