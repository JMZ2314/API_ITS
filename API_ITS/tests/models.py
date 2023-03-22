from django.db import models
import uuid
# from lessons.models import Lesson
from levels_test.models import LevelTest
from types_test.models import TypeTest

def test_image_path(instance,filename):
    return 'images/test/{0}/{1}'.format(instance.reference,filename)
class Test(models.Model):

    class Meta:
        db_table = 'test'

    reference = models.UUIDField(default= uuid.uuid4, editable=False)
    content = models.TextField()
    created_date = models.DateTimeField(auto_now=True)
    updated_date = models.DateTimeField(auto_now=True)
    is_enabled = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    level  = models.ForeignKey( LevelTest, on_delete= models.CASCADE)
    type = models.ForeignKey( TypeTest, on_delete= models.CASCADE)
    image = models.ImageField( upload_to=test_image_path, blank=True, null=True )
    # review_lesson = models.ForeignKey(Lesson, on_delete= models.SET_NULL,blank= True,null=True)