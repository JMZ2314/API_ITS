from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin
from django.db import models
import uuid
from resource.models import Resource
from sections.models import Section

def lessons_image_path(instance,filename):
    return 'images/lessons/{0}/{1}'.format(instance.reference,filename)

class Lesson(models.Model):

    class Meta:
        db_table = 'lesson'
    
    reference = models.UUIDField(default= uuid.uuid4, editable=False)
    title = models.CharField(max_length=50)
    content = models.TextField()
    section = models.ForeignKey(Section, on_delete= models.CASCADE)
    previous = models.ForeignKey('self', on_delete= models.DO_NOTHING, blank=True ,null=True)
    image = models.ImageField(upload_to= lessons_image_path,blank=True,null=True)
    created_date = models.DateTimeField(auto_now=True)
    updated_date = models.DateTimeField(auto_now=True)
    is_enabled = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    resource = models.ForeignKey(Resource,on_delete=models.SET_NULL,blank=True,null=True)
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