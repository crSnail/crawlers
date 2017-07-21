# -*- coding: utf-8 -*-

import os
import shevle


class CacheFile(object):
    """缓存文件对象。

    Args:
        file_name (str): 文件名称。

    Returns:
        None
    """
    def __init__(self, file_name):
        self._file = file_name

    def flush(self):
        """将数据刷新到缓存文件中。
        """


class Cache(object):
    """爬虫缓存系统。

    Args:
        local_storage (str): 缓存数据的目录。

    Returns:
        None
    """

    def __init__(self, local_storage="./"):
        if not os.path.exists(local_storage):
            os.mkdir(local_storage)
        if not os.path.isdir(local_storage):
            raise IOError()
        self._local_storage = local_storage

    def __getattr__(self, attr):
        """通过属性来访问相应APP。

        Args:
            attr (str): 属性名，一般是爬虫APP名，如itjuzi。

        Returns:
            None
        """
        path = self._local_storage + ".cache" + attr
        cache = shevle.open(path)
        return cache
