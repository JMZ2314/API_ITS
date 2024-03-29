from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin
from django.db import models
import uuid


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


# MODELOS DE LA BD
class LearningStyle(models.Model):

    class Meta:
        db_table = 'learning_styles'

    name = models.CharField(max_length=35)
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


class LevelTest(models.Model):
    
    class Meta:
        db_table = 'levels_test'
    
    name = models.CharField(max_length= 20)
    is_enabled = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now=True)
    updated_date = models.DateTimeField(auto_now=True)

class TypeTest(models.Model):
    class Meta:
        db_table = 'types_test'
    
    name = models.CharField(max_length= 20)
    is_enabled = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now=True)
    updated_date = models.DateTimeField(auto_now=True)

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



def course_image_path(instance,filename):
    return 'images/courses/{0}/{1}'.format(instance.reference,filename)
class Course(models.Model):
    class Meta:
        db_table = 'courses'

    reference = models.UUIDField(default= uuid.uuid4, editable=False)
    title = models.CharField(max_length=30)
    description = models.TextField()
    created_date = models.DateTimeField(auto_now=True)
    updated_date = models.DateTimeField(auto_now=True)
    is_enabled = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    users = models.ManyToManyField(User, through='user_course')
    previous = models.ForeignKey('self', on_delete= models.DO_NOTHING, null= True)
    image = models.ImageField(upload_to= course_image_path,blank=True,null=True)

class User_Course(models.Model):
    class Meta:
        db_table = 'user_course'
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    course = models.ForeignKey(Course, on_delete= models.CASCADE)
    approved = models.BooleanField(default= False)

class Test(models.Model):

    class Meta:
        db_table = 'test'

    content = models.TextField()
    created_date = models.DateTimeField(auto_now=True)
    updated_date = models.DateTimeField(auto_now=True)
    is_enabled = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    level  = models.ForeignKey( LevelTest, on_delete= models.CASCADE)
    type = models.ForeignKey( TypeTest, on_delete= models.CASCADE)

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
    date_answer = models.DateField(auto_now= True)  


class Section(models.Model):

    class Meta:
        db_table = 'section' 
    
    title = models.CharField(max_length=30)
    course = models.ForeignKey(Course, on_delete= models.CASCADE)
    is_enabled = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    previous = models.ForeignKey('self', on_delete= models.DO_NOTHING, null= True)
    created_date = models.DateTimeField(auto_now=True)
    updated_date = models.DateTimeField(auto_now=True)
    test = models.OneToOneField(Test, on_delete=models.CASCADE)


def lessons_image_path(instance,filename):
    return 'images/lessons/{0}/{1}'.format(instance.reference,filename)

def lessons_resource_path(instance,filename):
    return 'resources/lessons/{0}/{1}'.format(instance.reference,filename)
class Lesson(models.Model):

    class Meta:
        db_table = 'lesson'
    
    reference = models.UUIDField(default= uuid.uuid4, editable=False)
    title = models.CharField(max_length=30)
    content = models.TextField()
    section = models.ForeignKey(Section, on_delete= models.CASCADE)
    previous = models.ForeignKey('self', on_delete= models.DO_NOTHING, null=True)
    image = models.ImageField(upload_to= lessons_image_path,blank=True,null=True)
    created_date = models.DateTimeField(auto_now=True)
    updated_date = models.DateTimeField(auto_now=True)
    is_enabled = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    resource = models.FileField(upload_to=lessons_resource_path,blank=True,null=True)
    objects = models.Manager()

    @classmethod
    def get_ordered_lessons(cls,section):

        try:
            # OBTENER TODAS LAS SECCIONES DE LA SECCIÓN SELECIONADA 
            lessons = cls.objects.filter(section_id = section)

            # ORDENAR LAS LECCIONES DE FORMA SUCESIVA
            lessons_ordered = []
            # obtener la primera lección de la sección y agegarla a una nueva lista
            first_lesson = lessons.get(previous = None)
            lessons_ordered.append(first_lesson)
            # ordenar las demás secciones
            for item in lessons_ordered:
                next_lesson = lessons.get( previous = item.id )
                lessons_ordered.append(next_lesson)
                if(len(lessons_ordered) == len(lessons)):

                    break
            return lessons_ordered
        except Exception as e:
            return []





 



    

      