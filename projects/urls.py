from django.urls import path, include
from rest_framework import routers,viewsets

from projects.Views.views import AnemiaViewSet,DiabetesViewSet,CancerPulmonarViewSet
from projects.Views.hospital_views import HospitalViewSet
from projects.Views.medico_views import  MedicoViewSet
from projects.Views.paciente_views import PacienteViewSet
from projects.Views.enfemedades_views import HistorialViewSet
# from Views import AnemiaViewSet,DiabetesViewSet,CancerPulmonarViewSet
from projects.Views.asignacionMedico_views import AsignacionMedicoViewSet
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
routerHistorial=routers.DefaultRouter()
routerHistorial.register(r'historial',HistorialViewSet)
routerAsignacion=routers.DefaultRouter()
routerAsignacion.register(r'asignacion',AsignacionMedicoViewSet)
urlpatterns = [
    path('', include(routerAnemia.urls)),
    path('', include(routerDiabetes.urls)),
    path('', include(routerCancerPulmonar.urls)),
    path('', include(routerHospital.urls)),
    path('', include(routerMedico.urls)),
    path('', include(routerPaciente.urls)),
    path('', include(routerHistorial.urls)),
    path('', include(routerAsignacion.urls)),
    path('asignacion/pacientes',AsignacionMedicoViewSet.as_view({'get':'pacientes_enfermedades'}), name='pacientes-enfermedades' ),
    path('login/', MedicoViewSet.as_view({'post': 'login_api'}), name='login-api'),
    path('search/', PacienteViewSet.as_view({'get': 'search'}), name='search'),
    path('enfermedades/anemia/',HistorialViewSet.as_view({'post':'create_Anemia'}), name='create-Anemia'),
    path('enfermedades/diabetes/',HistorialViewSet.as_view({'post':'create_Diabetes'}), name='create-Diabetes'),
    path('enfermedades/cancerPulmonar/',HistorialViewSet.as_view({'post':'create_CancerPulmonar'}), name='create-CancerPulmonar'),
    path('enfermedades/historial/',HistorialViewSet.as_view({'get':'list'}), name='list'),
]