#coding=utf-8
import os
import sys
import requests
import time
from bs4 import BeautifulSoup
import datetime
import MySQLdb
import threading
import re
from selenium import webdriver

reload(sys)
sys.setdefaultencoding('utf8')

today = datetime.datetime.now().strftime('%Y-%m-%d')
print 'today:',today
# lsh=115400001086500
# xh=1
ss = """<tr><td> <marquee direction="up" height="135" scrollamount="1" onMouseOut="this.start();" onMouseOver
="this.stop();"><table border="0" width="100%"><tr height="150" ><td valign="top" style="cursor: pointer
;" onclick="doView('115100001180496','2')" ><table width="90%" border="0" height="90%" bgcolor="#EBEBEB"
><tr align="center"  height="20"><td style="font-size:13px;">开庭公告</td></tr><tr align="center" valign
="top" ><td align="left" ><p style="font-size:13px;margin:0px;">2017年 04月 28日&nbsp;&nbsp;09:15-11:30
第二十二法庭公开审理&nbsp;&nbsp;(2014)宁商外初字第00020号&nbsp;&nbsp;一案</p></td></tr></table></td><td valign="top" style
="cursor: pointer;" onclick="doView('115100001435463','1')" ><table width="90%" border="0" height="90
%" bgcolor="#EBEBEB"><tr align="center"  height="20"><td style="font-size:13px;">开庭公告</td></tr><tr align
="center" valign="top" ><td align="left" ><p style="font-size:13px;margin:0px;">2017年 05月 10日&nbsp;&nbsp
;11:30-12:00第二十二法庭公开审理&nbsp;&nbsp;(2015)宁商外初字第00010号&nbsp;&nbsp;一案</p></td></tr></table></td><td valign
="top" style="cursor: pointer;" onclick="doView('115100001435464','1')" ><table width="90%" border="0"
 height="90%" bgcolor="#EBEBEB"><tr align="center"  height="20"><td style="font-size:13px;">开庭公告</td
></tr><tr align="center" valign="top" ><td align="left" ><p style="font-size:13px;margin:0px;">2017年
 05月 10日&nbsp;&nbsp;09:30-11:30第二十二法庭公开审理&nbsp;&nbsp;(2015)宁商外初字第00011号&nbsp;&nbsp;一案</p></td></tr><
/table></td><td valign="top" style="cursor: pointer;" onclick="doView('115100001448586','1')" ><table
 width="90%" border="0" height="90%" bgcolor="#EBEBEB"><tr align="center"  height="20"><td style="font-size
:13px;">开庭公告</td></tr><tr align="center" valign="top" ><td align="left" ><p style="font-size:13px;margin
:0px;">2017年 02月 14日&nbsp;&nbsp;09:30-11:00第二十二法庭公开审理&nbsp;&nbsp;(2015)宁商外初字第00079号&nbsp;&nbsp;一案</p
></td></tr></table></td></tr><tr height="150" ><td valign="top" style="cursor: pointer;" onclick="doView
('115200001133646','1')" ><table width="90%" border="0" height="90%" bgcolor="#EBEBEB"><tr align="center"
  height="20"><td style="font-size:13px;">开庭公告</td></tr><tr align="center" valign="top" ><td align="left"
 ><p style="font-size:13px;margin:0px;">2016年 11月 04日&nbsp;&nbsp;14:30-17:00锁九法庭公开审理&nbsp;&nbsp;(2015
)玄民初字第02317号&nbsp;&nbsp;一案</p></td></tr></table></td><td valign="top" style="cursor: pointer;" onclick
="doView('115400001086500','1')" ><table width="90%" border="0" height="90%" bgcolor="#EBEBEB"><tr align
="center"  height="20"><td style="font-size:13px;">开庭公告</td></tr><tr align="center" valign="top" ><td
 align="left" ><p style="font-size:13px;margin:0px;">2016年 06月 20日&nbsp;&nbsp;09:30-11:00第七法庭(白)公开审理
&nbsp;&nbsp;(2015)秦民特字第00039号&nbsp;&nbsp;一案</p></td></tr></table></td><td valign="top" style="cursor
: pointer;" onclick="doView('115400001086805','1')" ><table width="90%" border="0" height="90%" bgcolor
="#EBEBEB"><tr align="center"  height="20"><td style="font-size:13px;">开庭公告</td></tr><tr align="center"
 valign="top" ><td align="left" ><p style="font-size:13px;margin:0px;">2016年 10月 26日&nbsp;&nbsp;09:30-12
:00第十一法庭(白)公开审理&nbsp;&nbsp;(2015)秦民初字第03470号&nbsp;&nbsp;一案</p></td></tr></table></td><td valign="top"
 style="cursor: pointer;" onclick="doView('115400001087377','1')" ><table width="90%" border="0" height
="90%" bgcolor="#EBEBEB"><tr align="center"  height="20"><td style="font-size:13px;">开庭公告</td></tr><tr
 align="center" valign="top" ><td align="left" ><p style="font-size:13px;margin:0px;">2016年 07月 11日&nbsp
;&nbsp;09:30-11:00第七法庭(白)公开审理&nbsp;&nbsp;(2015)秦民特字第00043号&nbsp;&nbsp;一案</p></td></tr></table></td><
/tr><tr height="150" ><td valign="top" style="cursor: pointer;" onclick="doView('115600001152306','1'
)" ><table width="90%" border="0" height="90%" bgcolor="#EBEBEB"><tr align="center"  height="20"><td
 style="font-size:13px;">开庭公告</td></tr><tr align="center" valign="top" ><td align="left" ><p style="font-size
:13px;margin:0px;">2016年 10月 27日&nbsp;&nbsp;09:10-10:00第七法庭公开审理&nbsp;&nbsp;(2015)鼓民特字第00096号&nbsp;&nbsp
;一案</p></td></tr></table></td><td valign="top" style="cursor: pointer;" onclick="doView('115800001109229'
,'1')" ><table width="90%" border="0" height="90%" bgcolor="#EBEBEB"><tr align="center"  height="20"
><td style="font-size:13px;">开庭公告</td></tr><tr align="center" valign="top" ><td align="left" ><p style
="font-size:13px;margin:0px;">2017年 01月 13日&nbsp;&nbsp;14:30-15:30第七法庭公开审理&nbsp;&nbsp;(2015)浦民初字第03498
号&nbsp;&nbsp;一案</p></td></tr></table></td><td valign="top" style="cursor: pointer;" onclick="doView('115800001109290'
,'1')" ><table width="90%" border="0" height="90%" bgcolor="#EBEBEB"><tr align="center"  height="20"
><td style="font-size:13px;">开庭公告</td></tr><tr align="center" valign="top" ><td align="left" ><p style
="font-size:13px;margin:0px;">2017年 01月 18日&nbsp;&nbsp;15:30-16:00第七法庭公开审理&nbsp;&nbsp;(2015)浦民初字第03514
号&nbsp;&nbsp;一案</p></td></tr></table></td><td valign="top" style="cursor: pointer;" onclick="doView('116000001092217'
,'1')" ><table width="90%" border="0" height="90%" bgcolor="#EBEBEB"><tr align="center"  height="20"
><td style="font-size:13px;">开庭公告</td></tr><tr align="center" valign="top" ><td align="left" ><p style
="font-size:13px;margin:0px;">2016年 12月 30日&nbsp;&nbsp;09:30-11:00第十七法庭公开审理&nbsp;&nbsp;(2015)栖民初字第03194
号&nbsp;&nbsp;一案</p></td></tr></table></td></tr><tr height="150" ><td valign="top" style="cursor: pointer
;" onclick="doView('116100001066994','1')" ><table width="90%" border="0" height="90%" bgcolor="#EBEBEB"
><tr align="center"  height="20"><td style="font-size:13px;">开庭公告</td></tr><tr align="center" valign
="top" ><td align="left" ><p style="font-size:13px;margin:0px;">2016年 12月 14日&nbsp;&nbsp;09:00-09:30
板桥法庭一公开审理&nbsp;&nbsp;(2015)雨板商初字第00053号&nbsp;&nbsp;一案</p></td></tr></table></td><td valign="top" style
="cursor: pointer;" onclick="doView('116100001070060','1')" ><table width="90%" border="0" height="90
%" bgcolor="#EBEBEB"><tr align="center"  height="20"><td style="font-size:13px;">开庭公告</td></tr><tr align
="center" valign="top" ><td align="left" ><p style="font-size:13px;margin:0px;">2016年 12月 02日&nbsp;&nbsp
;09:30-10:30第六法庭公开审理&nbsp;&nbsp;(2015)雨民初字第02607号&nbsp;&nbsp;一案</p></td></tr></table></td><td valign
="top" style="cursor: pointer;" onclick="doView('116200001142524','1')" ><table width="90%" border="0"
 height="90%" bgcolor="#EBEBEB"><tr align="center"  height="20"><td style="font-size:13px;">开庭公告</td
></tr><tr align="center" valign="top" ><td align="left" ><p style="font-size:13px;margin:0px;">2016年
 06月 08日&nbsp;&nbsp;14:10-17:30第二法庭公开审理&nbsp;&nbsp;(2013)江宁民初字第04540号&nbsp;&nbsp;一案</p></td></tr></table
></td><td valign="top" style="cursor: pointer;" onclick="doView('116400001120266','1')" ><table width
="90%" border="0" height="90%" bgcolor="#EBEBEB"><tr align="center"  height="20"><td style="font-size
:13px;">开庭公告</td></tr><tr align="center" valign="top" ><td align="left" ><p style="font-size:13px;margin
:0px;">2017年 01月 25日&nbsp;&nbsp;14:30-15:00本部第4法庭公开审理&nbsp;&nbsp;(2015)六商初字第00794号&nbsp;&nbsp;一案</p>
</td></tr></table></td></tr><tr height="150" ><td valign="top" style="cursor: pointer;" onclick="doView
('116400001122651','1')" ><table width="90%" border="0" height="90%" bgcolor="#EBEBEB"><tr align="center"
  height="20"><td style="font-size:13px;">开庭公告</td></tr><tr align="center" valign="top" ><td align="left"
 ><p style="font-size:13px;margin:0px;">2017年 01月 05日&nbsp;&nbsp;15:30-16:00本部第4法庭公开审理&nbsp;&nbsp;(2015
)六商初字第00997号&nbsp;&nbsp;一案</p></td></tr></table></td><td valign="top" style="cursor: pointer;" onclick
="doView('116400001122914','1')" ><table width="90%" border="0" height="90%" bgcolor="#EBEBEB"><tr align
="center"  height="20"><td style="font-size:13px;">开庭公告</td></tr><tr align="center" valign="top" ><td
 align="left" ><p style="font-size:13px;margin:0px;">2017年 01月 05日&nbsp;&nbsp;14:30-15:00本部第4法庭公开审理&nbsp
;&nbsp;(2015)六商初字第01029号&nbsp;&nbsp;一案</p></td></tr></table></td><td valign="top" style="cursor: pointer
;" onclick="doView('116800000078638','1')" ><table width="90%" border="0" height="90%" bgcolor="#EBEBEB"
><tr align="center"  height="20"><td style="font-size:13px;">开庭公告</td></tr><tr align="center" valign
="top" ><td align="left" ><p style="font-size:13px;margin:0px;">2016年 12月 29日&nbsp;&nbsp;09:30-10:00
第一法庭公开审理&nbsp;&nbsp;(2015)崇刑二初字第00187号&nbsp;&nbsp;一案</p></td></tr></table></td><td valign="top" style
="cursor: pointer;" onclick="doView('117000000003700','1')" ><table width="90%" border="0" height="90
%" bgcolor="#EBEBEB"><tr align="center"  height="20"><td style="font-size:13px;">开庭公告</td></tr><tr align
="center" valign="top" ><td align="left" ><p style="font-size:13px;margin:0px;">2202年 07月 15日&nbsp;&nbsp
;08:30-10:304号法庭公开审理&nbsp;&nbsp;(2002)北刑初字第103号&nbsp;&nbsp;一案</p></td></tr></table></td></tr><tr height
="150" ><td valign="top" style="cursor: pointer;" onclick="doView('117000000005018','1')" ><table width
="90%" border="0" height="90%" bgcolor="#EBEBEB"><tr align="center"  height="20"><td style="font-size
:13px;">开庭公告</td></tr><tr align="center" valign="top" ><td align="left" ><p style="font-size:13px;margin
:0px;">2202年 12月 26日&nbsp;&nbsp;13:30-15:305号法庭公开审理&nbsp;&nbsp;(2002)北民一初字第1168号&nbsp;&nbsp;一案</p></td
></tr></table></td><td valign="top" style="cursor: pointer;" onclick="doView('117000000007672','1')"
 ><table width="90%" border="0" height="90%" bgcolor="#EBEBEB"><tr align="center"  height="20"><td style
="font-size:13px;">开庭公告</td></tr><tr align="center" valign="top" ><td align="left" ><p style="font-size
:13px;margin:0px;">2033年 12月 01日&nbsp;&nbsp;13:30-15:304号法庭公开审理&nbsp;&nbsp;(2003)北民一初字第1295号&nbsp;&nbsp
;一案</p></td></tr></table></td><td valign="top" style="cursor: pointer;" onclick="doView('117000000008427'
,'1')" ><table width="90%" border="0" height="90%" bgcolor="#EBEBEB"><tr align="center"  height="20"
><td style="font-size:13px;">开庭公告</td></tr><tr align="center" valign="top" ><td align="left" ><p style
="font-size:13px;margin:0px;">3004年 09月 01日&nbsp;&nbsp;14:00-16:003号法庭公开审理&nbsp;&nbsp;(2004)北民一初字第200
号&nbsp;&nbsp;一案</p></td></tr></table></td><td valign="top" style="cursor: pointer;" onclick="doView('117100000017461'
,'1')" ><table width="90%" border="0" height="90%" bgcolor="#EBEBEB"><tr align="center"  height="20"
><td style="font-size:13px;">开庭公告</td></tr><tr align="center" valign="top" ><td align="left" ><p style
="font-size:13px;margin:0px;">2040年 08月 13日&nbsp;&nbsp;08:30-09:30第二法庭公开审理&nbsp;&nbsp;(2004)惠民二初字第866
号&nbsp;&nbsp;一案</p></td></tr></table></td></tr><tr height="150" ><td valign="top" style="cursor: pointer
;" onclick="doView('117100000021770','1')" ><table width="90%" border="0" height="90%" bgcolor="#EBEBEB"
><tr align="center"  height="20"><td style="font-size:13px;">开庭公告</td></tr><tr align="center" valign
="top" ><td align="left" ><p style="font-size:13px;margin:0px;">2050年 01月 01日&nbsp;&nbsp;03:00-04:00
第一法庭公开审理&nbsp;&nbsp;(2005)惠民初字第202号&nbsp;&nbsp;一案</p></td></tr></table></td><td valign="top" style="cursor
: pointer;" onclick="doView('117100000024571','1')" ><table width="90%" border="0" height="90%" bgcolor
="#EBEBEB"><tr align="center"  height="20"><td style="font-size:13px;">开庭公告</td></tr><tr align="center"
 valign="top" ><td align="left" ><p style="font-size:13px;margin:0px;">5005年 09月 27日&nbsp;&nbsp;00:00-02
:00第一法庭公开审理&nbsp;&nbsp;(2005)惠民二初字第1060号&nbsp;&nbsp;一案</p></td></tr></table></td><td valign="top" style
="cursor: pointer;" onclick="doView('117400000002483','1')" ><table width="90%" border="0" height="90
%" bgcolor="#EBEBEB"><tr align="center"  height="20"><td style="font-size:13px;">开庭公告</td></tr><tr align
="center" valign="top" ><td align="left" ><p style="font-size:13px;margin:0px;">3004年 03月 15日&nbsp;&nbsp
;08:30-09:30张渚第一法庭公开审理&nbsp;&nbsp;(2004)宜民一初字第0029号&nbsp;&nbsp;一案</p></td></tr></table></td><td valign
="top" style="cursor: pointer;" onclick="doView('117400000187635','1')" ><table width="90%" border="0"
 height="90%" bgcolor="#EBEBEB"><tr align="center"  height="20"><td style="font-size:13px;">开庭公告</td
></tr><tr align="center" valign="top" ><td align="left" ><p style="font-size:13px;margin:0px;">2016年
 08月 10日&nbsp;&nbsp;14:30-16:00第十二法庭公开审理&nbsp;&nbsp;(2015)宜民初字第01317号&nbsp;&nbsp;一案</p></td></tr></table
></td></tr><tr height="150" ><td valign="top" style="cursor: pointer;" onclick="doView('117400000187875'
,'1')" ><table width="90%" border="0" height="90%" bgcolor="#EBEBEB"><tr align="center"  height="20"
><td style="font-size:13px;">开庭公告</td></tr><tr align="center" valign="top" ><td align="left" ><p style
="font-size:13px;margin:0px;">2016年 07月 06日&nbsp;&nbsp;13:30-14:00周铁第二法庭公开审理&nbsp;&nbsp;(2015)宜周民初字第00388
号&nbsp;&nbsp;一案</p></td></tr></table></td><td valign="top" style="cursor: pointer;" onclick="doView('117400000196397'
,'1')" ><table width="90%" border="0" height="90%" bgcolor="#EBEBEB"><tr align="center"  height="20"
><td style="font-size:13px;">开庭公告</td></tr><tr align="center" valign="top" ><td align="left" ><p style
="font-size:13px;margin:0px;">2016年 11月 22日&nbsp;&nbsp;09:00-10:00第五法庭公开审理&nbsp;&nbsp;(2015)宜民特字第00043
号&nbsp;&nbsp;一案</p></td></tr></table></td><td valign="top" style="cursor: pointer;" onclick="doView('117400000198839'
,'1')" ><table width="90%" border="0" height="90%" bgcolor="#EBEBEB"><tr align="center"  height="20"
><td style="font-size:13px;">开庭公告</td></tr><tr align="center" valign="top" ><td align="left" ><p style
="font-size:13px;margin:0px;">2016年 07月 29日&nbsp;&nbsp;09:00-09:30第十法庭公开审理&nbsp;&nbsp;(2015)宜民初字第02506
号&nbsp;&nbsp;一案</p></td></tr></table></td><td valign="top" style="cursor: pointer;" onclick="doView('117700000095696'
,'1')" ><table width="90%" border="0" height="90%" bgcolor="#EBEBEB"><tr align="center"  height="20"
><td style="font-size:13px;">开庭公告</td></tr><tr align="center" valign="top" ><td align="left" ><p style
="font-size:13px;margin:0px;">2016年 12月 16日&nbsp;&nbsp;09:30-10:30第十六法庭公开审理&nbsp;&nbsp;(2014)徐民终字第02772
号&nbsp;&nbsp;一案</p></td></tr></table></td></tr><tr height="150" ><td valign="top" style="cursor: pointer
;" onclick="doView('117700000103356','1')" ><table width="90%" border="0" height="90%" bgcolor="#EBEBEB"
><tr align="center"  height="20"><td style="font-size:13px;">开庭公告</td></tr><tr align="center" valign
="top" ><td align="left" ><p style="font-size:13px;margin:0px;">2016年 12月 03日&nbsp;&nbsp;14:00-16:00
第三十二法庭公开审理&nbsp;&nbsp;(2015)徐商初字第00112号&nbsp;&nbsp;一案</p></td></tr></table></td><td valign="top" style
="cursor: pointer;" onclick="doView('117700000109030','1')" ><table width="90%" border="0" height="90
%" bgcolor="#EBEBEB"><tr align="center"  height="20"><td style="font-size:13px;">开庭公告</td></tr><tr align
="center" valign="top" ><td align="left" ><p style="font-size:13px;margin:0px;">2016年 11月 17日&nbsp;&nbsp
;09:00-09:30第十四法庭公开审理&nbsp;&nbsp;(2015)徐民终字第03143号&nbsp;&nbsp;一案</p></td></tr></table></td><td valign
="top" style="cursor: pointer;" onclick="doView('117700000111081','1')" ><table width="90%" border="0"
 height="90%" bgcolor="#EBEBEB"><tr align="center"  height="20"><td style="font-size:13px;">开庭公告</td
></tr><tr align="center" valign="top" ><td align="left" ><p style="font-size:13px;margin:0px;">2016年
 10月 06日&nbsp;&nbsp;14:00-15:00第十六法庭公开审理&nbsp;&nbsp;(2015)徐民终字第03934号&nbsp;&nbsp;一案</p></td></tr></table
></td><td valign="top" style="cursor: pointer;" onclick="doView('117900000092007','1')" ><table width
="90%" border="0" height="90%" bgcolor="#EBEBEB"><tr align="center"  height="20"><td style="font-size
:13px;">开庭公告</td></tr><tr align="center" valign="top" ><td align="left" ><p style="font-size:13px;margin
:0px;">2016年 06月 12日&nbsp;&nbsp;09:30-11:00第九法庭公开审理&nbsp;&nbsp;(2015)云环刑初字第00005号&nbsp;&nbsp;一案</p><
/td></tr></table></td></tr><tr height="150" ><td valign="top" style="cursor: pointer;" onclick="doView
('118200000001043','1')" ><table width="90%" border="0" height="90%" bgcolor="#EBEBEB"><tr align="center"
  height="20"><td style="font-size:13px;">开庭公告</td></tr><tr align="center" valign="top" ><td align="left"
 ><p style="font-size:13px;margin:0px;">3004年 03月 25日&nbsp;&nbsp;08:00-09:00第七法庭公开审理&nbsp;&nbsp;(2004
)泉刑初字第83号&nbsp;&nbsp;一案</p></td></tr></table></td><td valign="top" style="cursor: pointer;" onclick="doView
('118200000004491','1')" ><table width="90%" border="0" height="90%" bgcolor="#EBEBEB"><tr align="center"
  height="20"><td style="font-size:13px;">开庭公告</td></tr><tr align="center" valign="top" ><td align="left"
 ><p style="font-size:13px;margin:0px;">3005年 03月 15日&nbsp;&nbsp;08:30-09:30第七法庭公开审理&nbsp;&nbsp;(2005
)泉刑初字第0042号&nbsp;&nbsp;一案</p></td></tr></table></td><td valign="top" style="cursor: pointer;" onclick
="doView('118400000002026','1')" ><table width="90%" border="0" height="90%" bgcolor="#EBEBEB"><tr align
="center"  height="20"><td style="font-size:13px;">开庭公告</td></tr><tr align="center" valign="top" ><td
 align="left" ><p style="font-size:13px;margin:0px;">2061年 10月 08日&nbsp;&nbsp;09:00-11:00第十审判庭公开审理&nbsp
;&nbsp;(2006)丰民一初字第0891号&nbsp;&nbsp;一案</p></td></tr></table></td><td valign="top" style="cursor: pointer
;" onclick="doView('118500000002324','1')" ><table width="90%" border="0" height="90%" bgcolor="#EBEBEB"
><tr align="center"  height="20"><td style="font-size:13px;">开庭公告</td></tr><tr align="center" valign
="top" ><td align="left" ><p style="font-size:13px;margin:0px;">3004年 01月 16日&nbsp;&nbsp;08:30-10:30
第八法庭公开审理&nbsp;&nbsp;(2004)沛民二初字第137号&nbsp;&nbsp;一案</p></td></tr></table></td></tr><tr height="150" >
<td valign="top" style="cursor: pointer;" onclick="doView('118500000002668','1')" ><table width="90%"
 border="0" height="90%" bgcolor="#EBEBEB"><tr align="center"  height="20"><td style="font-size:13px
;">开庭公告</td></tr><tr align="center" valign="top" ><td align="left" ><p style="font-size:13px;margin:0px
;">3004年 03月 09日&nbsp;&nbsp;09:00-11:00第七法庭公开审理&nbsp;&nbsp;(2004)沛民一初字第221号&nbsp;&nbsp;一案</p></td></tr
></table></td><td valign="top" style="cursor: pointer;" onclick="doView('118500000007942','1')" ><table
 width="90%" border="0" height="90%" bgcolor="#EBEBEB"><tr align="center"  height="20"><td style="font-size
:13px;">开庭公告</td></tr><tr align="center" valign="top" ><td align="left" ><p style="font-size:13px;margin
:0px;">2205年 06月 10日&nbsp;&nbsp;14:30-16:30栖山法庭公开审理&nbsp;&nbsp;(2005)沛民二初字第0104号&nbsp;&nbsp;一案</p></td
></tr></table></td><td valign="top" style="cursor: pointer;" onclick="doView('118500000011126','1')"
 ><table width="90%" border="0" height="90%" bgcolor="#EBEBEB"><tr align="center"  height="20"><td style
="font-size:13px;">开庭公告</td></tr><tr align="center" valign="top" ><td align="left" ><p style="font-size
:13px;margin:0px;">2025年 11月 25日&nbsp;&nbsp;09:30-10:30栖山法庭公开审理&nbsp;&nbsp;(2005)沛民二初字第0671号&nbsp;&nbsp
;一案</p></td></tr></table></td><td valign="top" style="cursor: pointer;" onclick="doView('118700000111861'
,'1')" ><table width="90%" border="0" height="90%" bgcolor="#EBEBEB"><tr align="center"  height="20"
><td style="font-size:13px;">开庭公告</td></tr><tr align="center" valign="top" ><td align="left" ><p style
="font-size:13px;margin:0px;">2017年 04月 05日&nbsp;&nbsp;09:00-10:00第九审判庭公开审理&nbsp;&nbsp;(2016)苏0324民初171
号&nbsp;&nbsp;一案</p></td></tr></table></td></tr><tr height="150" ><td valign="top" style="cursor: pointer
;" onclick="doView('118900000124658','1')" ><table width="90%" border="0" height="90%" bgcolor="#EBEBEB"
><tr align="center"  height="20"><td style="font-size:13px;">开庭公告</td></tr><tr align="center" valign
="top" ><td align="left" ><p style="font-size:13px;margin:0px;">2016年 06月 09日&nbsp;&nbsp;09:15-11:00
第四法庭公开审理&nbsp;&nbsp;(2015)常民终字第01036号&nbsp;&nbsp;一案</p></td></tr></table></td><td valign="top" style
="cursor: pointer;" onclick="doView('118900000128305','2')" ><table width="90%" border="0" height="90
%" bgcolor="#EBEBEB"><tr align="center"  height="20"><td style="font-size:13px;">开庭公告</td></tr><tr align
="center" valign="top" ><td align="left" ><p style="font-size:13px;margin:0px;">2016年 08月 11日&nbsp;&nbsp
;09:00-11:00第五法庭公开审理&nbsp;&nbsp;(2015)常商外初字第00012号&nbsp;&nbsp;一案</p></td></tr></table></td><td valign
="top" style="cursor: pointer;" onclick="doView('119000000005133','1')" ><table width="90%" border="0"
 height="90%" bgcolor="#EBEBEB"><tr align="center"  height="20"><td style="font-size:13px;">开庭公告</td
></tr><tr align="center" valign="top" ><td align="left" ><p style="font-size:13px;margin:0px;">2205年
 12月 20日&nbsp;&nbsp;14:40-16:40第四法庭公开审理&nbsp;&nbsp;(2005)天民一初字第1505号&nbsp;&nbsp;一案</p></td></tr></table
></td><td valign="top" style="cursor: pointer;" onclick="doView('119000000073112','1')" ><table width
="90%" border="0" height="90%" bgcolor="#EBEBEB"><tr align="center"  height="20"><td style="font-size
:13px;">开庭公告</td></tr><tr align="center" valign="top" ><td align="left" ><p style="font-size:13px;margin
:0px;">2017年 09月 08日&nbsp;&nbsp;15:30-16:00第五法庭公开审理&nbsp;&nbsp;(2015)天刑二初字第00143号&nbsp;&nbsp;一案</p><
/td></tr></table></td></tr><tr height="150" ><td valign="top" style="cursor: pointer;" onclick="doView
('119300000071720','1')" ><table width="90%" border="0" height="90%" bgcolor="#EBEBEB"><tr align="center"
  height="20"><td style="font-size:13px;">开庭公告</td></tr><tr align="center" valign="top" ><td align="left"
 ><p style="font-size:13px;margin:0px;">2016年 06月 09日&nbsp;&nbsp;09:15-10:30公开审理&nbsp;&nbsp;&nbsp;&nbsp
;一案</p></td></tr></table></td><td valign="top" style="cursor: pointer;" onclick="doView('119300000072658'
,'1')" ><table width="90%" border="0" height="90%" bgcolor="#EBEBEB"><tr align="center"  height="20"
><td style="font-size:13px;">开庭公告</td></tr><tr align="center" valign="top" ><td align="left" ><p style
="font-size:13px;margin:0px;">2016年 07月 07日&nbsp;&nbsp;15:00-15:30第四审判庭公开审理&nbsp;&nbsp;(2015)新民初字第01600
号&nbsp;&nbsp;一案</p></td></tr></table></td><td width='25%'>&nbsp;</td><td width='25%'>&nbsp;</td></tr"""

