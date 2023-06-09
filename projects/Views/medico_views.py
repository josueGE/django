from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from projects.serializers import MedicoSerializer
from projects.models import Medico,Hospital, Paciente,Anemia,Diabetes,CancerPulmonar
from django.contrib.auth.models import User
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.auth import AuthToken
from django.db.models import Q
class  MedicoViewSet(viewsets.ModelViewSet):
    serializer_class = MedicoSerializer
    queryset = Medico.objects.all()
    def create(self, request):
        codigo_hospital = request.data.get('codigoHospital')
        if not codigo_hospital:
            return Response({'error': 'El campo codigoHospital es requerido.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            codigo_hospital_obj = Hospital.objects.get(codigo=codigo_hospital)
        except Hospital.DoesNotExist:
            return Response({'error': 'El código de hospital no existe.'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            correo_electronico = request.data.get('correoElectronico')
            password_medico = request.data.get('password')
            # Crear el objeto User solo si no existe un usuario con el mismo correo electrónico
            user = User.objects.create_user(username=correo_electronico, email=correo_electronico, password=password_medico)
            # Crear el objeto Medico y asignar el usuario si corresponde
            medico = serializer.save(hospital=codigo_hospital_obj, user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def list(self, request):
        medicos = Medico.objects.all()
        serializer = self.serializer_class(medicos, many=True)
        response_data = []
        for data in serializer.data:
            medico_id = data['id']
            medico = Medico.objects.get(id=medico_id)
            data['hospital'] = medico.hospital.nombre
            data.pop('password', None)
            response_data.append(data)
        return Response(response_data)
    def update(self,request, pk=None):
        try:
            medico= Medico.objects.get(pk=pk)
            serializer = self.serializer_class(medico, data=request.data)
            codigo_hospital = request.data.get('codigoHospital')
            if not codigo_hospital:
                return Response({'error': 'El campo codigoHospital es requerido.'}, status=status.HTTP_400_BAD_REQUEST)
            try:
                codigo_hospital_obj = Hospital.objects.get(codigo=codigo_hospital)
                # return Response({'mensaje':codigo_hospital_obj.nombre})
            except Hospital.DoesNotExist:
                return Response({'error': 'El código de hospital no existe.'}, status=status.HTTP_400_BAD_REQUEST)
            if serializer.is_valid():
                serializer.save(hospital=codigo_hospital_obj)
                return Response(serializer.data,status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Medico.DoesNotExist:
            return Response({'error': 'no existe el medico.'}, status=status.HTTP_400_BAD_REQUEST)
    def destroy(self, request, pk=None):
        try:
            medico = Medico.objects.get(pk=pk)
            medico.delete()
            return Response({'mensaje':'se elimino correctamente el medico'},status=status.HTTP_204_NO_CONTENT)
        except Medico.DoesNotExist:
            return Response({'error': 'no existe el medico para eliminarlo.'}, status=status.HTTP_400_BAD_REQUEST)
    def retrieve(self, request, pk=None):
        try:
            medico = Medico.objects.get(pk=pk)
            serializer = self.serializer_class(medico)
            response_data = serializer.data
            response_data['hospital'] = medico.hospital.nombre
            response_data.pop('password', None)
            return Response(response_data)
        except Medico.DoesNotExist:
            return Response({'error': 'no existe el medico.'}, status=status.HTTP_400_BAD_REQUEST)
    def login_api(self,request):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user= serializer.validated_data['user']
        _,token =AuthToken.objects.create(user)
        
        medico = Medico.objects.get(user=user)
        
        return Response({
            'medico': {
        'id': medico.id,
        'nombre': medico.nombre,
        'apellido': medico.apellido,
        'correoElectronico': medico.correoElectronico,
        'numero_celular': medico.numero_celular,
        'ci': medico.ci,
        'especialidad': medico.especialidad,
        'rol': medico.rol,
        'hospital': medico.hospital.nombre,
        'id_hospital':medico.hospital.id,},
            'usser_info':{
                'id':user.id,
            },
            'token':token,
        },status=status.HTTP_200_OK)
    def obtener_pacientes_por_medico(self, request, medico_id=None):
        try:
            medico = Medico.objects.get(pk=medico_id)
            anemias = Anemia.objects.filter(medico_id=medico_id)
            diabetes = Diabetes.objects.filter(medico_id=medico_id)
            cancer_pulmonar = CancerPulmonar.objects.filter(medico_id=medico_id)
            resultado = []
            
            for anemia in anemias:
                paciente = anemia.paciente
                resultado.append({
                    'id_paciente': paciente.id,
                    'anemia_id': anemia.id,  # Agrega el ID de la enfermedad
                    'nombre': paciente.nombre,
                    'apellido': paciente.apellido,
                    'enfermedad': 'anemia'
                })
            
            for diabetic in diabetes:
                paciente = diabetic.paciente
                resultado.append({
                    'id_paciente': paciente.id,
                    'id_enfermedad': diabetic.id,  # Agrega el ID de la enfermedad
                    'nombre': paciente.nombre,
                    'apellido': paciente.apellido,
                    'enfermedad': 'diabetes'
                })
            
            for cancer in cancer_pulmonar:
                paciente = cancer.paciente
                resultado.append({
                    'id_paciente': paciente.id,
                    'id_enfermedad': cancer.id,  # Agrega el ID de la enfermedad
                    'nombre': paciente.nombre,
                    'apellido': paciente.apellido,
                    'enfermedad': 'cancer_pulmonar'
                })
            
            return Response(resultado)
        
        except Medico.DoesNotExist:
            return Response({'error': f"No se encontró el médico con ID {medico_id}"}, status=status.HTTP_404_NOT_FOUND)
