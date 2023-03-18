from rest_framework import views,pagination,status
from rest_framework.response import Response
from core.serializers import LearningStyleSerializer
from core.models import LearningStyle
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

class LearningStyleView(views.APIView,pagination.PageNumberPagination):

    serializer_class = LearningStyleSerializer
    # authentication_classes = [JWTAuthentication,]
    # permission_classes = [IsAuthenticated,]

    def get(self,request,format = None):
        try:
            learning_styles = LearningStyle.objects.all()
            paginated_data = self.paginate_queryset(learning_styles,request)
            serializer =  self.serializer_class( paginated_data, many = True)
            return Response({'success': True , 'count': learning_styles.count()  , 'data': serializer.data, 'next':self.get_next_link() , 'previous':self.get_previous_link() , 'status:' : status.HTTP_200_OK } , status= status.HTTP_200_OK)
        except Exception as e:
            return Response({'success': False, 'message': f"{e}", 'status' : status.HTTP_400_BAD_REQUEST }, status= status.HTTP_400_BAD_REQUEST)
    
    def post(self, request):

        try:

            serializer = self.serializer_class(data=request.data)

            if(serializer.is_valid()):
                learning_style_created =   self.serializer_class(serializer.save()).data
                return Response({'success': True, 'message': "Estilo de aprendizaje creado exitosamente", 'data': learning_style_created , 'status' : status.HTTP_200_OK }, status= status.HTTP_200_OK)
            else:
                return Response({'success': False, 'messages':  serializer.errors , 'status' : status.HTTP_400_BAD_REQUEST }, status= status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'success': False, 'message': f"{e}", 'status' : status.HTTP_400_BAD_REQUEST }, status= status.HTTP_400_BAD_REQUEST)