reg = r"doView([('\d+')]+)(,)('\d')(\))"
# rs = re.find_all(reg,ss)
rs = re.findall(reg,ss)
rss=list(rs)
print len(rss),type(rss),rss[0][0],rss[0][2],type(rss[0][0])
lsh = rss[0][0][1:].strip("'")
xh = rss[0][2].strip("'")
url = 'http://221.226.175.76:8038/webapp/area/jsgy/fygg/ggll.jsp?pageLx=ktgg&lsh='+str(lsh)+'&xh='+str(xh)
print url
r= requests.get(url)
rbs = BeautifulSoup(r.text,'html5lib')
td_list = rbs.find_all('td')
# print td_list
an_hao = td_list[1].text.strip()
fa_yuan = td_list[4].text.strip()
gong_gao_lei_xing = td_list[6].text.strip()
an_you = td_list[8].text.strip()
li_an_ri_qi = td_list[10].text.strip()
an_jian_zhuang_tai = td_list[12].text.strip()
cheng_ban_ren = td_list[14].text.strip()
cbr_dian_hua = td_list[16].text.strip()
shu_ji_yuan = td_list[18].text.strip()
jie_an_ri_qi = td_list[20].text.strip()
gong_gao_nei_rong = td_list[26].text.strip()
fa_bu_ri_qi = td_list[28].text.strip()
sql = "INSERT INTO jsfy VALUES('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" %(an_hao,fa_yuan,gong_gao_lei_xing,\
	an_you,li_an_ri_qi,an_jian_zhuang_tai,cheng_ban_ren,cbr_dian_hua,shu_ji_yuan,jie_an_ri_qi,gong_gao_nei_rong,fa_bu_ri_qi,today)
print sql
# for i in range(len(td_list)):
# 	print i,td_list[i]