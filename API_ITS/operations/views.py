# from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin
# from django.db import models
# import uuid
# from modules.models import Module
# class Operation(models.Model):

#     class Meta:

#         db_table = 'operations'
    
#     name= models.CharField(max_length=20)
#     module = models.ForeignKey(Module, on_delete= models.CASCADE)
#     created_date = models.DateTimeField(auto_now=True)
#     updated_date = models.DateTimeField(auto_now=True)