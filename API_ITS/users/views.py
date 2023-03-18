from rest_framework import views,pagination,status
from rest_framework.response import Response
from core.models import User
from core.serializers import UserSerializer,LearningStyleSerializer,RoleSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from core import models


class UserView(views.APIView,pagination.PageNumberPagination):

    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request,format=None):
    
        try:
            users = User.objects.all()
            paginated_data = self.paginate_queryset(users,request)
            serializer = self.serializer_class( paginated_data, many = True)

            return Response({'success': True , 'count': users.count()  , 'data': serializer.data, 'next':self.get_next_link() , 'previous':self.get_previous_link() , 'status:' : status.HTTP_200_OK }, status= status.HTTP_200_OK  )
        except Exception as e:
            return Response({'success': False, 'message': f"{e}", 'status' : status.HTTP_400_BAD_REQUEST } , status= status.HTTP_400_BAD_REQUEST)

class RegisterView(views.APIView):

    serializer_class = UserSerializer

    def post(self, request):
        
        try:

            serializer = self.serializer_class(data=request.data)

            if(serializer.is_valid()):
                user_created =   self.serializer_class(serializer.save()).data
                return Response({'success': True, 'message': "Registro exitoso", 'data': user_created , 'status' : status.HTTP_200_OK }, status= status.HTTP_200_OK)
            else:
                return Response({'success': False, 'messages':  serializer.errors , 'status' : status.HTTP_400_BAD_REQUEST }, status= status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'success': False, 'message': f"Ocurrió un error al crear la cuenta: {e}", 'status' : status.HTTP_400_BAD_REQUEST }, status= status.HTTP_400_BAD_REQUEST)


        