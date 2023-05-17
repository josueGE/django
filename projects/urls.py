from django.urls import path, include
from rest_framework import routers,viewsets
from .views import AnemiaViewSet,DiabetesViewSet,CancerPulmonarViewSet

routerAnemia = routers.DefaultRouter()
routerAnemia.register(r'anemia', AnemiaViewSet)
routerDiabetes = routers.DefaultRouter()
routerDiabetes.register(r'diabetes', DiabetesViewSet)
routerCancerPulmonar=routers.DefaultRouter()
routerCancerPulmonar.register(r'cancerPulmonar',CancerPulmonarViewSet)
urlpatterns = [
    path('', include(routerAnemia.urls)),
    path('', include(routerDiabetes.urls)),
    path('', include(routerCancerPulmonar.urls)),
]