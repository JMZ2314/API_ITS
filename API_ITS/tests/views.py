from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from core.models import Test
from core.serializers import TestSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.authentication import JWTAuthentication

class TestView(APIView,PageNumberPagination):

    serializer_class = TestSerializer
    # authentication_classes = [JWTAuthentication,]
    # permission_classes = [IsAuthenticated,]  

    def get (self,request):
        try:
         
            test_id = request.query_params.get('id')

            filter_by_id = test_id is not None

            if (filter_by_id):
                tests = [Test.objects.get(id = test_id),]
            else:
                tests = Test.objects.all()
       

            paginated_data = self.paginate_queryset(tests,request)
            serializer = self.serializer_class( paginated_data, many = True)

            return Response({'success': True , 'count': 0 if filter_by_id else tests.count() , 'data': serializer.data[0]  if filter_by_id else serializer.data , 'next':self.get_next_link() , 'previous':self.get_previous_link() , 'status:' : status.HTTP_200_OK }, status= status.HTTP_200_OK  )
        except Exception as e:
            return Response({'success': False, 'message': f"{e}", 'status' : status.HTTP_400_BAD_REQUEST } , status= status.HTTP_400_BAD_REQUEST)
