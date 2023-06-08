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

class AnemiaViewSet(viewsets.ModelViewSet):
    serializer_class = AnemiaSerializer
    queryset = Anemia.objects.all()
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
            serializer.save(paciente=codigo_paciente_obj,medico=codigo_medico_obj)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # def create(self, request):
    # # obtener los datos del request
    #     model=''
    #     datos = request.data
        
        
    #     # hacer la prediccion utilizando el modelo .pkl

    #     x_in=[
    #         np.float_(datos['Hemogobina']),
    #         np.float_(datos['MCH']),
    #         np.float_(datos['MCHC']),
    #         np.float_(datos['MCV']),
    #         np.int_(datos['genero'])
    #     ]    
    #     print(x_in)
    #     if model == '':
    #         with open(Model_path,'rb') as file:
    #             model = pickle.load(file)
    #     resultado = model_prediction(x_in,model)
    #     print(resultado)
    #     # crear una instancia de Anemia y asignar el resultado
    #     anemia = Anemia(
    #         nombreUsuario=datos['nombreUsuario'],
    #         Hemogobina=datos['Hemogobina'],
    #         MCH=datos['MCH'],
    #         MCHC=datos['MCHC'],
    #         MCV=datos['MCV'],
    #         Resultado=resultado[0],
    #         genero=int(datos['genero'])
    #     )

    #     # guardar la instancia en la base de datos
    #     anemia.save()

    #     # devolver la respuesta
    #     serializer = self.serializer_class(anemia)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        try:
            anemia = Anemia.objects.get(pk=pk)
            serializer = self.serializer_class(anemia)
            return Response(serializer.data)
        except Anemia.DoesNotExist:
            return Response({'error': 'no existe el reporte de anemia.'}, status=status.HTTP_400_BAD_REQUEST)

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
