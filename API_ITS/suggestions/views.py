from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from suggestions.models import Suggestions
from answers.models import Answer,User_Answer
from core.serializers import SuggestionsSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.parsers import JSONParser,FormParser,MultiPartParser

class SuggestionView(APIView,PageNumberPagination):

    serializer_class = SuggestionsSerializer
    parser_classes = [JSONParser,FormParser,MultiPartParser]
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated,]  

    def get (self,request):
        try:

            user_id = request.query_params.get('user_id')

            filter_by_user = user_id is not None

            if(filter_by_user):
                suggestions = Suggestions.objects.filter(user_id = user_id)
                
            else:
                suggestions = Suggestions.objects.all()

            paginated_data = self.paginate_queryset(suggestions,request)
            serializer = self.serializer_class( paginated_data, many = True)          

            return Response({'success': True , 'count': suggestions.count()  , 'data': serializer.data, 'next':self.get_next_link() , 'previous':self.get_previous_link() , 'status:' : status.HTTP_200_OK }, status= status.HTTP_200_OK  )

        
        except Exception as e:
            # return Response({'success':False, 'data': None})
            return Response({'success': False, 'message': f"{e}", 'status' : status.HTTP_400_BAD_REQUEST } , status= status.HTTP_400_BAD_REQUEST)
        

    def post(self, request):
        
        try:

            serializer = self.serializer_class(data=request.data)

            if(serializer.is_valid()):
                suggestion_created =   self.serializer_class(serializer.save()).data
                return Response({'success': True, 'message': "Tu sugerencia fue registrada exitosamente", 'data': suggestion_created , 'status' : status.HTTP_200_OK }, status= status.HTTP_200_OK)
            else:
                return Response({'success': False, 'messages':  serializer.errors , 'status' : status.HTTP_400_BAD_REQUEST }, status= status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'success': False, 'message': f"Ocurrió un error al registrar la sugerencia: {e}", 'status' : status.HTTP_400_BAD_REQUEST }, status= status.HTTP_400_BAD_REQUEST)
    

class SuggestionViewDetail(APIView):

    serializer_class = SuggestionsSerializer
    parser_classes = [JSONParser,FormParser,MultiPartParser]
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated,] 

    def put(self,request,pk,format= None):

        try:
            suggestion = Suggestions.objects.get(id = pk)
            serializer = SuggestionsSerializer(suggestion, data=request.data)
            if serializer.is_valid():
                suggestion_updated = self.serializer_class(serializer.save()).data
                return Response({'success': True, 'message': "Tu sugerencia fue editada exitosamente", 'data': suggestion_updated , 'status' : status.HTTP_200_OK }, status= status.HTTP_200_OK)

        except Exception as e:
                return Response({'success': False, 'message': f"Ocurrió un error al editar la sugerencia: {e}", 'status' : status.HTTP_400_BAD_REQUEST }, status= status.HTTP_400_BAD_REQUEST)

