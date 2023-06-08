from rest_framework import serializers
from .models import Project
from .models import Anemia,Diabetes,CancerPulmonar
from .models import Hospital,Medico,Paciente

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields=('id','title','description','technology','created_at')
        read_only_fields = ('created_at',)

class AnemiaSerializer(serializers.ModelSerializer):
    class Meta:
        model= Anemia
        exclude=['paciente','medico']        
        read_only_fields = ('fecha',)
class DiabetesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diabetes
        exclude=['paciente','medico']        
        read_only_fields = ('fecha',)
class  CancerPulmonarSerializer(serializers.ModelSerializer):
    class Meta:
        model= CancerPulmonar
        exclude=['paciente','medico']        
        read_only_fields = ('fecha',)
class HopitalSerializer(serializers.ModelSerializer):
    class Meta:
        model= Hospital
        exclude=['codigo']
class MedicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medico
        exclude=['hospital','user']
class PacienteSerializer(serializers.ModelSerializer):
    class Meta:
        model=Paciente
        fields=('__all__')
# class HistorialSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=HistorialPaciente
#         fields=('__all__')
#         #exclude=['paciente','anemia','diabetes','cancer_pulmonar']
#         unique_together = ['paciente', 'anemia', 'diabetes', 'cancer_pulmonar']
# class AsignacionMedicoSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=AsignacionMedico
#         fields=('__all__')
#         # exclude=['fecha_asignacion']