from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin
from django.db import models


# MANAGERS DE LOS MODELOS
class UserManager(BaseUserManager):

    def create_user(self,email,first_name,last_name, password):

        email = self.normalize_email(email)
        user = self.model(email= email, first_name = first_name, last_name = last_name, password = password)
        user.set_password(password)
        user.save(using = self.db)

        return user

    def create_superuser(self,email,first_name,last_name, password):
        
        user = self.create_user(email,first_name,last_name, password)
        user.role = Role.objects.get(id = 2)
        user.learning_style = LearningStyle.objects.get(id = 5)
        user.is_staff = True
        user.is_superuser  = True
        user.save(using = self.db)
        return user


# MODELOS DE LA BD
class LearningStyle(models.Model):

    class Meta:
        db_table = 'learning_styles'

    name = models.CharField(max_length=20)
    created_date = models.DateTimeField(auto_now=True)
    updated_date = models.DateTimeField(auto_now=True)
    is_enabled = models.BooleanField(default=True)

class Module(models.Model):

    class Meta:
        db_table = 'modules'

    name= models.CharField(max_length=20)
    created_date = models.DateTimeField(auto_now=True)
    updated_date = models.DateTimeField(auto_now=True)

class Operation(models.Model):

    class Meta:

        db_table = 'operations'
    
    name= models.CharField(max_length=20)
    module = models.ForeignKey(Module, on_delete= models.CASCADE)
    created_date = models.DateTimeField(auto_now=True)
    updated_date = models.DateTimeField(auto_now=True)


class Role(models.Model):

    class Meta:
        db_table = 'roles'


    name= models.CharField(max_length=20)
    operation = models.ManyToManyField(Operation)
    created_date = models.DateTimeField(auto_now=True)
    updated_date = models.DateTimeField(auto_now=True)

class User(AbstractBaseUser,PermissionsMixin):

    class Meta:
        db_table = 'users'

    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField(max_length=255, unique=True)
    is_enabled = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now=True)
    updated_date = models.DateTimeField(auto_now=True)
    is_staff = models.BooleanField(default=False)
    is_superuser  = models.BooleanField(default= False)
    learning_style = models.ForeignKey( LearningStyle, on_delete = models.CASCADE, default= 2)
    role = models.ForeignKey( Role, on_delete= models.CASCADE, default= 1 )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name']

    def __str__(self):

        return self.email