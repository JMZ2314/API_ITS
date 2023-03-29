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


class ProgressView(APIView):

    serializer_class = CourseSerializer
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated,]
    parser_classes = [MultiPartParser,FormParser,JSONParser]

    def get (self,request):
        try:
        
            user_id = request.query_params['user_id']

            courses = Course.objects.all()
            # OBTENER LAS RESPUESTAS CORRECTAS
            answers_correct = Answer.objects.filter(is_correct = True)
            # OBTENER LAS RESPUESTAS DEL USUARIO
            user_answers = User_Answer.objects.filter(user_id= user_id) 
            
            percentage_accumulated  = 0


            for course in courses:
                
                # OBTENER LAS SECCIONES DEL CURSO
                sections_by_course = Section.objects.filter(course_id = course.id)

                
                # SI NO HAY SECCIONES POR CURSO, SALTAR CURSO PARA EVITAR EXCEPCIÓN EN LOS CALCULOS
                quantity_sections_by_course = len(sections_by_course)

                if(quantity_sections_by_course == 0):
                    continue

                # OBTENER LAS RESPUESTAS CORRECTAS POR USUARIO EN CADA UNA DE LAS SECCIONES DEL CURSO
                answer_correcy_by_user = [answer for answer in answers_correct if any( test.id == answer.test_id for test in Test.objects.all()  if any( section.id == test.section_id for section in sections_by_course ) )  and any(answer_user.answer_id == answer.id for answer_user in user_answers) ]


                percentage = round( len( (100*answer_correcy_by_user) ) /  len(sections_by_course) )
                
                percentage_accumulated += percentage

            total_percentage =  round(percentage_accumulated/courses.count(),2)
               

            return Response({'success': True, 'data': total_percentage, 'status:' : status.HTTP_200_OK }, status= status.HTTP_200_OK  )
        except Exception as e:
            return Response({'success': False, 'message': f'{e}', 'status' : status.HTTP_400_BAD_REQUEST } , status= status.HTTP_400_BAD_REQUEST)
    
