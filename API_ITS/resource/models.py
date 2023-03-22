from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin
from django.db import models
import uuid


def resource_files_path(instance,filename):
    return 'resource/{0}/{1}'.format(instance.reference,filename)     
class Resource(models.Model):
    class Meta:
        db_table = 'resource'
    reference = models.UUIDField(default= uuid.uuid4, editable=False)
    model_3d = models.FileField(upload_to=resource_files_path,blank=True,null=True)
    text =  models.CharField(max_length=250,blank=True,null=True)
