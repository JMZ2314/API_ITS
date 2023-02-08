from rest_framework import views,pagination,status
from rest_framework.response import Response
from core.models import User
from core.serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated


class UserView(views.APIView,pagination.PageNumberPagination):

    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated,]  

    def get(self,request,format=None):
    
        try:
            users = User.objects.all()
            print(users)
            paginated_data = self.paginate_queryset(users,request)
            serializer = self.serializer_class( paginated_data, many = True)

            return Response({'success': True , 'count': users.count()  , 'data': serializer.data, 'next':self.get_next_link() , 'previous':self.get_previous_link() , 'status:' : status.HTTP_200_OK }, status= status.HTTP_200_OK  )
        except Exception as e:
            return Response({'success': False, 'message': f"{e}", 'status' : status.HTTP_400_BAD_REQUEST } , status= status.HTTP_400_BAD_REQUEST)

        