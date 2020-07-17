# Generated by Django 3.0.7 on 2020-06-30 00:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resourcemanagement', '0002_device'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestSNMP',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, help_text='添加时间', verbose_name='添加时间')),
                ('create_user_id', models.CharField(help_text='创建人id', max_length=255, verbose_name='创建人id')),
                ('is_deleted', models.BooleanField(default=False)),
                ('sysdate', models.IntegerField(default=0)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]