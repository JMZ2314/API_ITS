from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from core.models import Course
from core.serializers import CourseSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import MultiPartParser, FormParser,JSONParser
from rest_framework_simplejwt.authentication import JWTAuthentication


class CourseView(APIView,PageNumberPagination):

    serializer_class = CourseSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated,]
    parser_classes = [MultiPartParser,FormParser,JSONParser]

    def get (self,request):
        try:
            courses = Course.objects.all()
            paginated_data = self.paginate_queryset(courses,request)
            serializer = self.serializer_class( paginated_data, many = True)

            return Response({'success': True , 'count': courses.count()  , 'data': serializer.data, 'next':self.get_next_link() , 'previous':self.get_previous_link() , 'status:' : status.HTTP_200_OK }, status= status.HTTP_200_OK  )
        except Exception as e:
            return Response({'success': False, 'message': f"{e}", 'status' : status.HTTP_400_BAD_REQUEST } , status= status.HTTP_400_BAD_REQUEST)
    
    def post(self, request):
        
        try:

            serializer = self.serializer_class(data=request.data)

            if(serializer.is_valid()):
                course_created =   self.serializer_class(serializer.save()).data
                return Response({'success': True, 'message': "El curso fue creado exitosamente", 'data': course_created , 'status' : status.HTTP_200_OK }, status= status.HTTP_200_OK)
            else:
                return Response({'success': False, 'messages':  serializer.errors , 'status' : status.HTTP_400_BAD_REQUEST }, status= status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'success': False, 'message': f"Ocurrió un error al crear el curso: {e}", 'status' : status.HTTP_400_BAD_REQUEST }, status= status.HTTP_400_BAD_REQUEST)
