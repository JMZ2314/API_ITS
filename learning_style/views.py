from rest_framework import views,pagination,status
from rest_framework.response import Response
from core.serializers import LearningStyleSerializer
from core.models import LearningStyle

class LearningStyleView(views.APIView,pagination.PageNumberPagination):

    serializer_class = LearningStyleSerializer
    
    def get(self,request,format = None):
        try:
            learning_styles = LearningStyle.objects.all()
            paginated_data = self.paginate_queryset(learning_styles,request)
            serializer =  self.serializer_class( paginated_data, many = True)
            return Response({'success': True , 'count': learning_styles.count()  , 'data': serializer.data, 'next':self.get_next_link() , 'previous':self.get_previous_link() , 'status:' : status.HTTP_200_OK } , status= status.HTTP_200_OK)
        except Exception as e:
            return Response({'success': 0, 'message': f"{e}", 'status' : status.HTTP_400_BAD_REQUEST }, status= status.HTTP_400_BAD_REQUEST)