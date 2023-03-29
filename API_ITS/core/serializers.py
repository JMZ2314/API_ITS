
from rest_framework import serializers
from roles.models import Role
from learning_style.models import LearningStyle
from  types_test.models import TypeTest
from levels_test.models import LevelTest
from tests.models import Test
from answers.models import Answer,User_Answer
from courses.models import Course
from sections.models import Section
from lessons.models import Lesson
from modules.models import Module
from operations.models import Operation
from resource.models import Resource
from users.models import User
from suggestions.models import Suggestions

class RoleSerializer(serializers.ModelSerializer):

    class Meta:
        model= Role
        fields= ['id','name']

class LearningStyleSerializer(serializers.ModelSerializer):

    class Meta:
        model= LearningStyle
        fields= ['id','name']

class TypeTestSerializer(serializers.ModelSerializer):

    class Meta:
        model= TypeTest
        fields= ['id','name']

class LevelTestSerializer(serializers.ModelSerializer):

    class Meta:
        model= LevelTest
        fields= ['id','name']
        

def file_null_validator(file):
    if file is None:
            raise serializers.ValidationError('Debe seleccionar un archivo para continuar')

class CourseSerializer(serializers.ModelSerializer):

    image = serializers.ImageField(required = False)
    previous_id = serializers.IntegerField(write_only = True,required=False,allow_null=True)
    class Meta:
        model= Course
        fields = ['id','title','description','is_enabled','previous','previous_id','image','reference','is_active']
        extra_kwargs = {
            'previous_id': {'error_messages': {'blank': 'El curso previo no puede estar en blanco'} },
            'title': {'error_messages': {'blank': 'El título del curso no puede estar en blanco'} },
            'description': {'error_messages': {'blank': 'La descripción del curso no puede estar en blanco'} },
        }

    def create(self, validated_data):
        
        course_created = Course.objects.create(**validated_data)

        # BUSCAR CURSOS QUE TENGAN EL MISMO ANTERIOR DEL QUE SE CREÓ
        courses_with_same_previous  = [course for course in Course.objects.all() if ( course.previous == course_created.previous and course.id != course_created.id )]

        if( len(courses_with_same_previous) != 0 ):
            # DE EXISTIR UNO SE ACTUALIZA SU PREVIO AL NUEVO CREADO
            course_for_update = courses_with_same_previous[0]
            course_for_update.previous = course_created
            course_for_update.save()

        return course_created

    def update(self, instance, validated_data):
        
        # OBTENER EL CURSO PREVIO
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.is_enabled = validated_data.get('is_enabled', instance.is_enabled)
        instance.image = validated_data.get('image',instance.image)

        # VERIFICAR SI ESTOY MOVIENDO EL ÚLTIMO
            # asignar el nuevo previo al actualizado
            # asignar como previo el actualizado a aquel que tenia como previo el nuevo previo

        # SI ES UNO DE EN MEDIO
            # buscar aquel que tiene como previo al actual y asignarle como previo, el previo del actual
            # asignar el nuevo previo al acutal
            # buscar aquel que tenia asignado el nuevo previo y asignarle como previo el actual (si existe)

        new_previous = Course.objects.get(id = validated_data.get('previous_id'))
        courses_with_next_instance = [course for course in Course.objects.all() if ( course.previous == instance )]
        is_last_course = len(courses_with_next_instance)  == 0
        if(is_last_course):
            instance.previous = validated_data.get('previous', new_previous)
            instance.save()
        else:
            courses_with_next_instance[0].previous = instance.previous
            courses_with_next_instance[0].save()
            instance.previous = validated_data.get('previous', new_previous)
            instance.save()

        courses_with_new_previous =  [course for course in Course.objects.all() if ( course.previous_id == validated_data.get('previous_id') and course.id != instance.id )]
        if(len(courses_with_new_previous) > 0):
                courses_with_new_previous[0].previous = instance
                courses_with_new_previous[0].save()

















        
    

        # # SI EL NUEVO PREVIO ES NONE ES PORQUE LO COLOCARA COMO EL NUEVO PRIMERO
        # if(new_id_previous is not None):
        #     n = Course.objects.get(id = new_id_previous)
        #     instance.previous = validated_data.get('previous', n)
        # else:
        #     instance.previous = validated_data.get('previous', None)

        # instance.image = validated_data.get('image', instance.image)
        # instance.save()

        # # BUSCAR CURSOS QUE TENGAN EL MISMO ANTERIOR DEL QUE SE CREÓ
        # courses_with_same_previous  = [course for course in Course.objects.all() if ( course.previous == instance.previous and course.id != instance.id )]

        # if( len(courses_with_same_previous) != 0 ):
        #     # DE EXISTIR UNO SE ACTUALIZA SU PREVIO AL NUEVO CREADO
        #     course_for_update = courses_with_same_previous[0]
        #     course_for_update.previous = instance
        #     course_for_update.save()

            

        return instance
    

    

    

