from django.urls import path, re_path
# import ipdb; ipdb.set_trace()
from API.view.Authviews import AuthView, OrderView
from API.view.UserView import UserView, UserInfoView, GroupView, UserGroupView
from API.view.Pasers import PaserView
from API.view.Rolesviews import RolesView, PageView, PageView2, PageView3,PageView4

urlpatterns = [
    path('v1/auth/', AuthView.as_view(), name="auth"),
    path('v1/order/', OrderView.as_view(), name="order"), # 用户认证
    # path('v1/info/', UserInfoView.as_view(), name="info"), # 用户权限
    re_path(r'(?P<version>[v1|v2]+)/users/', UserView.as_view(), name='api_user'), # 版本
    re_path(r'(?P<version>[v1|v2]+)/paser/', PaserView.as_view(), name='paser'), # 解析
    re_path(r'(?P<version>[v1|v2]+)/roles/', RolesView.as_view(), name="roles" ), # 序列化
    re_path(r'(?P<version>[v1|v2]+)/info/', UserInfoView.as_view(), name="roles" ), # 序列化
    re_path(r'(?P<version>[v1|v2]+)/group/(?P<pk>\d+)/', GroupView.as_view(), name="gp"), # 序列化生成url
    re_path(r'(?P<version>[v1|v2]+)/usergroup/', UserGroupView.as_view()),    #序列化做验证
    re_path(r'(?P<version>[v1|v2]+)/page/', PageView.as_view()), # 分页1 http://127.0.0.1:8000/api/v1/page/?page=2
    re_path(r'(?P<version>[v1|v2]+)/page2/', PageView2.as_view()), # 分页2 自定义分页 http://127.0.0.1:8000/api/v1/page2/?page=1&size=2
    re_path(r'(?P<version>[v1|v2]+)/page3/', PageView3.as_view()), # 分页3 自定义分页 http://127.0.0.1:8000/api/v1/page3/?offset=1&limit=1 # 偏移几个 显示几个
    re_path(r'(?P<version>[v1|v2]+)/page4/', PageView4.as_view()), # 分页3 自定义分页 http://127.0.0.1:8000/api/v1/page4 加密分页 只允许上一页或者下一页
    
    
    
    
]
