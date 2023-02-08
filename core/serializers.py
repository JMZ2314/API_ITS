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

        
class UserSerializer(serializers.ModelSerializer):
    role = RoleSerializer()
    learning_style = LearningStyleSerializer()
    class Meta:
        model= models.User
        fields = ['id','first_name','last_name','email','role','learning_style','is_superuser']
        depth = 1