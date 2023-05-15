from django.shortcuts import render
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.auth import AuthToken
from .serializers import RegisterSerializer
from django.contrib.auth.models import User
from .serializers import RegisterSerializer
from rest_framework import status
# Create your views here.
#nuevo login
@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    # Obtener las credenciales del usuario desde el cuerpo de la solicitud
    email = request.data.get('email')
    password = request.data.get('password')

    # Validar las credenciales usando el serializador de token de autenticación
    serializer = AuthTokenSerializer(data={'email': email, 'password': password})
    serializer.is_valid(raise_exception=True)

    # Obtener el usuario validado y generar un nuevo token de autenticación
    user = serializer.validated_data['user']
    token = AuthToken.objects.create(user)

    # Devolver una respuesta con el id, email y token de autenticación
    return Response({
        'id': user.id,
        'email': user.email,
    })
#
@api_view(['POST'])
def login_api(request):
    print(request.data)
    serializer = AuthTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user= serializer.validated_data['user']
    _,token =AuthToken.objects.create(user)
    
    return Response({
        'usser_info':{
            'id':user.id,
            'username':user.username,
            'email': user.email
        },
        'token':token
    })
@api_view(['GET'])
def mostrar_usuarios_api(request):
    user = User.objects.all()
    serializer = RegisterSerializer(user, many=True)
    return Response(serializer.data)
@api_view(['POST'])
def register_api(request):
    serializer=RegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user=serializer.save()
    _,token=AuthToken.objects.create(user)
    return Response( {
        'usser_info':{
            'id':user.id,
            'username':user.username,
            'email': user.email,
        },
        'token':token
    })
@api_view(['GET'])
def buscar_usuario_api(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({"error": "Usuario no encontrado"})

    serializer = RegisterSerializer(user)
    return Response(serializer.data)
@api_view(['DELETE'])
def eliminar_usuario_api(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({"error": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)

    user.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)