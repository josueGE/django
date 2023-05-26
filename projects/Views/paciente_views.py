from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from projects.serializers import PacienteSerializer
from projects.models import Paciente
from django.db.models import Q
class PacienteViewSet(viewsets.ModelViewSet):
    serializer_class = PacienteSerializer
    queryset = Paciente.objects.all()
    def create(self,request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            # hospital=codigo_hospital_obj.id
            # serializer.validated_data['hospital'] = hospital 
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def update(self,request,pk=None):
        try:
            paciente=Paciente.objects.get(pk=pk)
            serializer = self.serializer_class(paciente,data=request.data)
            if serializer.is_valid():
                # hospital=codigo_hospital_obj.id
                # serializer.validated_data['hospital'] = hospital 
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Paciente.DoesNotExist:
                return Response({'error': 'no existe el paciente.'}, status=status.HTTP_400_BAD_REQUEST)
    def search(self, request):
        search_query = request.query_params.get('q', '')
        pacientes = Paciente.objects.filter(
            Q(nombre__icontains=search_query) | Q(apellido__icontains=search_query)
        )
        result = []
        for paciente in pacientes:
            result.append({
                'id': paciente.id,
                'nombre': paciente.nombre,
                'apellido': paciente.apellido,
            })
        return Response(result)
    def destroy(self, request, pk=None):
        try:
            paciente = Paciente.objects.get(pk=pk)
            paciente.delete()
            return Response({'mensaje':'se elimino correctamente el paciente'},status=status.HTTP_204_NO_CONTENT)
        except Paciente.DoesNotExist:
            return Response({'error': 'no existe el paciente.'}, status=status.HTTP_400_BAD_REQUEST)
    def retrieve(self, request, pk=None):
        try:
            paciente = Paciente.objects.get(pk=pk)
            serializer = self.serializer_class(paciente)
            response_data = serializer.data
            return Response(response_data)
        except Paciente.DoesNotExist:
            return Response({'error': 'no existe el medico.'}, status=status.HTTP_400_BAD_REQUEST)    