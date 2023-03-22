from django.db import models
import uuid

class LevelTest(models.Model):
    
    class Meta:
        db_table = 'levels_test'
    
    name = models.CharField(max_length= 20)
    is_enabled = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now=True)
    updated_date = models.DateTimeField(auto_now=True)