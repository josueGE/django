from django.shortcuts import render
from rest_framework import viewsets
from .serializers import AnemiaSerializer
from .models import Anemia
from django.shortcuts import render
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import status
import joblib
# Create your views here.
class AnemiaViewSet(viewsets.ModelViewSet):
    serializer_class = AnemiaSerializer
    queryset = Anemia.objects.all()

    def create(self, request):
        # obtener los datos del request
        datos = request.data

        # hacer la prediccion utilizando el modelo .pkl
        modelo = joblib.load('MODELADOS/anemia.pkl')
        resultado = modelo.predict(datos)

        # crear una instancia de Anemia y asignar el resultado
        anemia = Anemia(
            nombreUsuario=datos['nombreUsuario'],
            Hemogobina=datos['Hemogobina'],
            MCH=datos['MCH'],
            MCHC=datos['MCHC'],
            MCV=datos['MCV'],
            Resultado=resultado
        )

        # guardar la instancia en la base de datos
        anemia.save()

        # devolver la respuesta
        serializer = self.serializer_class(anemia)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        anemia = Anemia.objects.get(pk=pk)
        serializer = self.serializer_class(anemia)
        return Response(serializer.data)

    def update(self, request, pk=None):
        anemia = Anemia.objects.get(pk=pk)
        serializer = self.serializer_class(anemia, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        anemia = Anemia.objects.get(pk=pk)
        anemia.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def list(self, request):
        anemias = Anemia.objects.all()
        serializer = self.serializer_class(anemias, many=True)
        return Response(serializer.data)
    