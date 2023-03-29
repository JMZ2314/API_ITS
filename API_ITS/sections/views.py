from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from sections.models import Section
from lessons.models import Lesson
from tests.models import Test
from answers.models import Answer,User_Answer
from core.serializers import SectionSerializer,SimpleEntitySerializer,AnswerUserSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.parsers import JSONParser,FormParser,MultiPartParser

class SectionView(APIView,PageNumberPagination):

    serializer_class = SectionSerializer
    parser_classes = [JSONParser,FormParser,MultiPartParser]
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated,]  

    def get (self,request):
        try:
            

            # OBTENER LOS QUERY PARAMS
            course_id = request.query_params.get('course')
            user_id = request.query_params.get('user_id')

            list_for_user = (course_id is not None ) and (user_id is not None) 

            if(list_for_user):
                sections_ordered = Section.get_ordered_sections(course_id = course_id)  
                    
                sections_lessons = []
                paginated_data = self.paginate_queryset(sections_ordered,request)
                serializer = self.serializer_class( paginated_data, many = True)
            
                
                counter_previous  = 0
                # PREPARAR UNA NUEVA LISTA QUE TENGA CADA SECCIÓN CON SUS RESPECTIVAS LECCIONES
                for item in serializer.data:
                    
                    # CONVERTIR A UN DICCIONARIO PARA ACCEDER MÁS FACILMENTE A LOS DATOS
                    section_dict = dict(item)
                    lessons_by_section  = Lesson.get_ordered_lessons(section=section_dict.get('id'))

                    #OBTENER LA ÚLTIMA RESPUESTA DEL USUARIO LOGUEADO PARA LA PUEBA DE LA SECCIÓN ACTUAL 
                    last_user_answer = next(iter( sorted( [answer_user for answer_user in User_Answer.objects.filter(user_id = user_id) if any( answer.id == answer_user.answer_id for answer in Answer.objects.all() if any( test.id  == answer.test_id for test in Test.objects.filter(section_id = section_dict.get('id') ) )) ], key= lambda x:x.date_answer, reverse=True)),None)
                    # OBTENER EL VALOR DE ESA RESPUESTA, ES DECIR, SI ES CORRECTA O NO (DE NO HABER UNA RESPUESTA DEL USUARIO PARA EL TEST SE ASIGNA FALSO) 
                    answer_value = False if last_user_answer is None else Answer.objects.get(id = last_user_answer.answer_id).is_correct


                    sections_lessons.append({
                        **section_dict,
                        'previous': None if counter_previous == 0 else sections_lessons[counter_previous - 1],
                        # OBTENER LAS LECCIONES QUE PERTENECEN A ESA SECCIÓN 
                        'lessons':   SimpleEntitySerializer(lessons_by_section, many = True).data,
                        'completed': answer_value
                    })
                
                    counter_previous = counter_previous + 1
                return Response({'success': True , 'count': len(sections_ordered)  , 'data': sections_lessons, 'next':self.get_next_link() , 'previous':self.get_previous_link() , 'status:' : status.HTTP_200_OK }, status= status.HTTP_200_OK  )
                
            else:

                filter_by_course = course_id is not None 
                if(filter_by_course):
                    sections_ordered = Section.get_ordered_sections(course_id = course_id) 
                    paginated_data = self.paginate_queryset(sections_ordered,request)
                    serializer = self.serializer_class( paginated_data, many = True)
                    return Response({'success': True , 'count': len(sections_ordered)  , 'data': serializer.data, 'next':self.get_next_link() , 'previous':self.get_previous_link() , 'status:' : status.HTTP_200_OK }, status= status.HTTP_200_OK  )
                else:
                    sections = Section.objects.all()
                    paginated_data = self.paginate_queryset(sections,request)
                    serializer = self.serializer_class( paginated_data, many = True)
                    return Response({'success': True , 'count': sections.count()  , 'data': serializer.data, 'next':self.get_next_link() , 'previous':self.get_previous_link() , 'status:' : status.HTTP_200_OK }, status= status.HTTP_200_OK  )
        
        except Exception as e:
            # return Response({'success':False, 'data': None})
            return Response({'success': False, 'message': f"{e}", 'status' : status.HTTP_400_BAD_REQUEST } , status= status.HTTP_400_BAD_REQUEST)
        

    def post(self, request):
        
        try:
            serializer = self.serializer_class(data=request.data)

            if(serializer.is_valid()):
                section_created =   self.serializer_class(serializer.save()).data
                return Response({'success': True, 'message': "La sección fue creada exitosamente", 'data': section_created , 'status' : status.HTTP_200_OK }, status= status.HTTP_200_OK)
            else:
                return Response({'success': False, 'messages':  serializer.errors , 'status' : status.HTTP_400_BAD_REQUEST }, status= status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'success': False, 'message': f"Ocurrió un error al crear la sección: {e}", 'status' : status.HTTP_400_BAD_REQUEST }, status= status.HTTP_400_BAD_REQUEST)
