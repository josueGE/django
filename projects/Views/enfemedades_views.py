from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from projects.models import HistorialPaciente,Paciente,Anemia,Diabetes,CancerPulmonar
from projects.serializers import HistorialSerializer
class HistorialViewSet(viewsets.ModelViewSet):
    serializer_class= HistorialSerializer
    queryset= HistorialPaciente.objects.all()
    def create_enfermedad(self, request, enfermedad_model, enfermedad_field):
        serializer = self.serializer_class(data=request.data)
        codigo_paciente = request.data.get('codigoPaciente')
        codigo_enfermedad = request.data.get(f'codigo{enfermedad_field.capitalize()}')
        
        if codigo_paciente and codigo_enfermedad:
            try:
                paciente_object = Paciente.objects.get(id=codigo_paciente)
            except Paciente.DoesNotExist:
                return Response({'error': 'El código de paciente no existe.'}, status=status.HTTP_400_BAD_REQUEST)
            
            try:
                enfermedad_object = enfermedad_model.objects.get(id=codigo_enfermedad)
            except enfermedad_model.DoesNotExist:
                return Response({'error': f'El código de {enfermedad_field} no existe.'}, status=status.HTTP_400_BAD_REQUEST)
            
            enfermedad_asociada = HistorialPaciente.objects.filter(**{enfermedad_field: enfermedad_object}).exclude(paciente=paciente_object).exists()
            
            if enfermedad_asociada:
                return Response({'error': f'La {enfermedad_field} ya está asociada a otro paciente.'}, status=status.HTTP_400_BAD_REQUEST)
            
            historial_object, created = HistorialPaciente.objects.get_or_create(paciente=paciente_object)
            
            if getattr(historial_object, enfermedad_field) == enfermedad_object:
                return Response({'error': 'El paciente ya tiene un historial con esta enfermedad.'}, status=status.HTTP_400_BAD_REQUEST)
            
            setattr(historial_object, enfermedad_field, enfermedad_object)
            historial_object.save()
            
            if created:
                return Response({'mensaje': 'Se creó exitosamente el enlace'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'mensaje': 'Se actualizó el enlace existente'}, status=status.HTTP_200_OK)
        
        return Response({'error': f'Los campos código paciente o código {enfermedad_field} no existen'}, status=status.HTTP_400_BAD_REQUEST)

    def create_Anemia(self, request):
        return self.create_enfermedad(request, Anemia, 'anemia')
    def create_Diabetes(self, request):
        return self.create_enfermedad(request, Diabetes, 'diabetes')
    def create_CancerPulmonar(self, request):
        return self.create_enfermedad(request, CancerPulmonar, 'cancer_pulmonar')
    
    def list(self, request):
        historialPaciente = HistorialPaciente.objects.all()
        serializer = self.serializer_class(historialPaciente, many=True)
        # Obtener los IDs relacionados y agregarlos al resultado del serializador
        data = serializer.data
        response_data=[]
        for item in data:
            historilaPaciente_id= item['id']
            medico = HistorialPaciente.objects.get(id=historilaPaciente_id)
            item['paciente'] = medico.paciente.id
            item['anemia'] = medico.anemia.id
            item['diabetes'] = getattr(medico.diabetes,'id',None)
            item['cancer_pulmonar'] = getattr(medico.cancer_pulmonar,'id',None)
            response_data.append(item)
        return Response(response_data)
    def destroy(self, request, pk=None):
        try:
            historial = HistorialPaciente.objects.get(pk=pk)
            historial.delete()
            return Response({'mensaje':'se elimino correctamente el historial'},status=status.HTTP_204_NO_CONTENT)
        except HistorialPaciente.DoesNotExist:
            return Response({'error': 'no existe el historial no encontrado.'}, status=status.HTTP_400_BAD_REQUEST)