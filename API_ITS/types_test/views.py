from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from types_test.models import TypeTest
from core.serializers import TypeTestSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination

class TypeTestView(APIView,PageNumberPagination):

    serializer_class = TypeTestSerializer
    permission_classes = [IsAuthenticated,]  

    def get (self,request):
        try:
            types_test = TypeTest.objects.all()
            paginated_data = self.paginate_queryset(types_test,request)
            serializer = self.serializer_class( paginated_data, many = True)

            return Response({'success': True , 'count': types_test.count()  , 'data': serializer.data, 'next':self.get_next_link() , 'previous':self.get_previous_link() , 'status:' : status.HTTP_200_OK }, status= status.HTTP_200_OK  )
        except Exception as e:
            return Response({'success': False, 'message': f"{e}", 'status' : status.HTTP_400_BAD_REQUEST } , status= status.HTTP_400_BAD_REQUEST)
