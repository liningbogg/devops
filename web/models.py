from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser

class DevopsUser(AbstractUser):
    """
    session_key: 用户session关键字
    mobile: 手机号码
    enterprise: 工作单位 
    """
    session_key = models.CharField(max_length=255,null=True)
    mobile = models.CharField(max_length=11,null=True)
    enterprise =  models.CharField(max_length=255,null=True)
