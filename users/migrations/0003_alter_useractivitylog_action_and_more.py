# Generated by Django 5.1.4 on 2025-02-27 08:12

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_useractivitylog'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useractivitylog',
            name='action',
            field=models.CharField(choices=[('LOGIN', 'Login'), ('LOGOUT', 'Logout'), ('CREATE', 'Create'), ('UPDATE', 'Update'), ('DELETE', 'Delete'), ('VIEW', 'View'), ('DOWNLOAD', 'Download')], max_length=10, verbose_name='العملية'),
        ),
        migrations.AlterField(
            model_name='useractivitylog',
            name='ip_address',
            field=models.GenericIPAddressField(blank=True, null=True, verbose_name='عنوان IP'),
        ),
        migrations.AlterField(
            model_name='useractivitylog',
            name='model_name',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='القسم'),
        ),
        migrations.AlterField(
            model_name='useractivitylog',
            name='object_id',
            field=models.IntegerField(blank=True, null=True, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='useractivitylog',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, verbose_name='الوقت'),
        ),
        migrations.AlterField(
            model_name='useractivitylog',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='اسم المستخدم'),
        ),
        migrations.AlterField(
            model_name='useractivitylog',
            name='user_agent',
            field=models.TextField(blank=True, null=True, verbose_name='agent'),
        ),
    ]
