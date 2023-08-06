# -*- coding: utf_8 -*-
# @Create   : 2021/6/25 16:59
# @Author   : yh
# @Remark   : mx框架Server层
from mx.conf_base import ConfBase


class Server(ConfBase):

    def __init__(self):
        super().__init__()
        self.db = getattr(self, '__db__')() if hasattr(self, '__db__') else None
        self.model = getattr(self, '__model__') if hasattr(self, '__model__') else None

    def create(self, *args, **kwargs):
        """
        添加数据的base方法
        """
        return self.db.create(*args, **kwargs)

    def update(self, *args, **kwargs):
        """
        更新数据的base方法
        """
        return self.db.update(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """
        删除数据的base方法
        """
        return self.db.delete(*args, **kwargs)
