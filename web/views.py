from django.shortcuts import render
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core.cache import cache
import time
import gvcode
import json
from django.contrib import auth
from web.models import *


# Create your views here.
class WebView(View):

    @classmethod
    def index(cls, request):
        return render(request, 'web/index.html', None)
    
    # 简单测试用例
    def test(self, request):
        return HttpResponse("date from django %s" % time.strftime('%Y-%m-%d %H:%M:%S' , time.localtime()))

    # 判断验证码是否正确
    def check_captcha(self, uuid, captcha):
        right_captcha = cache.get(uuid)
        if right_captcha is None:
            return False
        else:
            captcha = captcha.replace(" ","")
            if captcha.lower() == right_captcha.lower():
                return True
            else:
                return False


    #用户注册模块
    def register(self, request):
        try:
            username = request.GET.get("username")
            captcha = request.GET.get("captcha")
            password = request.GET.get("password")
            uuid = request.GET.get("uuid")
            if self.check_captcha(uuid, captcha) is False:
                result = {"status":"failure" ,"username":username, "tip":"验证码错误"} 
                return HttpResponse(json.dumps(result))
            # 判断用户是否存在
            user = auth.authenticate(username=username, password=password)
            if user:
                result = {"status":"failure" ,"username":username, "tip":"用户已经存在"} 
                return HttpResponse(json.dumps(result))
            user = DevopsUser.objects.create_user(username=username, password=password)
            user.save()
            # 添加到session
            request.session['username'] = username
            result = {"status":"success" ,"username":username, "tip":"注册成功"} 
            return HttpResponse(json.dumps(result))
        except Exception as e:
            print(e)
            result = {"status":"failure" ,"username":username, "tip":"注册失败,内部错误"} 
            return HttpResponse(json.dumps(result))

    #验证码生成
    def get_captcha(self, request):
        try:
            if request.method == 'GET':
                uuid = request.GET.get("uuid")
                imgData, rightCode = gvcode.base64()
                cache.set(uuid, rightCode, nx=True) 
                cache.expire(uuid, 300)
                print(uuid,rightCode)
                return HttpResponse(imgData, content_type="image/jpeg")

        except Exception as e:
            print(e)

