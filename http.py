# -*- coding: utf-8 -*-

from __future__ import with_statement, print_function

import time
import urllib

import requests
from requests.exceptions import (
    ConnectionError,
    Timeout,
    HTTPError,
    TooManyRedirects,
)

try:
    import gevent
    sleep = gevent.sleep
except ImportError:
    sleep = time.sleep


class CrawlerHttpClient(object):

    def __init__(
            self,
            default_headers=None,
            tries=3,
            try_internal=1,
            rate_limit=None,
            allow_redirects=True,
    ):
        '''
        初始化一个爬虫客户端。

        Args:
            default_headers (dict): 爬虫默认HTTP头信息。
            tries (int): 请求资源失败，重试次数。
            try_internal (int): 请求资源失败，重试间隔。
            rate_limit (int): 请求资源次数限制。
            allow_redirects (bool): 是否追踪重定向。

        Returns:
            None
        '''
        self._login = True
        self._auth_info = None
        self._tries = tries
        self._try_internal = try_internal
        self._rate_limit = rate_limit
        self._allow_redirects = allow_redirects

        self._s = requests.Session()
        self._s.max_redirects = 10  # 最大允许10次重定向

        if default_headers is not None:
            self._s.headers.update(default_headers)

    def get(self, url, data=None, timeout=None):
        '''
        获取URL标识的资源实体。

        Args:
            url (str): 标识资源实体的URL。
            data (dict): 请求参数。
            timeout (int): 请求超时时间。

        Returns:
            None
        '''
        if self._login is False:
            self._login()

        if data is not None:
            url = url + urllib.urlencode(data)

        for i in range(self._tries):
            try:
                resp = self._s.get(
                    url,
                    timeout=timeout,
                    allow_redirects=self._allow_redirects,
                )
                break
            except (
                    ConnectionError,
                    Timeout,
            ):
                sleep((i+1)*self._try_internal)
                continue
            except (
                    HTTPError,
                    TooManyRedirects,
            ):
                raise RuntimeError('Unavaliable url...')
        else:
            raise RuntimeError('Bad network...')
        return resp

    def __call__(self, *args, **kwargs):
        return self.get(*args, **kwargs)

    def login(
            self,
            user,
            password,
            captcha_recognize_callback=None,
            force=False,
    ):
        '''
        登录系统。

        Args:
            user (str): 登录账户。
            password (str): 登录密码。
            captcha_recognize_callback (method): 识别登录验证码的回调函数。
            force (bool): 默认login为lazy模式，force强制登录。

        Returns:
            bool: 标识是否登录成功。
        '''
        self._auth_info = dict()
        self._auth_info['user'] = user
        self._auth_info['password'] = password
        self._auth_info['callback'] = captcha_recognize_callback

        if force is True:
            return self._login()
        return True

    def _login(self):
        raise NotImplementedError()


if __name__ == '__main__':
    httpclient = CrawlerHttpClient()
    resp = httpclient('http://www.weiche.cn')
    if resp is not None:
        print(resp.text)
