import json

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.versioning import URLPathVersioning
from rest_framework import serializers

from API.utils.throttle import VisitThrottle
from API.models import UserInfo, UserGroup


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


# 方法一. 使用序列化串行器
# class UserInfoSerializer(serializers.Serializer):
# 	"""序列化用户信息"""
# 	type = serializers.CharField(source='get_user_type_display') # 显示全部source
# 	username = serializers.CharField()
# 	password = serializers.CharField()
# 	# 组的名字
# 	group = serializers.CharField(source="group.title")
# 	# 表示自定义显示
# 	rls = serializers.SerializerMethodField()

# 	def get_rls(self, row):
# 		# 获得用户的所有角色
# 		role_obj_list = row.roles.all()
# 		ret = []
# 		for item in role_obj_list:
# 			ret.append({'id': item.id, 'title': item.title})
# 		return ret

# 方法二 使用模型序列化
# class UserInfoSerializer(serializers.ModelSerializer):
# 	# 需要序列化的字段
# 	type = serializers.CharField(source="get_user_type_display") 吧
# 	group = serializers.CharField(source="group.title")
# 	rls = serializers.SerializerMethodField()

# 	def get_rls(self, row):
# 		# 获得所有的数据库中的对象
# 		# 获取用户所有的角色
# 		role_obj_list = row.roles.all()
# 		ret = []
# 		# 获取角色的id和名字
# 		# 以字典的形式显示
# 		for item in role_obj_list:
# 			ret.append({'id': item.id, 'title': item.title})
# 		return ret

# 	class Meta:
# 		# 指定模型 与显示字段
# 		model = UserInfo
# 		fields = ['id', 'username', 'password', 'type', 'group', 'rls']


# 方法三、 自动序列化链表(depth)
class UserInfoSerializer(serializers.ModelSerializer):
    """自动化序列链表"""
    group = serializers.HyperlinkedIdentityField(view_name='gp',lookup_field='group_id',lookup_url_kwarg='pk')
    class Meta:
        model = UserInfo
        fields = ['id', 'username', 'password', 'group', 'roles']
        # 表示链表深度
        depth = 0


class UserInfoView(APIView):
    """用户的信息"""

    def get(self, request, *args, **kwargs):
        # import ipdb; ipdb.set_trace()
        users = UserInfo.objects.all()
        ser = UserInfoSerializer(instance=users, many=True, context={'request':request})
        ret = json.dumps(ser.data, ensure_ascii=False)
        return HttpResponse(ret)


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserGroup
        fields = "__all__"


class GroupView(APIView):
    """组视图"""

    def get(self, request, *args, **kwargs):
        # import ipdb
        # ipdb.set_trace()
        pk = kwargs.get('pk')  # 获取主键
        # 根据主键查询数据
        obj = UserGroup.objects.filter(pk=pk).first()
        ser = GroupSerializer(instance=obj, many=False)
        return JsonResponse(ser.data)


class UserView(APIView):
    """获取版本"""
    authentication_classes = []  # 里面为空代表不需要认证
    permission_classes = []  # 里面为空，代表不需要权限
    # 默认的节流是登录用户 (10/m) ，
    throttle_classes = [VisitThrottle, ]  # 局部配置，（不适用settings 中的全局配置的时候）

    def get(self, request, *args, **kwargs):
        # 获取版本
        print(request.version)
        # 获取版本处理对象
        print(request.versioning_scheme)
        # 反向解析
        url_path = request.versioning_scheme.reverse(
            viewname='api_user', request=request)
        print(url_path)
        return HttpResponse("用户列表")


class UserGroupSerializer(serializers.Serializer):
    title = serializers.CharField()

class UserGroupView(APIView):
    def post(self,request,*args, **kwargs):
        ser = UserGroupSerializer(data=request.data)
        if ser.is_valid():
            print(ser.validated_data['title'])
        else:
            print(ser.errors)

        return HttpResponse("用户提交数据验证")