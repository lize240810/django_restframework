from rest_framework import exceptions
from API.models import UserToken, UserInfo
from rest_framework.authentication import BaseAuthentication

# 自己写认证类方法梳理

'''
1. 创建认证类
继承BaseAuthentication 1. 重写authenticate，2.authenticate_header方法直接pass 但是必须写
2. authenticate() 返回值
	1.None 当前认证不管，等下一个认证来执行
	2.raise exceptions.AuthenticationFailed("认证失败") # from rest_framework import exceptions
	3. 有返回值元祖形式 （元素1，元素2）
3. 局部使用
	authentication_classes = [BaseAuthentication, ]
4. 全局使用
	REST_FRAMEWORK = {
	    "DEFAULT_AUTHENTICATION_CLASSES":['API.utils.auth.Authentication',]
	}
'''

class Authentications(BaseAuthentication):
	"""用于用户登录认证"""
	def authenticate(self, request):
		# 从get请求中获取到用户认证码   
		token = request._request.GET.get('token')
		# 查询数据库查看是否存在
		token_obj = UserToken.objects.filter(token=token).first()
		if not token_obj:
			raise exceptions.AuthenticationFailed("用户认证失败")
		return (token_obj.user,token_obj)
	
	def authenticate_header(self, request):
		pass
