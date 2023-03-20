from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from core.models import Answer
from core.serializers import AnswerUserSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.parsers import JSONParser,FormParser,MultiPartParser

class AnswerUserView(APIView,PageNumberPagination):

    serializer_class = AnswerUserSerializer
    parser_classes = [JSONParser,FormParser,MultiPartParser]
    # authentication_classes = [JWTAuthentication,]
    # permission_classes = [IsAuthenticated,] 
    
    def post(self, request):
        
        try:

            serializer = self.serializer_class(data=request.data)

            if(serializer.is_valid()):
                user_answer_created =   self.serializer_class(serializer.save()).data
                return Response({'success': True, 'message': "La respuesta fue registrada con exito", 'data': user_answer_created , 'status' : status.HTTP_200_OK }, status= status.HTTP_200_OK)
            else:
                return Response({'success': False, 'messages':  serializer.errors , 'status' : status.HTTP_400_BAD_REQUEST }, status= status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'success': False, 'message': f"Ocurrió un error al regitrar la respuesta: {e}", 'status' : status.HTTP_400_BAD_REQUEST }, status= status.HTTP_400_BAD_REQUEST)
