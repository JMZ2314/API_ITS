from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin
from django.db import models
import uuid

class Module(models.Model):

    class Meta:
        db_table = 'modules'

    name= models.CharField(max_length=20)
    created_date = models.DateTimeField(auto_now=True)
    updated_date = models.DateTimeField(auto_now=True)