from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin
from django.db import models
import uuid
from answers.models import Answer
from users.models import User

# class User_Answer(models.Model):
#     class Meta:
#         db_table = 'user_answer'
    
#     user = models.ForeignKey(User, on_delete= models.CASCADE)
#     answer = models.ForeignKey(Answer, on_delete= models.CASCADE)
#     date_answer = models.DateTimeField(auto_now= True)  
