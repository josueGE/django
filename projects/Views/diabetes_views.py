from django.shortcuts import render
from rest_framework import viewsets
# from serializers import AnemiaSerializer
# from serializers import DiabetesSerializer,CancerPulmonarSerializer
# from models import Anemia
# from models import Diabetes, CancerPulmonar
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from projects.models import Diabetes,Anemia,CancerPulmonar,Paciente,Medico
from projects.serializers import DiabetesSerializer,AnemiaSerializer,CancerPulmonarSerializer

class DiabetesViewSet(viewsets.ModelViewSet):
    serializer_class = DiabetesSerializer
    queryset = Diabetes.objects.all()         

    def create(self, request):
        codigo_paciente = request.data.get('paciente')
        codigo_medico = request.data.get('medico')
        if not codigo_paciente:
            return Response({'error': 'El campo paciente es requerido.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            codigo_paciente_obj = Paciente.objects.get(pk=codigo_paciente)
        except Paciente.DoesNotExist:
            return Response({'error': 'El paciente no existe.'}, status=status.HTTP_400_BAD_REQUEST)
        if not codigo_medico:
            return Response({'error': 'El campo medico es requerido.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            codigo_medico_obj = Medico.objects.get(pk=codigo_medico)
        except Medico.DoesNotExist:
            return Response({'error': 'El medico no existe.'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(paciente=codigo_medico_obj,medico=codigo_medico_obj)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def retrieve(self, request, pk=None):
        try:
            diabetes = Diabetes.objects.get(pk=pk)
        except Diabetes.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        try:
            diabetes = Diabetes.objects.get(pk=pk)
        except Diabetes.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(diabetes)
        return Response(serializer.data)
    def update(self, request, pk=None):
        try:
            diabetes = Diabetes.objects.get(pk=pk)
        except Diabetes.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(diabetes, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def destroy(self, request, pk=None):
        try:
            diabetes = Diabetes.objects.get(pk=pk)
        except Diabetes.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        diabetes.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    def list(self, request):
        anemias = Diabetes.objects.all()
        serializer = self.serializer_class(anemias, many=True)
        return Response(serializer.data)
