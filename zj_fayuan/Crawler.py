# coding=utf-8

import requests
from ProxyConf import ProxyConf, key3
from requests.exceptions import RequestException
from MyException import StatusCodeException
from requests.exceptions import ReadTimeout
from requests.exceptions import ConnectTimeout
from requests.exceptions import ProxyError
from requests.exceptions import ConnectionError
from requests.exceptions import ChunkedEncodingError
from PIL import Image
import logger
import os
import sys
import random
import platform
from bs4 import element


class Crawler(object):

    headers = {}
    session = requests.session()
    requests_timeout = 60
    max_try_times = 15
    use_proxy = False
    proxy_config = None
    app_key = key3
    log_name = None
    print_msg = True
    start_page = 1
    page_idx = -1

    def __init__(self, use_proxy=False):
        self.use_proxy = use_proxy
        if self.use_proxy:
            self.proxy_config = ProxyConf(self.app_key)
            self.session.proxies = self.proxy_config.get_proxy()

    def turn_off_print(self):
        self.print_msg = False

    def reset_session(self):
        self.session = None
        if self.use_proxy:
            self.proxy_config = ProxyConf(self.app_key)
            self.session.proxies = self.proxy_config.get_proxy()

    def get(self, url, t=1, **kwargs):
        """
        发送get请求,包含添加代理,锁定ip与重试机制
        :param url: 请求的url
        :param t: 重试次数
        """
        try:
            if self.use_proxy:
                self.headers['Proxy-Authorization'] = self.proxy_config.get_auth_header()
            r = self.session.get(url=url, headers=self.headers, timeout=self.requests_timeout, **kwargs)
            if r.status_code != 200:
                # print '*', r.text
                #self.info(u'错误的响应代码: %d' % r.status_code)
                raise StatusCodeException(str(r.status_code))
            return r
        except (StatusCodeException, RequestException, ChunkedEncodingError, ReadTimeout, ConnectTimeout, ProxyError, ConnectionError) as e:
            # traceback.print_exc(e)
            if t == self.max_try_times:
                raise e
            else:
                if t>10:
                    import time
                    time.sleep(2)
                return self.get(url, t+1, **kwargs)

    def post(self, url, t=2, **kwargs):
        """
        发送post请求,包含添加代理,锁定ip与重试机制
        :param url: 请求的url
        :param t: 重试次数
        :return:
        """
        try:
            if self.use_proxy:
                self.headers['Proxy-Authorization'] = self.proxy_config.get_auth_header()
            r = self.session.post(url=url, headers=self.headers, timeout=self.requests_timeout, **kwargs)
            if r.status_code != 200:
                #self.info(u'错误的响应代码: %d' % r.status_code)
                raise StatusCodeException(str(r.status_code))
            return r
        except (StatusCodeException, RequestException, ChunkedEncodingError, ReadTimeout, ConnectTimeout, ProxyError, ConnectionError) as e:
            # traceback.print_exc(e)
            if t == self.max_try_times:
                raise e
            else:
                return self.post(url, t+1, **kwargs)

    def info(self, msg):
        logger.write(msg, name=self.log_name, print_msg=self.print_msg)

    def download_yzm(self, image_url, yzm_path=None):
        r = self.get(url=image_url)
        # print r.headers
        # print r.text
        if not yzm_path:
            yzm_path = self.get_yzm_path()
        # print yzm_path
        with open(yzm_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)
                    f.flush()
            f.close()
        return yzm_path

    def download_file(self, src_url, dst_path):
        r = self.get(url=src_url)
        with open(dst_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)
                    f.flush()
            f.close()

    def get_yzm_path(self):
        self
        return os.path.join(os.path.dirname(__file__), '../temp/' + str(random.random())[2:] + '.jpg')

    def get_yzm(self, yzm_url):
        yzm_path = self.download_yzm(yzm_url)
        yzm = self.recognize_yzm(yzm_path)
        print yzm
        os.remove(yzm_path)
        # print yzm_path
        return yzm

    def recognize_yzm(self, yzm_path):
        """
            输入验证码保存路径,识别验证码
            :param yzm_path: 验证码路径
            :return: 验证码识别结果
            """
        self
        image = Image.open(yzm_path)
        image.show()
        print '请输入验证码:'
        yzm = raw_input()
        image.close()
        # os.remove(path)
        return yzm


def get_args():
    args = dict()
    for arg in sys.argv:
        kv = arg.split('=')
        if len(kv) == 2:
            k = kv[0]
            if k != 'topic':
                # v = kv[1]
                if platform.system() == 'Windows':
                    v = kv[1].decode('gbk', 'ignore')
                else:
                    v = kv[1]
            else:
                v = kv[1]
            args[k] = v
    return args


def get_text(soup):
    # print soup
    res = ''
    if isinstance(soup, element.NavigableString):
        if unicode(soup).strip() not in ('', '{C}'):
            return unicode(soup)+'\n'
    else:
        for c in soup.children:
            # if not isinstance(c, element.NavigableString):
            #     print type(c), c.tag, c.text
            res += get_text(c)
    return res

# def read_doc_file(path):
#     doc = docx.opendocx(path)


if __name__ == '__main__':
    crawler = Crawler(False)
    # crawler.download_yzm('http://wenshu.court.gov.cn/User/ValidateCode')
    # crawler.download_file('http://www.gzcourt.gov.cn:8080/ywxt/cpws/download.jsp?AHDM=20154401001200200523', '../data/test2.doc')
    # read_doc_file('../data/test.docx')
    crawler.get()
    crawler.post()