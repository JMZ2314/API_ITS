from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from core.models import Lesson
from core.serializers import LessonSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.parsers import MultiPartParser,FormParser,JSONParser

class LessonView(APIView,PageNumberPagination):

    serializer_class = LessonSerializer
    parser_classes = [MultiPartParser,FormParser,JSONParser]
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated,]  

    def get (self,request):
        try:

             # OBTENER LOS QUERY PARAMS
            section_id = request.query_params.get('section')
            
            if(section_id is None):
                return Response({'success': False, 'message': 'Debe seleccionar la sección a la que pertenecen las lecciones', 'status' : status.HTTP_400_BAD_REQUEST } , status= status.HTTP_400_BAD_REQUEST)



            lessons_ordered   = Lesson.get_ordered_lessons(section=section_id)

            paginated_data = self.paginate_queryset(lessons_ordered,request)            
        
        
            serializer = self.serializer_class( paginated_data, many = True)

            return Response({'success': True , 'count': len(lessons_ordered) , 'data': serializer.data, 'next':self.get_next_link() , 'previous':self.get_previous_link() , 'status:' : status.HTTP_200_OK }, status= status.HTTP_200_OK  )
        except Exception as e:
            return Response({'success': False, 'message': f"{e}", 'status' : status.HTTP_400_BAD_REQUEST } , status= status.HTTP_400_BAD_REQUEST)
    

    def post(self,request):
        try:
            serializer = self.serializer_class(data=request.data)

            if(serializer.is_valid()):
                lesson_created =   self.serializer_class(serializer.save()).data
                return Response({'success': True, 'message': "La lección fue creada exitosamente", 'data': lesson_created , 'status' : status.HTTP_200_OK }, status= status.HTTP_200_OK)
            else:
                return Response({'success': False, 'messages':  serializer.errors , 'status' : status.HTTP_400_BAD_REQUEST }, status= status.HTTP_400_BAD_REQUEST)
        except Exception as e:
                return Response({'success': False, 'message': f"Ocurrió un error al crear la lección: {e}", 'status' : status.HTTP_400_BAD_REQUEST }, status= status.HTTP_400_BAD_REQUEST)

