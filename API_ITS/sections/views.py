from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from core.models import Section,Lesson
from core.serializers import SectionSerializer,LessonSerializer,SimpleEntitySerializer
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

            if(course_id is not None):
                sections_ordered = Section.objects.filter(course_id = course_id)
            else:
                sections_ordered = Section.get_ordered_sections()
                
            sections_lessons = []
            paginated_data = self.paginate_queryset(sections_ordered,request)
            serializer = self.serializer_class( paginated_data, many = True)
            

            # PREPARAR UNA NUEVA LISTA QUE TENGA CADA SECCIÓN CON SUS RESPECTIVAS LECCIONES
            for item in serializer.data:
                
                # CONVERTIR A UN DICCIONARIO PARA ACCEDER MÁS FACILMENTE A LOS DATOS
                section_dict = dict(item)
                lessons_by_section  = Lesson.get_ordered_lessons(section=section_dict.get('id'))
                
                sections_lessons.append({
                    'id' : section_dict.get('id'),
                    'title' : section_dict.get('title'),
                    'is_enabled': section_dict.get('is_enabled'),
                    'is_active': section_dict.get('is_active'),
                    'course': section_dict.get('course'),
                    # OBTENER LAS LECCIONES QUE PERTENECEN A ESA SECCIÓN 
                    'lessons':   SimpleEntitySerializer(lessons_by_section, many = True).data
                })

            return Response({'success': True , 'count': len(sections_ordered)  , 'data': sections_lessons, 'next':self.get_next_link() , 'previous':self.get_previous_link() , 'status:' : status.HTTP_200_OK }, status= status.HTTP_200_OK  )
        
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
