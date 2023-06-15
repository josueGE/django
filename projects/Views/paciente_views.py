from django.forms import model_to_dict
from django.shortcuts import get_object_or_404, render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from projects.serializers import PacienteSerializer
from projects.models import Medico, Paciente,Diabetes,Anemia,CancerPulmonar,Hospital
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
    def search(self, request, pk=None):
        try:
            medico = Medico.objects.get(pk=pk)
        except Medico.DoesNotExist:
            return Response({'error': 'No existe el médico.'}, status=status.HTTP_400_BAD_REQUEST)
        
        hospital = medico.hospital  # Obtener el hospital asociado al médico
        
        search_query = request.query_params.get('q', '')
        pacientes = Paciente.objects.filter(hospital=hospital).filter(
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
    def enfermedadesPaciente(self, request, pk=None):
        try:
            paciente = Paciente.objects.get(pk=pk)
            anemias = Anemia.objects.filter(paciente=paciente)
            diabetes = Diabetes.objects.filter(paciente=paciente)
            cancer_pulmonar = CancerPulmonar.objects.filter(paciente=paciente)
            resultado = []
            
            for anemia in anemias:
                resultado.append({
                    'enfermedad': 'anemia',
                    'datos': model_to_dict(anemia),  # Convierte el modelo a un diccionario
                })
            
            for diabetic in diabetes:
                resultado.append({
                    'enfermedad': 'diabetes',
                    'datos': model_to_dict(diabetic),  # Convierte el modelo a un diccionario
                })
            
            for cancer in cancer_pulmonar:
                resultado.append({
                    'enfermedad': 'cancer_pulmonar',
                    'datos': model_to_dict(cancer),  # Convierte el modelo a un diccionario
                })
            
            return Response(resultado)
        
        except Paciente.DoesNotExist:
            return Response({'error': f"No se encontró el paciente con ID {pk}"}, status=status.HTTP_404_NOT_FOUND)

    def definirHospital(self, request):
        pacientes_anemia = Paciente.objects.filter(anemia__isnull=False, hospital__isnull=True)
        pacientes_diabetes = Paciente.objects.filter(diabetes__isnull=False, hospital__isnull=True)
        pacientes_cancer = Paciente.objects.filter(cancerpulmonar__isnull=False, hospital__isnull=True)

        # Asignar hospitales a pacientes con enfermedad de anemia
        for paciente in pacientes_anemia:
            enfermedad_anemia = get_object_or_404(Anemia, paciente=paciente)
            medico = enfermedad_anemia.medico
            paciente.hospital = medico.hospital
            paciente.save()

        # Asignar hospitales a pacientes con enfermedad de diabetes
        for paciente in pacientes_diabetes:
            enfermedad_diabetes = get_object_or_404(Diabetes, paciente=paciente)
            medico = enfermedad_diabetes.medico
            paciente.hospital = medico.hospital
            paciente.save()

        # Asignar hospitales a pacientes con enfermedad de cáncer pulmonar
        for paciente in pacientes_cancer:
            enfermedad_cancer = get_object_or_404(CancerPulmonar, paciente=paciente)
            medico = enfermedad_cancer.medico
            paciente.hospital = medico.hospital
            paciente.save()

        return Response('Asignación de hospitales realizada correctamente')

    def definirHospitalView(self,request):
        self.definirHospital(request)
        return Response('Asignación de hospitales realizada correctamente')