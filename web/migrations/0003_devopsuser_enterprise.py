# Generated by Django 3.0.7 on 2020-06-18 09:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0002_devopsuser_mobile'),
    ]

    operations = [
        migrations.AddField(
            model_name='devopsuser',
            name='enterprise',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
