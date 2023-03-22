from django.db import models
import uuid
from users.models import User

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
    previous = models.ForeignKey('self', on_delete= models.DO_NOTHING, blank=True ,null= True)
    image = models.ImageField(upload_to= course_image_path,blank=True,null=True)

    @classmethod
    def get_ordered_courses(cls):

        try:
            # OBTENER TODOS LOS CURSOS
            courses = cls.objects.all()

            # ORDENAR LOS CURSOS DE FORMA SUCESIVA
            courses_ordered = []
            # obtener el primer curso
            first_course = courses.get(previous = None)
            courses_ordered.append(first_course)
            # ordenar los demás cursos
            for item in courses_ordered:
                next_course = courses.get( previous = item.id )
                courses_ordered.append(next_course)
                if(len(courses_ordered) == len(courses)):

                    break
            return courses_ordered
        except Exception as e:
            return []
        
class User_Course(models.Model):
    class Meta:
        db_table = 'user_course'
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    course = models.ForeignKey(Course, on_delete= models.CASCADE)
    approved = models.BooleanField(default= False)