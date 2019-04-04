from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.versioning import URLPathVersioning
from API.utils.throttle import  VisitThrottle


# class UserView(APIView):
# 	"""用户版本控制"""
# 	authentication_classes = [] # 里面为空代表不需要认证
# 	permission_classes = [] # 里面为空，代表不需要权限
# 	# 默认的节流是登录用户 (10/m) ，
# 	throttle_classes = [VisitThrottle,] # 局部配置，（不适用settings 中的全局配置的时候）

# 	versioning_class = URLPathVersioning
# 	def get(self, request, *args, **kwargs):
# 		# import ipdb; ipdb.set_trace()
# 		# 获取版本
# 		print(request.version)
# 		return HttpResponse("用户列表")



class UserView(APIView):
	"""获取版本"""
	authentication_classes = [] # 里面为空代表不需要认证
	permission_classes = [] # 里面为空，代表不需要权限
	# 默认的节流是登录用户 (10/m) ，
	throttle_classes = [VisitThrottle,] # 局部配置，（不适用settings 中的全局配置的时候）
	def get(self, request, *args,**kwargs):
		# 获取版本
		print(request.version)
		# 获取版本处理对象
		print(request.versioning_scheme) 
		# 反向解析
		url_path = request.versioning_scheme.reverse(viewname='api_user', request=request)
		print(url_path)
		return HttpResponse("用户列表")
		
