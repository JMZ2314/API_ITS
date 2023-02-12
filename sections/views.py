from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from core.models import Section,Lesson
from core.serializers import SectionSerializer,LessonSerializer,SimpleEntitySerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination

class SectionView(APIView,PageNumberPagination):

    serializer_class = SectionSerializer
    permission_classes = [IsAuthenticated,]  

    def get (self,request):
        try:

            sections = Section.objects.all()
            sections_lessons = []
            paginated_data = self.paginate_queryset(sections,request)
            serializer = self.serializer_class( paginated_data, many = True)
            
            # PREPARAR UNA NUEVA LISTA QUE TENGA CADA SECCIÓN CON SUS RESPECTIVAS LECCIONES
            for item in serializer.data:
                
                # CONVERTIR A UN DICCIONARIO PARA ACCEDER MÁS FACILMENTE A LOS DATOS
                section_dict = dict(item)
                
                sections_lessons.append({
                    'id' : section_dict.get('id'),
                    'title' : section_dict.get('title'),
                    'is_enabled': section_dict.get('is_enabled'),
                    'is_active': section_dict.get('is_active'),
                    # OBTENER LAS LECCIONES QUE PERTENECEN A ESA SECCIÓN 
                    'lessons':   SimpleEntitySerializer(Lesson.objects.filter(section = section_dict.get('id')), many = True).data
                })

            return Response({'success': True , 'count': sections.count()  , 'data': sections_lessons, 'next':self.get_next_link() , 'previous':self.get_previous_link() , 'status:' : status.HTTP_200_OK }, status= status.HTTP_200_OK  )
        
        except Exception as e:
            # return Response({'success':False, 'data': None})
            return Response({'success': False, 'message': f"{e}", 'status' : status.HTTP_400_BAD_REQUEST } , status= status.HTTP_400_BAD_REQUEST)