class TestSerializer(serializers.ModelSerializer):

    # CAMPOS DE SOLO ESCRITURA
    level_id = serializers.IntegerField(write_only = True)
    type_id = serializers.IntegerField(write_only = True)
    class Meta:
        model= Test
        fields = ['id','content','level','type','is_active','is_enabled','image','level_id','type_id','image','review_lesson']
        depth = 1

class SectionSerializer(serializers.ModelSerializer):

    # CAMPOS DE SOLO ESCRITURA
    course_id = serializers.IntegerField(write_only = True)
    previous_id = serializers.IntegerField(write_only = True,required=False,allow_null=True)
    course_id = serializers.IntegerField(write_only = True,required=False,allow_null=True)
    class Meta:
        model= Section
        fields = ['id','title','is_enabled','previous','course','is_active','course_id','previous_id']

        extra_kwargs = {
            'title': {'error_messages': {'blank': 'El título de la sección no puede estar en blanco'} },
        }

    def validate_course_id(self,value):
        if value == -1:
            raise serializers.ValidationError("Debe seleccionar un curso para la sección")
        return value

    def create(self, validated_data):
        
        section_created = Section.objects.create(**validated_data)

        # BUSCAR LAS SECCIONES QUE TENGAN EL MISMO ANTERIOR DEL QUE SE CREÓ
        sections_with_same_previous  = [section for section in Section.objects.all() if ( section.previous == section_created.previous and section.id != section_created.id )]

        if( len(sections_with_same_previous) != 0 ):
            # DE EXISTIR UNO SE ACTUALIZA SU PREVIO AL NUEVO CREADO
            section_for_update = sections_with_same_previous[0]
            section_for_update.previous = section_created
            section_for_update.save()

        return section_created
    def update(self, instance, validated_data):
        
        # OBTENER EL CURSO PREVIO
        new_course = Section.objects.get(id = validated_data.get('course_id'))
        instance.course = validated_data.get('course', new_course)
        instance.title = validated_data.get('title', instance.title)
        instance.is_enabled = validated_data.get('is_enabled', instance.is_enabled)
        instance.course = validated_data.get('image',instance.image)

        # VERIFICAR SI ESTOY MOVIENDO EL ÚLTIMO
            # asignar el nuevo previo al actualizado
            # asignar como previo el actualizado a aquel que tenia como previo el nuevo previo

        # SI ES UNO DE EN MEDIO
            # buscar aquel que tiene como previo al actual y asignarle como previo, el previo del actual
            # asignar el nuevo previo al acutal
            # buscar aquel que tenia asignado el nuevo previo y asignarle como previo el actual (si existe)

        new_previous = Section.objects.get(id = validated_data.get('previous_id'))
        sections_with_next_instance = [section for section in Course.objects.all() if ( section.previous == instance )]
        is_last_section = len(sections_with_next_instance)  == 0
        if(is_last_section):
            instance.previous = validated_data.get('previous', new_previous)
            instance.save()
        else:
            sections_with_next_instance[0].previous = instance.previous
            sections_with_next_instance[0].save()
            instance.previous = validated_data.get('previous', new_previous)
            instance.save()

        sections_with_new_previous =  [section for section in Section.objects.all() if ( section.previous_id == validated_data.get('previous_id') and section.id != instance.id )]
        if(len(sections_with_new_previous) > 0):
                sections_with_new_previous[0].previous = instance
                sections_with_new_previous[0].save()

