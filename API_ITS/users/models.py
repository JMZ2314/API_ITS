
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin
from django.db import models
import uuid
from roles.models import Role
from learning_style.models import LearningStyle

# MANAGERS DE LOS MODELOS
class UserManager(BaseUserManager):

    def create_user(self,email,first_name,last_name, password,learning_style,is_enabled, role):

       
        email = self.normalize_email(email)
        user = self.model(
            email= email, 
            first_name = first_name, 
            last_name = last_name, 
            password = password,  
            is_enabled = is_enabled,
            role = role,
            learning_style = learning_style
            )
        user.set_password(password)
        user.save(using = self.db)

        return user

    def create_superuser(self,email,first_name,last_name, password):
        
        user = self.create_user(email,first_name,last_name, password)
        # ROL DE USUARIO ADMINISTRADOR ID = 2
        user.role = Role.objects.get(id = 2)
         # ESTILO DE APRENDIZAJE NO ASIGNADO ID = 5
        user.learning_style = LearningStyle.objects.get(id = 5)
        user.is_staff = True
        user.is_superuser  = True
        user.save(using = self.db)
        return user
class User(AbstractBaseUser,PermissionsMixin):

    class Meta:
        db_table = 'users'

    first_name = models.CharField(max_length=20 )
    last_name = models.CharField(max_length=20)
    email = models.EmailField(max_length=255, unique=True, blank=False ,error_messages = {'unique': 'El correo ya esta registrado'})
    is_enabled = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now=True)
    updated_date = models.DateTimeField(auto_now=True)
    is_staff = models.BooleanField(default=False)
    is_superuser  = models.BooleanField(default= False)
    learning_style = models.ForeignKey( LearningStyle,on_delete = models.CASCADE,default= 2)
    role = models.ForeignKey( Role, on_delete= models.CASCADE, blank=True ,null= True  ,default= 1 )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name']

    def __str__(self):

        return self.email

