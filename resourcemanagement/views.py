from django.shortcuts import render
from django.views.generic import View
from resourcemanagement.models import TestSNMP
from django.utils.decorators import method_decorator
from django.http import JsonResponse
import time
from pyzabbix import ZabbixAPI
import requests
import json

# Create your views here.
headers = {
    'Content-Type': 'application/json'
}
def check_login(fn):
    def wrapper(request,*args,**kwargs):
        if request.session.get('is_login', False):
            return fn(request,*args,*kwargs)
        else:
            # 获取用户当前访问的url，并传递给/user/login/
            result = {"status":"failure", "username":str(request.user), "tip":"缺少权限"}
            return JsonResponse(result)
    return wrapper

class GetZabbix:
    def __init__(self):
        #用户信息
        self.username = "Admin"
        self.password = "zabbix"
        self.url = "http://10.0.0.30/zabbix/api_jsonrpc.php"
        self.token = self.getToken()

    def getToken(self):
        data = {
            "jsonrpc": "2.0",
            "method": "user.login",
            "params": {
                "user": self.username,
                "password": self.password
            },
            "id": 1,
            "auth": None
        }
        r = requests.post(url=self.url, headers=headers, data=json.dumps(data))
        token = json.loads(r.content).get("result")
        return token

    def getHosts(self):
        data = {
            "jsonrpc": "2.0",
            "method": "host.get",
            "params": {
                "output": [
                    "hostid",
                    "host"
                ],
                "selectInterfaces": [
                    "interfaceid",
                    "ip"
                ]
            },
            "id": 2,
            "auth": self.token
        }
        r = requests.post(url=self.url, headers=headers, data=json.dumps(data))
        return r.content

    def getItems(self, hostid):
        data = {
            "jsonrpc": "2.0",
            "method": "item.get",
            "params": {
                "output": "extend",
                "hostids": hostid,
            },
            "id": hostid,
            "auth": self.token
        }
        r = requests.post(url=self.url, headers=headers, data=json.dumps(data))
        return r.content

    def getGraphs(self, hostid):
        data = {
            "jsonrpc": "2.0",
            "method": "graph.get",
            "params": {
                "output": "extend",
                "hostids": hostid,
            },
            "id": hostid,
            "auth": self.token
        }
        r = requests.post(url=self.url, headers=headers, data=json.dumps(data))
        return r.content

    def getProblems(self, hostid):
        data = {
            "jsonrpc": "2.0",
            "method": "Problem.get",
            "params": {
                "output": "extend",
                "hostids": hostid,
            },
            "id": hostid,
            "auth": self.token
        }
        r = requests.post(url=self.url, headers=headers, data=json.dumps(data))
        return r.content

class ResourceManagementView(View):
    
    def __init__(self):
        self.zabbix = GetZabbix()

    @method_decorator(check_login)
    def getSnmpInfo(self, request):
        try:
            start = time.clock()
            oid = request.GET.get("oid")
            sys_list = []
            x_index = []
            sys_info = TestSNMP.objects.filter(oid=oid).order_by('id')
            sys_info = sys_info[sys_info.count()-1000:]
            for item in sys_info:
                sys_list.append(item.sysdate)
                x_index.append(item.id)
            end = time.clock()
            print(end-start)
            result = {"status":"success" , "username":str(request.user), "tip": "获取特定设备系统时间成功（仅仅作为测试用途）", "sys_time":sys_list, "x_index":x_index}
            return JsonResponse(result)

        except Exception as e:
            print(e)
            result = {"status":"failure" , "username":str(request.user), "tip":"内部错误"}
            return JsonResponse(result)

    @method_decorator(check_login)
    def getHost(self, request):
        try:
            hosts = json.loads(self.zabbix.getHosts())['result']
            body = []
            for host in hosts:
                hostid = host['hostid']
                hostname = host['host']
                hostip = host['interfaces'][0]['ip']
                items = json.loads(self.zabbix.getItems(hostid))['result']
                items_num = len(items)
                graphs = json.loads(self.zabbix.getGraphs(hostid))['result']
                graphs_num = len(graphs)
                problems = json.loads(self.zabbix.getProblems(hostid))['result']
                problems_num = len(problems)
                elem = {
                    "host": hostname,
                    "hostip": hostip,
                    "hostid": hostid,
                    "items_num": items_num,
                    "graphs_num": graphs_num,
                    "problems_num": problems_num,
                }
                body.append(elem)
            print(body)
            result = {"status":"success" , "username":str(request.user), "tip": "获取主机信息成功", "body":body}
            return JsonResponse(result)

        except Exception as e:
            print(e)
            result = {"status":"failure" , "username":str(request.user), "tip":"内部错误"}
            return JsonResponse(result)


    @method_decorator(check_login)
    def getProblems(self, request):
        try:
            hostid = int(request.GET.get("hostid"))
            problems = json.loads(self.zabbix.getProblems(hostid))['result']
            body = []
            for problem in problems:
                clock = int(problem["clock"])
                timeArray = time.localtime(clock)
                date = time.strftime("%Y年%m月%d日 %H:%M:%S", timeArray)
                severity = problem["severity"]
                name = problem["name"]
                print(problem)
                elem = {
                    "date": date,
                    "severity":severity,
                    "name":name,    
                }
                body.append(elem)
            print(body)
            result = {"status":"success" , "username":str(request.user), "tip": "获取主机problems信息成功", "body":body}
            return JsonResponse(result)

        except Exception as e:
            print(e)
            result = {"status":"failure" , "username":str(request.user), "tip":"内部错误"}
            return JsonResponse(result)
