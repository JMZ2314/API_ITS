from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from answers.models import Answer
from core.serializers import AnswerSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.parsers import JSONParser,FormParser,MultiPartParser

class AnswerView(APIView,PageNumberPagination):

    serializer_class = AnswerSerializer
    parser_classes = [JSONParser,FormParser,MultiPartParser]
    # authentication_classes = [JWTAuthentication,]
    # permission_classes = [IsAuthenticated,]  

    def get (self,request):
        try:
            
            test_id = request.query_params.get('test')
            filter_by_test = test_id is not None

            if(filter_by_test):
                answers = Answer.objects.filter(test_id = test_id)
            else:
                answers = Answer.objects.all()

            paginated_data = self.paginate_queryset(answers,request)
            serializer = self.serializer_class( paginated_data, many = True)

            return Response({'success': True , 'count': answers.count()  , 'data': serializer.data, 'next':self.get_next_link() , 'previous':self.get_previous_link() , 'status:' : status.HTTP_200_OK }, status= status.HTTP_200_OK  )
        except Exception as e:
            return Response({'success': False, 'message': f"{e}", 'status' : status.HTTP_400_BAD_REQUEST } , status= status.HTTP_400_BAD_REQUEST)
    
    def post(self, request):
        
        try:

            serializer = self.serializer_class(data=request.data)

            if(serializer.is_valid()):
                answer_created =   self.serializer_class(serializer.save()).data
                return Response({'success': True, 'message': "La respuesta fue creada exitosamente", 'data': answer_created , 'status' : status.HTTP_200_OK }, status= status.HTTP_200_OK)
            else:
                return Response({'success': False, 'messages':  serializer.errors , 'status' : status.HTTP_400_BAD_REQUEST }, status= status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'success': False, 'message': f"Ocurrió un error al crear la respuesta: {e}", 'status' : status.HTTP_400_BAD_REQUEST }, status= status.HTTP_400_BAD_REQUEST)
