from datetime import timezone
import datetime
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from projects.models import AsignacionMedico,HistorialPaciente,Medico,Anemia,Diabetes,CancerPulmonar
from projects.serializers import AsignacionMedicoSerializer
from django.db.models import Prefetch
class AsignacionMedicoViewSet(viewsets.ModelViewSet):
    serializer_class=AsignacionMedicoSerializer
    queryset=AsignacionMedico.objects.all()
    def create(self, request):
        codigoMedico=request.data.get('medico')
        codigoHistorial=request.data.get('historial')
        try:
            historial = HistorialPaciente.objects.get(pk=codigoHistorial)
        except HistorialPaciente.DoesNotExist:
            return Response({'error': 'no existe el historial paciente.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            medico = Medico.objects.get(pk=codigoMedico)
        except Medico.DoesNotExist:
            return Response({'error': 'no existe el medico.'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            serializer.validated_data['historial'] = historial
            serializer.validated_data['medico'] = medico
            serializer.validated_data['fecha_asignacion'] = datetime.datetime.now()
            serializer.save()
            data = serializer.data
            data['fecha_asignacion'] = serializer.validated_data['fecha_asignacion']
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def pacientes_enfermedades(self, request):
        medico_id = request.data.get('medico_id')
        try:
            medico = Medico.objects.get(pk=medico_id)
        except Medico.DoesNotExist:
            return Response({'error': 'No existe el médico.'}, status=status.HTTP_400_BAD_REQUEST)
        asignaciones = AsignacionMedico.objects.filter(medico=medico).select_related('historial__paciente')
        pacientes_enfermedades = asignaciones.prefetch_related(
            Prefetch('historial__anemia', queryset=Anemia.objects.all()),
            Prefetch('historial__diabetes', queryset=Diabetes.objects.all()),
            Prefetch('historial__cancer_pulmonar', queryset=CancerPulmonar.objects.all())
        )
        resultado = []
        for asignacion in pacientes_enfermedades:
            paciente = asignacion.historial.paciente
            enfermedades = []
            if asignacion.historial.anemia:
                enfermedades.append(('anemia', asignacion.historial.anemia.id))
            if asignacion.historial.diabetes:
                enfermedades.append(('diabetes', asignacion.historial.diabetes.id))
            if asignacion.historial.cancer_pulmonar:
                enfermedades.append(('cancer pulmonar', asignacion.historial.cancer_pulmonar.id))
            resultado.append({
                'paciente_id': paciente.id,
                'nombre': paciente.nombre,
                'apellido': paciente.apellido,
                'enfermedades': enfermedades
            })
        return Response(resultado, status=status.HTTP_200_OK)
        