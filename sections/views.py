from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from core.models import Section
from core.serializers import SectionSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination

class SectionView(APIView,PageNumberPagination):

    serializer_class = SectionSerializer
    permission_classes = [IsAuthenticated,]  

    def get (self,request):
        try:
            sections = Section.objects.all()
            paginated_data = self.paginate_queryset(sections,request)
            serializer = self.serializer_class( paginated_data, many = True)

            return Response({'success': True , 'count': sections.count()  , 'data': serializer.data, 'next':self.get_next_link() , 'previous':self.get_previous_link() , 'status:' : status.HTTP_200_OK }, status= status.HTTP_200_OK  )
        except Exception as e:
            return Response({'success': False, 'message': f"{e}", 'status' : status.HTTP_400_BAD_REQUEST } , status= status.HTTP_400_BAD_REQUEST)
