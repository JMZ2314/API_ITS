from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin
from django.db import models
import uuid
from tests.models import Test
from users.models import User


class Answer(models.Model):

    class Meta:
        db_table = 'answer'
    
    description = models.CharField(max_length= 30)
    is_correct = models.BooleanField(default= False)
    created_date = models.DateTimeField(auto_now=True)
    updated_date = models.DateTimeField(auto_now=True)
    is_enabled = models.BooleanField(default=True)
    test = models.ForeignKey(Test, on_delete= models.CASCADE)
    users = models.ManyToManyField(User, through='user_answer')


class User_Answer(models.Model):
    class Meta:
        db_table = 'user_answer'
    
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete= models.CASCADE)
    date_answer = models.DateTimeField(auto_now= True)  
    
