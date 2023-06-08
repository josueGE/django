from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from projects.serializers import PacienteSerializer
from projects.models import Paciente,Diabetes,Anemia,CancerPulmonar
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
    def obtener_enfermedades_paciente(self,request,pk=None):
        # enfermedades = []
        # # Obtener todas las instancias de Anemia relacionadas con el paciente
        # anemias = Anemia.objects.filter(paciente_id=pk)
        # for anemia in anemias:
        #     enfermedades.append('anemia')
        # # Obtener todas las instancias de Diabetes relacionadas con el paciente
        # diabetes = Diabetes.objects.filter(paciente_id=pk)
        # for diabete in diabetes:
        #     enfermedades.append('diabetes')
        # # Obtener todas las instancias de CancerPulmonar relacionadas con el paciente
        # canceres_pulmonares = CancerPulmonar.objects.filter(paciente_id=pk)
        # for cancer_pulmonar in canceres_pulmonares:
        #     enfermedades.append('cancer_pulmonar')
        # return Response(enfermedades)
        pacientes = Paciente.objects.filter(
        Q(anemia__isnull=False) | Q(diabetes__isnull=False) | Q(cancerpulmonar__isnull=False)
        ).prefetch_related('anemia_set', 'diabetes_set', 'cancerpulmonar_set')

        resultado = []
        for paciente in pacientes:
            enfermedades = []
            if paciente.anemia_set.exists():
                enfermedades.append('anemia')
            if paciente.diabetes_set.exists():
                enfermedades.append('diabetes')
            if paciente.cancerpulmonar_set.exists():
                enfermedades.append('cancer_pulmonar')
            resultado.append({
                'nombre': paciente.nombre,
                'apellido': paciente.apellido,
                'enfermedades': enfermedades
            })
        return Response(resultado)    