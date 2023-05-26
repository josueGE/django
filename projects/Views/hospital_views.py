from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from projects.models import Hospital,Paciente,Medico
from projects.serializers import HopitalSerializer,PacienteSerializer
import random
import string
from django.core.mail import send_mail
from django.conf import settings
class HospitalViewSet(viewsets.ModelViewSet):
    serializer_class= HopitalSerializer
    queryset = Hospital.objects.all()
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            nombre = serializer.validated_data['nombre']
            random_letters = ''.join(random.choices(nombre.upper(), k=3))
            codigo = random_letters + ''.join(random.choices(string.digits, k=4))
            serializer.validated_data['codigo'] = codigo
            instance=serializer.save()
            subject = 'Bienvenido al sistema hospitalario'
            message = f'HOSPITAL:{nombre} se ha creado su codigo hospital con el código: {codigo} con este codigo puede registrar a su personal de salud para el uso de la APP'
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [instance.correoElectronico]  # Reemplaza "correo" con el campo de correo del hospital
            send_mail(subject, message, from_email, recipient_list)
            response_data = serializer.data
            response_data['codigo'] = codigo
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def list(self, request):
        hospital = Hospital.objects.all()
        serializer = self.serializer_class(hospital, many=True)
        response_data = []
        for data in serializer.data:
            hospital_id = data['id']
            hospital = Hospital.objects.get(id=hospital_id)
            data['codigo'] = hospital.codigo
            response_data.append(data)
        return Response(response_data)
    def destroy(self, request, pk=None):
        try:
            hospital = Hospital.objects.get(pk=pk)
        except Hospital.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        hospital.delete()
        return Response('se elimino correctamente',status=status.HTTP_204_NO_CONTENT)
    def update(self, request,pk=None):
        try:
            hospitales = Hospital.objects.get(pk=pk)
        except Hospital.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(hospitales, data=request.data)
        
        if serializer.is_valid():
            nombre_actualizado = serializer.validated_data.get('nombre')
            if nombre_actualizado.lower() != hospitales.nombre.lower():
                random_letters = ''.join(random.choices(nombre_actualizado.upper(), k=3))
                codigo = random_letters + ''.join(random.choices(string.digits, k=4))
                serializer.validated_data['codigo'] = codigo
                # Envío del correo
                subject = 'Cambio de código en el sistema hospitalario'
                message = f'Se ha actualizado el código de su hospital. El nuevo código es: {codigo}'
                from_email = settings.EMAIL_HOST_USER
                recipient_list = [hospitales.correoElectronico]
                send_mail(subject, message, from_email, recipient_list)
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    