class LessonSerializerLevel1(serializers.ModelSerializer):
    # CAMPOS DE SOLO ESCRITURA
    section_id = serializers.IntegerField(write_only = True)
    previous_id = serializers.IntegerField(write_only = True,allow_null= True)
    resource_id = serializers.IntegerField(write_only = True,required = False,allow_null = True)
    section = SectionSerializer(read_only = True)
    
    class Meta:
        model = Lesson
        fields = ['id','title','content','is_enabled','is_active','image','previous','section','section_id','previous_id','resource_id','resource']
class LessonSerializer(serializers.ModelSerializer):
    # CAMPOS DE SOLO ESCRITURA
    section_id = serializers.IntegerField(write_only = True)
    previous_id = serializers.IntegerField(write_only = True,allow_null= True)
    resource_id = serializers.IntegerField(write_only = True,required = False,allow_null = True)
    section = SectionSerializer(read_only = True)
    previous = LessonSerializerLevel1(read_only = True)
    
    class Meta:
        model = Lesson
        fields = ['id','title','content','is_enabled','is_active','image','previous','section','section_id','previous_id','resource_id','resource']

class ResourceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Resource
        fields = ['id','model_3d','text']


        
class UserSerializer(serializers.ModelSerializer):
    

    # CAMPOS DE SOLO LECTURA
    role = RoleSerializer(read_only = True)
    learning_style = LearningStyleSerializer(read_only = True)

    # CAMPOS DE SOLO ESCRITURA
    learning_style_id = serializers.IntegerField(write_only = True)
    role_id = serializers.IntegerField(write_only = True)
    confirm_password = serializers.CharField(max_length =255,write_only= True,error_messages = {'blank': 'El campo confirmar contraseña no puede estar en blanco'})


    class Meta:
        model= User
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
        learning_style =  LearningStyle.objects.get(id = validated_data["learning_style_id"])
        role =  Role.objects.get(id = validated_data["role_id"])
          
        return User.objects.create_user(
            email = validated_data["email"],
            first_name = validated_data["first_name"],
            last_name = validated_data["last_name"],
            password = validated_data["password"],
            learning_style = learning_style,
            is_enabled = validated_data["is_enabled"],
            role = role
        )
        

class AnswerSerializer(serializers.ModelSerializer):

    # CAMPOS DE SOLO ESCRITURA
    test_id = serializers.IntegerField(write_only = True)
    class Meta:
        model = Answer
        fields = ['id','description','is_correct','is_enabled','test','test_id']
        depth = 1

class SimpleEntitySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()


class AnswerUserSerializer(serializers.ModelSerializer):

    user_id = serializers.IntegerField(write_only=True)
    answer_id = serializers.IntegerField(write_only=True)
    class Meta:
        model = User_Answer
        fields = ['id','user','date_answer','answer','user_id','answer_id']
        depth = 1


class SuggestionsSerializer(serializers.ModelSerializer):

    user_id = serializers.IntegerField(write_only = True)
    course_id = serializers.IntegerField(write_only = True)
    user = UserSerializer(read_only = True)
    course = CourseSerializer(read_only= True)


    def validate_course_id(self,value):
        if value == -1:
            raise serializers.ValidationError("Debe seleccionar un curso para la sugerencia")
        return value

    class Meta:
        model = Suggestions
        fields = ['id','user','course','date','user_id','course_id','content','is_enabled']
        extra_kwargs = {
            'content': {'error_messages': {'blank': 'El contenido de la sugerencia no puede estar en blanco'} },
        }
         

