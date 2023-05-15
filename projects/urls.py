from django.urls import path, include
from rest_framework import routers,viewsets
from .views import AnemiaViewSet
from .views import DiabetesViewSet

router = routers.DefaultRouter()
router.register(r'anemia', AnemiaViewSet)
routerDiabetes = routers.DefaultRouter()
routerDiabetes.register(r'diabetes', DiabetesViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('', include(routerDiabetes.urls)),
]