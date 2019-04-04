import time
from rest_framework.throttling import BaseThrottle, SimpleRateThrottle

VISIT_RECORD = {}  # 保存访问记录


# # 第一种节流方式
# class VisitThrottle(BaseThrottle):
#     """限制访问次数"""

#     def __init__(self):
#         self.history = None  # 初始化访问记录

#     def allow_request(self, request, view):
#         # 获取用户记录
#         # self.get_ident(request) 获取当前请求的ip
#         remote_addr = self.get_ident(request)
#         ctime = time.time()  # 获得当前时间戳
#         # 如果Ip不存在那么就添加到访问记录里面
#         if remote_addr not in VISIT_RECORD:
#             # 保存在访问记录中
#             VISIT_RECORD[remote_addr] = [ctime, ]  # 键值对形式保存
#             # 没有记录证明没有访问过 可以直接访问
#             return True  # True 表示可以访问
#         # 获得当前访问记录
#         history = VISIT_RECORD.get(remote_addr)
#         # 初始化访问记录
#         self.history = history
#         # 如果历史记录里面存在这访问记录那么就删除最早的一次超过60s的访问记录
#         while history and history[-1] < ctime - 60:
#             # 1. 判断 history列表是否为空 并且 判断 最后一次是否小于当前时间-60s
#             history.pop()
#            # 如果访问不超过三次, 就把当前访问记录插到第一个位置
#         if len(history) < 3:
#         	# 列表指定位置插入
#         	history.insert(0, ctime)
#         	return True

#     def wait(self):
#     	'''
#     		重写方法
#     		还需要多久等待时间
#     	'''
#     	# 当前时间戳
#     	ctime = time.time()
#     	#
#     	return 60 - (ctime - self.history[-1])


class VisitThrottle(SimpleRateThrottle):
    """匿名用户60s只能访问三次(根据ip)"""
    scope = 'LIZE'  # 这里的值， 自己定义m srttings 里面根据这个值配置Rate

    def get_cache_key(self, request, view):
        # 通过ip节流
        return self.get_ident(request)

class UserThrottle(SimpleRateThrottle): # 全局配置 根据ip限制
    """登录用户60s可以访问10次"""
    scope = 'LIZEUser'

    def get_cache_key(self, request, view):
        return request.user.username

