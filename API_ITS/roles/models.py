from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin
from django.db import models
import uuid
from  operations.models import Operation

class Role(models.Model):

    class Meta:
        db_table = 'roles'


    name= models.CharField(max_length=20)
    operation = models.ManyToManyField(Operation)
    created_date = models.DateTimeField(auto_now=True)
    updated_date = models.DateTimeField(auto_now=True)