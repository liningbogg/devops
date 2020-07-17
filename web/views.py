from django.shortcuts import render
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.http import HttpResponse
from django.core.cache import cache
import time
import gvcode
import json
from django.contrib import auth
import jwt
from django.http import JsonResponse
from web.models import *

def check_login(fn):
    def wrapper(request,*args,**kwargs):
        if request.session.get('is_login', False):
            return fn(request,*args,*kwargs)
        else:
            # 获取用户当前访问的url，并传递给/user/login/
            result = {"status":"failure", "username":str(request.user), "tip":"缺少权限"} 
            return JsonResponse(result)
    return wrapper

# Create your views here.
class WebView(View):

    
    # 简单测试用例
    @method_decorator(check_login)
    def test(self, request):
        try:
            message = "date from django %s" % time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            result = {"status":"success" , "username":str(request.user), "tip": "获取后端时间成功", "message":message} 
            return JsonResponse(result)
        except Exception as e:
            result = {"status":"failure" , "username":str(request.user), "tip":"内部错误"} 
            return JsonResponse(result)
            



    # 判断验证码是否正确
    def check_captcha(self, uuid, captcha):
        right_captcha = cache.get(uuid)
        if right_captcha is None:
            return False
        else:
            captcha = captcha.replace(" ", "")
            if captcha.lower() == right_captcha.lower():
                return True
            else:
                return False


    # 用户注册模块
    def register(self, request):
        try:
            username = request.GET.get("username")
            captcha = request.GET.get("captcha")
            password = request.GET.get("password")
            uuid = request.GET.get("uuid")
            if self.check_captcha(uuid, captcha) is False:
                result = {"status":"failure" , "username":username, "tip":"验证码错误"} 
                return JsonResponse(result)
            # 判断用户是否存在
            user = auth.authenticate(username=username, password=password)
            if user:
                result = {"status":"failure" , "username":username, "tip":"用户已经存在"} 
                return JsonResponse(result)
            user = DevopsUser.objects.create_user(username=username, password=password)
            user.save()
            # 添加到session
            request.session['username'] = username
            result = {"status":"success", "username":username, "tip":"注册成功"} 
            return JsonResponse(result)
        except Exception as e:
            print(e)
            result = {"status":"failure", "username":username, "tip":"注册失败,内部错误"} 
            return JsonResponse(result)


    # 用户登录模块
    def login(self, request):
        try:
            username = request.GET.get("username")
            password = request.GET.get("password")
            user = auth.authenticate(username=username, password=password)
            if user is not None and user.is_active:
                devops_user =DevopsUser.objects.filter(username=username)
                session_key = devops_user.first().session_key
                print(session_key)
                if session_key:
                    request.session.delete(session_key)
                auth.login(request, user)
                devops_user.update(session_key=request.session.session_key)
                request.session['is_login'] = True
                encoded_jwt = jwt.encode({'username':username},'secret_key',algorithm='HS256')
                result = {"status":"success", "username":username, "tip":"用户登录成功:"+username, "token":str(encoded_jwt, encoding='utf-8')} 
                return JsonResponse(result)
            else:
                result = {"status":"failure", "username":username, "tip":"登录失败,用户名或密码错误"} 
                return JsonResponse(result)

            
        except Exception as e:
            print(e)
            result = {"status":"failure", "username":username, "tip":"登录失败,内部错误"} 
            return JsonResponse(result)
            

    # 用户退出登录
    def logout(self, request):
        try:
            auth.logout(request)
            result = {"status":"success", "username":str(request.user), "tip":"退出登录成功"} 
            return JsonResponse(result)

        except Exception as e:
            print(e)
            result = {"status":"failure", "username":str(request.user), "tip":"退出登录失败,内部错误"} 
            return JsonResponse(result)


    # 验证码生成
    def get_captcha(self, request):
        try:
            if request.method == 'GET':
                uuid = request.GET.get("uuid")
                imgData, rightCode = gvcode.base64()
                cache.set(uuid, rightCode, nx=True) 
                cache.expire(uuid, 300)
                return HttpResponse(imgData, content_type="image/jpeg")

        except Exception as e:
            print(e)

