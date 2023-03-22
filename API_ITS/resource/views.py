from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from resource.models import Resource
from core.serializers import ResourceSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.parsers import MultiPartParser,FormParser,JSONParser

class ResourceView(APIView,PageNumberPagination):

    serializer_class = ResourceSerializer
    parser_classes = [MultiPartParser,FormParser,JSONParser]
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated,]  

    def get (self,request):
        try:

            resource_id = request.query_params.get('id')

            filter_by_id = resource_id is not None

            if(filter_by_id):
                resources = [Resource.objects.get(id= resource_id),]
            else:
                resources   = Resource.objects.all()

            paginated_data = self.paginate_queryset(resources,request)            
        
        
            serializer = self.serializer_class( paginated_data, many = True)

            return Response({'success': True , 'count': 0 if filter_by_id else resources.count() , 'data': serializer.data[0]  if filter_by_id else serializer.data, 'next':self.get_next_link() , 'previous':self.get_previous_link() , 'status:' : status.HTTP_200_OK }, status= status.HTTP_200_OK  )
        except Exception as e:
            return Response({'success': False, 'message': f"{e}", 'status' : status.HTTP_400_BAD_REQUEST } , status= status.HTTP_400_BAD_REQUEST)
    

    def post(self,request):
        try:
            serializer = self.serializer_class(data=request.data)

            if(serializer.is_valid()):
                resource_created =   self.serializer_class(serializer.save()).data
                return Response({'success': True, 'message': "EL recurso fue creado exitosamente", 'data': resource_created , 'status' : status.HTTP_200_OK }, status= status.HTTP_200_OK)
            else:
                return Response({'success': False, 'messages':  serializer.errors , 'status' : status.HTTP_400_BAD_REQUEST }, status= status.HTTP_400_BAD_REQUEST)
        except Exception as e:
                return Response({'success': False, 'message': f"Ocurrió un error al cerar el recurso: {e}", 'status' : status.HTTP_400_BAD_REQUEST }, status= status.HTTP_400_BAD_REQUEST)

