from django.db import models
import uuid
# from tests.models import Test
from courses.models import Course

class Section(models.Model):

    class Meta:
        db_table = 'section' 
    
    title = models.CharField(max_length=50)
    course = models.ForeignKey(Course, on_delete= models.CASCADE,blank=True,null=True)
    is_enabled = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    previous = models.ForeignKey('self', on_delete= models.DO_NOTHING, null= True, blank=True)
    created_date = models.DateTimeField(auto_now=True)
    updated_date = models.DateTimeField(auto_now=True)
    # test = models.ForeignKey(Test, on_delete=models.CASCADE)

    @classmethod
    def get_ordered_sections(cls,course_id):

        try:
            # OBTENER TODAS LAS SECCIONES DEL CURSO SELECCIONADO
            sections = cls.objects.filter(course_id = course_id)

            # ORDENAR LAS SECCIONES DE FORMA SUCESIVA
            sections_ordered = []
            # obtener la primera sección del curso y agegarla a una nueva lista
            first_section = sections.get(previous = None)
            sections_ordered.append(first_section)
            # ordenar las demás secciones

            if(len(sections) > 1):
                for item in sections_ordered:
                    next_course = sections.get( previous = item.id )
                    sections_ordered.append(next_course)
                    if(len(sections_ordered) == len(sections)):
                        break
            return sections_ordered
        except Exception as e:
            return []