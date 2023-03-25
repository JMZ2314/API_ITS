from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from courses.models import Course
from answers.models import Answer,User_Answer
from users.models import User
from tests.models import Test
from sections.models import Section
from core.serializers import CourseSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import MultiPartParser, FormParser,JSONParser
from rest_framework_simplejwt.authentication import JWTAuthentication


class CourseView(APIView,PageNumberPagination):

    serializer_class = CourseSerializer
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated,]
    parser_classes = [MultiPartParser,FormParser,JSONParser]

    def get (self,request):
        try:
            
            # OBTENER LOS CURSOS ORDENADOS
            courses_ordered = Course.get_ordered_courses()
            paginated_data = self.paginate_queryset(courses_ordered,request)
            serializer = self.serializer_class( paginated_data, many = True)
            courses_with_progress = []

            # OBTENER EL ID DEL USUARIO QUE SE LOGUEO EN LA APP
            user_id = request.query_params['user_id']
            # OBTENER LAS RESPUESTAS CORRECTAS
            answers_correct = Answer.objects.filter(is_correct = True)
            # OBTENER LAS RESPUESTAS DEL USUARIO
            user_answers = User_Answer.objects.filter(user_id= user_id) 
            
            counter_previous = 0
            for course in serializer.data:
                
                # CONVERTIR EL OBJETO CURSO A DICCIONARIO PARA PODER MODIFICARLO
                course_dict = dict(course)

                # OBTENER LAS SECCIONES DEL CURSO
                sections_by_course = Section.objects.filter(course_id = course_dict.get('id'))

                # OBTENER LAS RESPUESTAS CORRECTAS POR USUARIO EN CADA UNA DE LAS SECCIONES DEL CURSO
                # answer_correcy_by_user = [answer for answer in answers_correct if any( section.test_id == answer.test_id for section in sections_by_course) and any(answer_user.answer_id == answer.id for answer_user in user_answers) ]
                answer_correcy_by_user = [answer for answer in answers_correct if any( test.id == answer.test_id for test in Test.objects.all()  if any( section.id == test.section_id for section in sections_by_course ) )  and any(answer_user.answer_id == answer.id for answer_user in user_answers) ]

                
                courses_with_progress.append({
                    #  'id':  course_dict.get('id') ,
                    # 'title': course_dict.get('title'),
                    # 'description': course_dict.get('description'),
                    # 'is_enabled': course_dict.get('is_enabled'),
                    # 'previous': course_dict.get('previous'),
                    # 'image': course_dict.get('image'),
                    # 'reference': 'bb7bec80-246f-4731-b4ae-dcb1cf1f490e',
                    # 'is_active': true
                    **course_dict,
                    'previous': None if counter_previous == 0 else courses_with_progress[counter_previous -1],
                    'progress_user':{
                        'percentage': round( len( (100*answer_correcy_by_user) ) /  len(sections_by_course) ) ,
                        'sections_completed' : len(answer_correcy_by_user),
                        'sections_missing': len(sections_by_course) - len(answer_correcy_by_user),
                        'total_sections': len(sections_by_course)
                    }
                })

                counter_previous = counter_previous + 1


            return Response({'success': True , 'count': len(courses_ordered)  , 'data': courses_with_progress, 'next':self.get_next_link() , 'previous':self.get_previous_link() , 'status:' : status.HTTP_200_OK }, status= status.HTTP_200_OK  )
        except Exception as e:
            return Response({'success': False, 'message': f'{e}', 'status' : status.HTTP_400_BAD_REQUEST } , status= status.HTTP_400_BAD_REQUEST)
    
    def post(self, request):
        
        try:

            serializer = self.serializer_class(data=request.data)

            if(serializer.is_valid()):
                course_created =   self.serializer_class(serializer.save()).data
                return Response({'success': True, 'message': 'El curso fue creado exitosamente', 'data': course_created , 'status' : status.HTTP_200_OK }, status= status.HTTP_200_OK)
            else:
                return Response({'success': False, 'messages':  serializer.errors , 'status' : status.HTTP_400_BAD_REQUEST }, status= status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'success': False, 'message': f'Ocurrió un error al crear el curso: {e}', 'status' : status.HTTP_400_BAD_REQUEST }, status= status.HTTP_400_BAD_REQUEST)
