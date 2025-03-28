from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings  # Use this to reference the custom user model


class CustomUser(AbstractUser):
    phone = models.CharField(max_length=15, blank=True, null=True)
    occupation = models.CharField(max_length=100, blank=True, null=True)


class UserActivityLog(models.Model):
    ACTION_TYPES = [
        ('LOGIN', 'دخول'),
        ('LOGOUT', 'خروج'),
        ('CREATE', 'انشاء'),
        ('UPDATE', 'تعديل'),
        ('DELETE', 'حذف'),
        ('VIEW', 'عرض'),
        ('DOWNLOAD', 'تحميل'),
        ('CONFIRM', 'تأكيد رسوم'),
        ('REJECT', 'رفض رسوم'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="اسم المستخدم", null=True, blank=True)
    action = models.CharField(max_length=10, choices=ACTION_TYPES, verbose_name="العملية")
    model_name = models.CharField(max_length=100, blank=True, null=True, verbose_name="القسم")
    object_id = models.IntegerField(blank=True, null=True, verbose_name="ID")
    number = models.CharField(max_length=50, null=True, blank=True, verbose_name="رقم المستند")
    ip_address = models.GenericIPAddressField(blank=True, null=True, verbose_name="عنوان IP")
    user_agent = models.TextField(blank=True, null=True, verbose_name="agent")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="الوقت")

    def __str__(self):
        return f"{self.user} {self.action} {self.model_name or 'General'} at {self.timestamp}"