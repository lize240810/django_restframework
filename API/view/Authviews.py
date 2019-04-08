import time

from django.shortcuts import render
from django.http import JsonResponse, HttpResponse # 返回Json格式、
from rest_framework.views import APIView
from API.models import UserInfo, UserToken
from rest_framework.request import Request
from rest_framework import exceptions
# 登录认证
from rest_framework.authentication import BasicAuthentication
# 权限
from API.utils.permission import SVIPpermission, MyPermission
# 节流
from API.utils.throttle import  VisitThrottle


ORDER_DICT = {
	1:{
		'name': 'apple',
		'price': 15
	},
	2:{
		'name': 'dog',
		'price': 100
	}
}

def md5(user):
	"""用户密码加密"""
	import hashlib 
	# 当前时间 生成一个随机字符串
	ctime = str(time.time())
	m = hashlib.md5()
	m.update(user.encode('utf-8'))
	return m.hexdigest()

class AuthView(APIView):
	"""认证视图"""

	authentication_classes = [] # 里面为空代表不需要认证
	permission_classes = [] # 里面为空，代表不需要权限
	def post(self, request, *args, **kwargs):
		ret = {'code': 1000, 'msg': None}
		try:
			user = request._request.POST.get('username')
			pwd = request._request.POST.get("password")
			# import ipdb; ipdb.set_trace()
			obj = UserInfo.objects.filter(username=user, password=pwd).first()
			# 为用户创建token
			
			if not obj:
				ret['code'] = 1001
				ret['msg'] = '用户名或密码错误'
			else:
				token = md5(user)
				# 存在就更新， 不存在就创建
				UserToken.objects.update_or_create(user=obj, defaults={'token': token})
			ret['token'] = token
		except Exception as e:
			ret['token'] = 1002
			ret['msg'] = '请求异常'
		return JsonResponse(ret)


class OrderView(APIView):
	"""订单相关业务"""
	
	# authentication_classes = [Authentication,] # 添加认证
	# authentication_classes = [] 
	def get(self, request, *args, **kwargs):
		# import ipdb; ipdb.set_trace()
		# 状态码
		ret = {'code': 1000, 'msg': None, 'data': None}
		# 
		try:
			ret['data'] = ORDER_DICT
		except Exception as e:
			pass
		return JsonResponse(ret)
		

class UserInfoView(APIView):
	"""订单相关业务（普通用户和VIP用户都可以看）"""
	permission_classes = [MyPermission,] # 不用全局的配置就使用自己的配置
	def get(self, request, *args, **kwargs):
		print(request.user)
		return HttpResponse("用户信息")


