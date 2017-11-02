# coding=utf-8

import requests
import json
import time
import os
from PIL import Image
import random
import Logger
import re


class SpiderMan(object):

    session = None
    manager_host = '118.190.114.196'
    manager_port = 8080
    order = None
    log_name = None

    def __init__(self, order='38c7e5f5-59a1-11e7-bda9-f45c89a63279', keep_session=True, keep_ip=False, max_try_times=3):
        self.order = order
        self.keep_ip = keep_ip
        if self.keep_ip:
            self.expected_ip = ''
        if keep_session:
            self.session = requests.session()
        if max_try_times:
            self.max_try_times = max_try_times

    def info(self, msg):
        Logger.write(msg, name=self.log_name, print_msg=True)

    def reset_session(self):
        self.session = requests.session()

    def get(self, url, **kwargs):
        for t in range(self.max_try_times):
            proxy_config = self.get_proxy()
            # print proxy_config
            kwargs['proxies'] = {'http': 'http://%(user)d:%(pwd)s@%(proxy)s' % proxy_config,
                                 'https': 'https://%(user)d:%(pwd)s@%(proxy)s' % proxy_config}
            kwargs['timeout'] = proxy_config['timeout']
            # if 'headers' in kwargs:
            #     kwargs['headers']['Proxy-Authentication'] = proxy_config['secret_key']
            # else:
            #     kwargs['headers'] = {'Proxy-Authentication': proxy_config['secret_key']}
            try:
                if self.session:
                    return self.session.get(url=url, **kwargs)
                else:
                    return requests.get(url=url, **kwargs)
            except requests.exceptions.RequestException, e:
                if t == self.max_try_times - 1:
                    raise e

    def post(self, url, **kwargs):
        for t in range(self.max_try_times):
            proxy_config = self.get_proxy()
            kwargs['proxies'] = {'http': 'http://%(user)d:%(pwd)s@%(proxy)s' % proxy_config,
                                 'https': 'https://%(user)d:%(pwd)s@%(proxy)s' % proxy_config}
            kwargs['timeout'] = proxy_config['timeout']
            # if 'headers' in kwargs:
            #     kwargs['headers']['Proxy-Authentication'] = proxy_config['secret_key']
            # else:
            #     kwargs['headers'] = {'Proxy-Authentication': proxy_config['secret_key']}
            try:
                if self.session:
                    return self.session.post(url=url, **kwargs)
                else:
                    return requests.post(url=url, **kwargs)
            except requests.exceptions.RequestException, e:
                if t == self.max_try_times - 1:
                    raise e

    def reset_ip(self):
        self.expected_ip = ''

    def get_proxy(self):
        while True:
            url = 'http://%s:%d/get-proxy-api' % (self.manager_host, self.manager_port)
            params = {'order': self.order}
            if self.keep_ip:
                params['expected_ip'] = self.expected_ip
            res = requests.get(url, params=params)
            if res.status_code == 200:
                json_obj = json.loads(res.text)
                if self.keep_ip:
                    self.expected_ip = json_obj['proxy'].split(':')[0]
                return json_obj
            else:
                time.sleep(1)
                print u'暂无可用代理'

    def add_to_black_list(self, domain, proxy):
        params = {'domain': domain, 'proxy': proxy}
        url = 'http://%s:%d/add-to-black-list' % (self.manager_host, self.manager_port)
        requests.post(url, params=params)

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


def get_param_value(url, param):
    l1 = re.split('[?&]', url)
    for p in l1:
        l2 = p.split('=')
        if l2[0] == param:
            return l2[1]
    return None


if __name__ == '__main__':
    crawler = SpiderMan('5fe6cf97-5592-11e7-be16-f45c89a63279')
    # print crawler.get_proxy()
    ts = time.time()
    for i in range(40):
        r = crawler.get('http://1212.ip138.com/ic.asp')
        r.encoding = 'gbk'
        print time.time() - ts
        print r.text

        # r.encoding = 'gbk'
        # print r.text

        # crawler.get_proxy()
