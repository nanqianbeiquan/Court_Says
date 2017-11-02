import re
a='http://xzzy.chinacourt.org/article/detail/2016/03/id/2119390.shtml'
print re.search('\d{6,}',a).group()