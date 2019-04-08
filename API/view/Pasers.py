# 解析
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser, FormParser
from rest_framework.views import APIView

class  PaserView(APIView):
	"""解析视图"""
	parser_classes = [JSONParser, FormParser]
	# JSONParser 表示解析application/json的头
	# FormParser 表示 application/x-www-form-urlencode 的头
	def post(self, request, *args,**kwargs):
		# 获取解析后的结果
		print(request.data)
		return HttpResponse('解析')