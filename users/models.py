from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    phone = models.CharField(max_length=15, blank=True, null=True)
    occupation = models.CharField(max_length=100, blank=True, null=True)

    def get_all_permissions(self, obj=None):
        # Get the default permissions
        permissions = super().get_all_permissions(obj)

        # Remove the 'app_label.' part of the permission string
        # Example: auth.add_user -> add_user
        permissions = {perm.split('.')[-1]: perm for perm in permissions}
        
        return permissions