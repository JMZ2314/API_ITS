from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from tests.models import Test
from core.serializers import TestSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.parsers import JSONParser,MultiPartParser,FormParser

class TestView(APIView,PageNumberPagination):

    serializer_class = TestSerializer
    parser_classes = [MultiPartParser,FormParser,JSONParser]
    # authentication_classes = [JWTAuthentication,]
    # permission_classes = [IsAuthenticated,]  

    def get (self,request):
        try:
         
            section_id = request.query_params.get('section_id')

            filter_by_section = section_id is not None

            if (section_id):
                tests = [Test.objects.get(section_id = section_id, level_id = 1),]
            else:
                tests = Test.objects.all()
       

            paginated_data = self.paginate_queryset(tests,request)
            serializer = self.serializer_class( paginated_data, many = True)

            return Response({'success': True , 'count': 0 if filter_by_section else tests.count() , 'data': serializer.data[0]  if filter_by_section else serializer.data , 'next':self.get_next_link() , 'previous':self.get_previous_link() , 'status:' : status.HTTP_200_OK }, status= status.HTTP_200_OK  )
        except Exception as e:
            return Response({'success': False, 'message': f"{e}", 'status' : status.HTTP_400_BAD_REQUEST } , status= status.HTTP_400_BAD_REQUEST)
        

    def post(self, request):
        
        try:

            serializer = self.serializer_class(data=request.data)

            if(serializer.is_valid()):
                test_created =   self.serializer_class(serializer.save()).data
                return Response({'success': True, 'message': "La prueba fue creada exitosamente", 'data': test_created , 'status' : status.HTTP_200_OK }, status= status.HTTP_200_OK)
            else:
                return Response({'success': False, 'messages':  serializer.errors , 'status' : status.HTTP_400_BAD_REQUEST }, status= status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'success': False, 'message': f"Ocurrió un error la prueba: {e}", 'status' : status.HTTP_400_BAD_REQUEST }, status= status.HTTP_400_BAD_REQUEST)
