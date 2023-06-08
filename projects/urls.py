from django.urls import path, include
from rest_framework import routers,viewsets
from projects.Views.anemia_views import AnemiaViewSet
from projects.Views.diabetes_views import DiabetesViewSet
from projects.Views.cancerP_views import CancerPulmonarViewSet
from projects.Views.hospital_views import HospitalViewSet
from projects.Views.medico_views import  MedicoViewSet
from projects.Views.paciente_views import PacienteViewSet
# from Views import AnemiaViewSet,DiabetesViewSet,CancerPulmonarViewSet
routerAnemia = routers.DefaultRouter()
routerAnemia.register(r'anemia', AnemiaViewSet)
routerDiabetes = routers.DefaultRouter()
routerDiabetes.register(r'diabetes', DiabetesViewSet)
routerCancerPulmonar=routers.DefaultRouter()
routerCancerPulmonar.register(r'cancerPulmonar',CancerPulmonarViewSet)
routerHospital = routers.DefaultRouter()
routerHospital.register(r'hospital',HospitalViewSet)
routerMedico = routers.DefaultRouter()
routerMedico.register(r'medico',MedicoViewSet)
routerPaciente = routers.DefaultRouter()
routerPaciente.register(r'paciente',PacienteViewSet)


urlpatterns = [
    path('', include(routerAnemia.urls)),
    path('', include(routerDiabetes.urls)),
    path('', include(routerCancerPulmonar.urls)),
    path('', include(routerHospital.urls)),
    path('', include(routerMedico.urls)),
    path('', include(routerPaciente.urls)),
    path('login/', MedicoViewSet.as_view({'post': 'login_api'}), name='login-api'),
    path('search/', PacienteViewSet.as_view({'get': 'search'}), name='search'),
    # path('paciente/enfermedades/<int:pk>/', PacienteViewSet.as_view({'get': 'obtener_enfermedades_paciente'}), name='obtener-enfermedades-paciente'),
    path('medico/pacientes/<int:medico_id>/',MedicoViewSet.as_view({'get':'obtener_pacientes_por_medico'}) , name='obtener-pacientes-por-medico'),
]