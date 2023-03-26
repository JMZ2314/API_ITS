from django.db import models
from users.models import User
from courses.models import Course

def test_image_path(instance,filename):
    return 'images/test/{0}/{1}'.format(instance.reference,filename)

class Suggestions(models.Model):

    class Meta:
        db_table = 'suggestions'

    content = models.TextField(blank=False)
    user = models.ForeignKey(User,on_delete=models.SET_NULL,blank= True,null=True)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, blank= True, null= True)
    attended = models.BooleanField(default= False, null= False, blank= False)
    date = models.DateTimeField(auto_now=True)