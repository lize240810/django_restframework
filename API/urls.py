from django.urls import path, re_path
# import ipdb; ipdb.set_trace()
from API.view.Authviews import AuthView, OrderView, UserInfoView
from API.view.UserView import UserView

urlpatterns = [
    path('v1/auth/', AuthView.as_view(), name="auth"),
    path('v1/order/', OrderView.as_view(), name="order"), # 用户认证
    path('v1/info/', UserInfoView.as_view(), name="info"), # 用户权限
    re_path(r'(?P<version>[v1|v2]+)/users/', UserView.as_view(), name='api_user') # 版本
]
