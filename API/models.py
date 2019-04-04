from django.db import models

# Create your models here.
class UserInfo(models.Model):
	"""用户模型"""
	USER_TYPE = (
		(1, '普通用户'),
		(2, 'VIP'),
		(3, 'SVIP'),
	)

	user_type = models.IntegerField("用户类型", choices=USER_TYPE, default=1)
	username = models.CharField("用户名", max_length=32)
	password = models.CharField("用户密码", max_length=64)

class UserToken(models.Model):
	"""用户身份信息"""
	user = models.OneToOneField(UserInfo, on_delete=models.CASCADE)
	token = models.CharField("用户身份令牌", max_length=64)


class UserGroup(models.Model):
	'''
		用户组
	'''
	title = models.CharField(max_length=32)

class Role(models.Model):
	'''
		任务
	'''
	title = models.CharField(max_length=32)

