# Generated by Django 3.0.7 on 2020-06-30 01:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resourcemanagement', '0003_testsnmp'),
    ]

    operations = [
        migrations.AddField(
            model_name='testsnmp',
            name='oid',
            field=models.CharField(default='', max_length=256),
        ),
    ]