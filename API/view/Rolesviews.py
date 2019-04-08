from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination, CursorPagination

from API.models import UserInfo, Role

# 使用序列化 需要先写一个序列化的类


class RolesSerializer(serializers.Serializer):
    """Role表里的字段id和title序列化"""
    id = serializers.IntegerField()
    title = serializers.CharField()


class RolesView(APIView):
    """序列化"""
    authentication_classes = []  # 里面为空代表不需要认证
    permission_classes = []  # 里面为空，代表不需要权限
    # 默认的节流是登录用户 (10/m) ，
    # throttle_classes = [VisitThrottle,] # 局部配置，（不适用settings 中的全局配置的时候）

    def get(self, request, *args, **kwargs):
        # import ipdb
        # ipdb.set_trace()
        # # Queryset
        # roles = Role.objects.all()
        # # 序列化
        # ser = RolesSerializer(instance=roles, many=True)
        # # 转换格式
        # ret = json.dumps(ser.data, ensure_ascii=False)
        # return HttpResponse(ret)

        # 方式二
        role = Role.objects.all().first()
        ser = RolesSerializer(instance=role, many=False)
        return JsonResponse(ser.data)


        
        

class PageSerialiser(serializers.ModelSerializer):
    """分页序列化"""
    class Meta:
        model = Role
        fields = "__all__"

class PageView(APIView):
    """分页视图"""
    def get(self, request, *args, **kwargs):
        # 获取所有数据
        roles = Role.objects.all()
        # 创建分页对象
        pg = PageNumberPagination()
        # 获取分页的数据
        page_roles = pg.paginate_queryset(queryset=roles, request=request, view=self)
        # 对数据进行序列化
        ser = PageSerialiser(instance=page_roles, many=True)
        return Response(ser.data)
        

# 自定义分页
class MyPageNumberPagination(PageNumberPagination):
    """每页显示多少个"""
    page_size = 3
    # 默认每页显示3个 传入参数改变个数
    page_size_query_param = 'size'
    # 最大页数不超过10
    max_page_size = 10
    # 获取页码数
    page_query_param = "page"


class PageView2(APIView):
    """分页视图"""
    def get(self, request, *args, **kwargs):
        # 获取所有数据
        roles = Role.objects.all()
        # 创建分页对象
        pg = MyPageNumberPagination()
        # 获取分页的数据
        page_roles = pg.paginate_queryset(queryset=roles, request=request, view=self)
        # 对数据进行序列化
        ser = PageSerialiser(instance=page_roles, many=True)
        return pg.get_paginated_response(ser.data) 

# 自定义分页2
class MyLimitOffsetPagination(LimitOffsetPagination):
    # 默认显示个数
    default_limit = 2
    # 当前的位置
    offset_query_param = "offset"
    # 通过limit 改变显示个数
    limit_query_param = "limit"
    # 一页最多显示多少个
    max_limit = 10

class PageView3(APIView):
    """分页视图"""
    def get(self, request, *args, **kwargs):
        # 获取所有数据
        roles = Role.objects.all()
        # 创建分页对象
        pg = MyLimitOffsetPagination()
        # 获取分页的数据
        page_roles = pg.paginate_queryset(queryset=roles, request=request, view=self)
        # 对数据进行序列化
        ser = PageSerialiser(instance=page_roles, many=True)
        # return Response(ser.data)
        # 自带上一页 或下一页
        return pg.get_paginated_response(ser.data)


# 自定义分页 加密分页 只能通过点击上一页和下一页访问数据
class MyCursorPagination(CursorPagination):
    """加密分页"""
    cursor_query_param = 'cursor' 
    page_size = 2 # 每页显示2个数据
    ordering = 'id' # 排序
    page_size_query_param = None
    max_page_size = None


class PageView4(APIView):
    """加密分页"""
    def get(self, request, *args, **kwargs):
        roles = Role.objects.all()
        # 创建分页对象
        pg = MyCursorPagination()
        # 获取分页的数据
        page_roles = pg.paginate_queryset(queryset=roles, request=request, view=self)
        # 对数据进行序列化
        ser = PageSerialiser(instance=page_roles, many=True)
        # return Response(ser.data)
        # 自带上一页 或下一页
        return pg.get_paginated_response(ser.data)
