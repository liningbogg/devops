from django.db import models

# Create your models here.

class BaseModel(models.Model):
    """模型类基类"""
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间', help_text='添加时间')
    create_user_id = models.CharField(max_length=255, null=False, verbose_name='创建人id', help_text='创建人id')
    is_deleted = models.BooleanField(default=False, null=False)

    class Meta:
        abstract = True


class DeviceType(BaseModel):
    """
    设备类型
    code: 类型编码
    name: 类型名称
    desc: 类型描述
    """

    code = models.CharField(max_length=256, null=False)
    name = models.CharField(max_length=256, null=False)
    desc = models.CharField(max_length=256, null=False)


class Device(BaseModel):
    """
    设备
    code: 设备编码
    name: 设备名称
    device_type: 设备类型
    entry_time: 录入时间
    desc: 设备描述

    """
    code = models.CharField(max_length=256, null=False)
    name = models.CharField(max_length=256, null=False)
    device_type =  models.ForeignKey('DeviceType', on_delete=models.CASCADE, null=False) 
    entry_time = models.DateTimeField(null=False)
    desc = models.CharField(max_length=256, null=False)
