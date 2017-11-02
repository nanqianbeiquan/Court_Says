#coding=utf-8
import os
import sys
import time

reload(sys)
sys.setdefaultencoding('utf8')

# path = r'E:\\My_Spider\\'
path = sys.path[0]
# print path
for i in os.listdir(path):
	if i.endswith('.py'):
		# print i
		if i != 'daydayupdate4server.py':
                        dpath = path+'\\'+i
                        # print dpath
                        
                        os.startfile(dpath)
                        # time.sleep(1)
