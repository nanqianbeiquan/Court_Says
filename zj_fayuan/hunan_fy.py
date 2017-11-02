# coding=utf-8
import sys
import SpiderMan
from lxml import html
import re
import traceback
from mysql_db.UpdateStatus import *
from log_conf.LogConf import *
import logging
reload(sys)
sys.setdefaultencoding('utf8')

pinyin='hunan_fy'
order_nbr = '5fe6cf97-5592-11e7-be16-f45c89a63279'
requests = SpiderMan.SpiderMan(order_nbr, keep_session=True)

update_start_status(pinyin)

create_logfile(pinyin)

try:
    domain='http://hunanfy.chinacourt.org'
    for xx in range(1,2):
        url='http://hunanfy.chinacourt.org/article/index/id/M0jONTAwNzAwNCACAAA%3D/page/'+str(xx)+'.shtml'
        page_html=requests.get(url)
        code=page_html.status_code
        if not code==200:
            logging.error(url + ' ****http:状态码为：' + str(code) )
        tree=html.fromstring(page_html.text)
        table_li=tree.xpath('//div[@class="font14"]/ul/li')
        for one_li in table_li:
            gg_detail='';hytcy='';sjy='';fa_yuan=''
            gong_gao=one_li.xpath('span[1]//a/@title')[0]
            if  gong_gao.startswith(u'关于') or  gong_gao.endswith(u'开庭公告') or  gong_gao.endswith(u'一案'):
                back_url=one_li.xpath('span[1]//a/@href')[0]
                link_id = re.search(r'\d{6,}', back_url).group()
                whole_url=domain+back_url
                page_html=requests.get(whole_url)
                code=page_html.status_code
                if not code==200:
                    logging.error(url + ' ****http:状态码为：' + str(code) )
                tree=html.fromstring(page_html.text)
                try:
                    content=tree.xpath('//div[@class="detail_txt detail_general"]')[0]
                except Exception, e:
                    logging.error(url + ' 获取内容失败' )
                else:
                    content_p=content.xpath('p')
                    if len(content_p)>0:
                        print '情况1'
                        if len(content.xpath('p[@class="MsoNormal"]'))>0:
                            content_word=content.xpath('string(.)')
                            ss=content_word.replace(' ','').replace('\t','').replace(u'\u3000','').replace('\n\n','').replace('\r','').replace(u'\n','')
                            try:
                                gg_detail=re.findall(u'(本院.*?)合议庭',ss)[0]
                                hytcy=re.findall(u'合议庭成员：(.*?)书记员',ss)[0]
                                sjy=re.findall(u'书记员：(.*?)刑',ss)[0]
                                fa_yuan=re.findall(u'刑.{1}庭',ss)[0]
                            except:
                                gg_detail= ss
                        else:
                            for one_p in content_p:
                                try:
                                    try:
                                        word=one_p.xpath('text()')[0].replace(u'\xa0','').replace(u' ','')
                                    except:
                                        word=one_p.xpath('string(.)').replace(u'\xa0','').replace(u' ','')

                                    if re.search(u'(?:本院定于|我院定于)',word):
                                        gg_detail=word
                                    elif word.startswith(u'合议庭成员'):
                                        hytcy=word.split('：')[1]
                                    elif word.startswith(u'书记员') or word.startswith(u'代理书'):
                                        sjy=word.split('：')[1]
                                    elif word.startswith(u'刑'):
                                        fa_yuan=word
                                except:
                                    pass
                    else:
                        print '情况2'
                        content_word=content.xpath('string(.)').replace(' ','').replace('\t','')
                        ss1=content_word.split('\n\n')
                        ss=[a for a in ss1 if a.replace(' ','').replace('\n','').replace('\t','').replace(u'\u3000','')!='']
                        
                        gg_detail=ss[0].replace(' ','').replace('\n','').replace('\t','').replace(u'\u3000','')
                        hytcy=ss[1].replace(' ','').replace('\n','').replace('\t','').replace(u'\u3000','').split('：')[1]
                        try:
                            sjy=ss[2].replace(' ','').replace('\n','').replace('\t','').replace(u'\u3000','').split('：')[1]
                        except:
                            sjy=ss[2].replace(' ','').replace('\n','').replace('\t','').replace(u'\u3000','').split(':')[1]
                        try:
                            fa_yuan=ss[3].replace(' ','').replace('\n','').replace('\t','').replace(u'\u3000','')
                            if not fa_yuan.startswith(u'刑'):
                                raise Exception
                        except:
                            fa_yuan=tree.xpath('//div[@class="editor"]/text()')[0].split('：')[1]
                            if not fa_yuan.startswith(u'刑'):
                                fa_yuan=' '

                    if fa_yuan=='':
                        fa_yuan=tree.xpath('//div[@class="editor"]/text()')[0].split('：')[1]
                    if gg_detail==''and hytcy=='' and sjy==''and fa_yuan=='':
                        logging.error(whole_url+'页面解析失败 全为空字符'+'\n')
                        print whole_url+'页面解析失败'
                        raise Exception
                    sql="insert into hunan_fy values('%s','%s','%s','%s','%s','%s','%s')" %(gong_gao,\
                                                                            gg_detail,hytcy,sjy,fa_yuan,today,link_id)
                    select_sql="select * from hunan_fy where link_id='%s' and gong_gao='%s' " % (link_id,gong_gao )
                    has_result=MySQL_court.execute_query(select_sql)
                    if not has_result:
                        try:
                            MySQL_court.execute_update(sql)
                        except:
                            logging.error(sql)
                            logging.error(traceback.format_exc())
                        else:
                            logging.info(gong_gao)
            else:
                logging.error(gong_gao +'标题不符合，内容有可能有误 查看')


except Exception, e:
    logging.error(traceback.format_exc())
else:
    update_end_status(pinyin)
