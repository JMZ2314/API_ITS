from rest_framework import serializers
from core import models


class RoleSerializer(serializers.ModelSerializer):

    class Meta:
        model= models.Role
        fields= ['id','name']

class LearningStyleSerializer(serializers.ModelSerializer):

    class Meta:
        model= models.LearningStyle
        fields= ['id','name']

class TypeTestSerializer(serializers.ModelSerializer):

    class Meta:
        model= models.TypeTest
        fields= ['id','name']

class LevelTestSerializer(serializers.ModelSerializer):

    class Meta:
        model= models.LevelTest
        fields= ['id','name']

class CourseSerializer(serializers.ModelSerializer):

    image = serializers.ImageField(required = False)
    # previous = 'self'
    class Meta:
        model= models.Course
        fields = ['id','title','description','is_enabled','previous','image','reference']

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Lesson
        fields = ['id','title','content','is_enabled','is_active']
    

class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model= models.Section
        fields = ['id','title','is_enabled','previous','course','test','is_active']
     
class TestSerializer(serializers.ModelSerializer):

    level = LevelTestSerializer()
    type = TypeTestSerializer()
    class Meta:
        model= models.Test
        fields = ['id','content','level','type','is_active','is_enabled']
        depth = 1
        
class UserSerializer(serializers.ModelSerializer):
    role = RoleSerializer()
    learning_style = LearningStyleSerializer()
    class Meta:
        model= models.User
        fields = ['id','first_name','last_name','email','role','learning_style','is_superuser','is_enabled']
        depth = 1
class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Answer
        fields = ['id','description','is_correct','is_enabled','test']

class SimpleEntitySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()



