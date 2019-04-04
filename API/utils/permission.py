'''
	权限管理
1, '普通用户'
2, 'VIP'
3, 'SVIP'
'''
# 权限使用
'''
	1. 使用
	自己写的权限类: 1. 必须继承BasePermission类， 2.必须实现has_permission方法
	2. 返回值
	True # 有权访问
	Flase # 无权访问
	3. 局部
	permission_classes = [MyPremission, ]
	4. 全局
	REST_FRAMEWORK = [
		# 权限
		"DEFAULT_PERMISSION_CLASSES": ['# 自己写的权限的位置']
	]
'''

class SVIPpermission(object):
	mssage = "必须是svip才能访问"
	def has_permission(self, request, view):
		if request.user.user_type !=3:
			return False
		return True

class MyPermission(object):
	def has_permission(self, request, view):
		if request.user.user_type == 3:
			return False
		return True
		