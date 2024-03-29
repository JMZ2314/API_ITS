

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

    

class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model= models.Section
        fields = ['id','title','is_enabled','previous','course','test','is_active']
     
class LessonSerializer(serializers.ModelSerializer):
    section = SectionSerializer()
    class Meta:
        model = models.Lesson
        fields = ['id','title','content','is_enabled','is_active','image','previous','section']
        depth = 1
class TestSerializer(serializers.ModelSerializer):

    level = LevelTestSerializer()
    type = TypeTestSerializer()
    class Meta:
        model= models.Test
        fields = ['id','content','level','type','is_active','is_enabled']
        depth = 1
        
class UserSerializer(serializers.ModelSerializer):
    

    # CAMPOS DE SOLO LECTURA
    role = RoleSerializer(read_only = True)
    learning_style = LearningStyleSerializer(read_only = True)

    # CAMPOS DE SOLO ESCRITURA
    learning_style_id = serializers.IntegerField(write_only = True)
    role_id = serializers.IntegerField(write_only = True)
    confirm_password = serializers.CharField(max_length =255,write_only= True,error_messages = {'blank': 'El campo confirmar contraseña no puede estar en blanco'})


    class Meta:
        model= models.User
        fields = ['id','first_name','last_name','email','password','confirm_password','role','learning_style','is_superuser','is_enabled','learning_style_id','role_id']
        depth = 1
        extra_kwargs = {
            'password': {'write_only': True},
            'first_name': {'error_messages': {'blank': 'El campo nombre no puede estar en blanco'} },
            'last_name': {'error_messages': {'blank': 'El campo apellido no puede estar en blanco'} },
            'password': {'error_messages': {'blank': 'El campo contraseña no puede estar en blanco'} },
            'email': {'error_messages': {'blank': 'El campo correo no puede estar en blanco'} },
        }

    # def validate_password(self,value):
    #     password_length = len(value)

    #     if(password_length < 8):
    #         raise serializers.ValidationError("La contraseña debe tener mínimo 8 caracteres")

    #     return value
    
    def validate(self,data):

        password_length = len(data['password'])

        if(password_length < 8):
            raise serializers.ValidationError({ 'password': 'La contraseña debe tener mínimo 8 caracteres'  })

        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({ 'verify': 'Las contraseñas no coinciden' })
        return data
    

    def create(self, validated_data):


        # OBTENER LOS OBJETOS DE ROL Y EL ESTILO DE APRENDIZAJE
        learning_style =  models.LearningStyle.objects.get(id = validated_data["learning_style_id"])
        role =  models.Role.objects.get(id = validated_data["role_id"])
          
        return models.User.objects.create_user(
            email = validated_data["email"],
            first_name = validated_data["first_name"],
            last_name = validated_data["last_name"],
            password = validated_data["password"],
            learning_style = learning_style,
            is_enabled = validated_data["is_enabled"],
            role = role
        )
        

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Answer
        fields = ['id','description','is_correct','is_enabled','test']

class SimpleEntitySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()



