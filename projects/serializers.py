from rest_framework import serializers
from .models import Project
from .models import Anemia
from .models import Diabetes
class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields=('id','title','description','technology','created_at')
        read_only_fields = ('created_at',)
class AnemiaSerializer(serializers.ModelSerializer):
    class Meta:
        model= Anemia
        fields=('__all__')
class DiabetesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diabetes
        fields=('__all__')