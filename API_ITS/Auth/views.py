from rest_framework_simplejwt.views import TokenObtainPairView,TokenBlacklistView
from rest_framework_simplejwt.serializers import TokenObtainSerializer,TokenBlacklistSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework import status,permissions
from users.models import User
from core.serializers import UserSerializer


class AuthView(TokenObtainPairView):
    
    serializer_class = TokenObtainSerializer
    

    def post(self,request):

        try:
            email = request.data['email']
            password = request.data['password']

            user = authenticate( email = email.lower(), password = password)
            # SI EXISTE EL USUARIO, CREAR EL TOKEN Y RESPONDER 
            if(user):
                user_serializer = UserSerializer(user)
                refresh = RefreshToken.for_user(user)
                return Response({'success': True, 'data': user_serializer.data, 'token': str(refresh.access_token) , 'refresh': str(refresh),'status:' : status.HTTP_200_OK }, status = status.HTTP_200_OK)
            else:
                return Response( {'success': False, 'message':'Correo o contraseña inválidos', 'status': status.HTTP_401_UNAUTHORIZED} , status= status.HTTP_401_UNAUTHORIZED)

        except Exception as e:
            return Response( {'success': False, 'message': f"{str(e)}", 'status' : status.HTTP_400_BAD_REQUEST }, status =  status.HTTP_400_BAD_REQUEST)

class LogOutView(TokenBlacklistView):
    
    serializer_class = TokenBlacklistSerializer

    def post(self,request):

        try:
            token_request = request.data['refresh']
            token = RefreshToken(token_request)
            token.blacklist()
            return Response({ 'sucess': True, 'message' : 'Token de actualización revocado exitosamente' , 'status' : status.HTTP_200_OK } , status = status.HTTP_200_OK)
        except Exception as e:
            return Response( {'success': False, 'message': f"{str(e)}", 'status' : status.HTTP_400_BAD_REQUEST }, status =  status.HTTP_404_NOT_FOUND)








