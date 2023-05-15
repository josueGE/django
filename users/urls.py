from django.urls import path
from rest_framework import routers
from . import views
router = routers.DefaultRouter()
urlpatterns=[
    path('api/login/', views.login_api),
    # path('api/login2/', views.login),
    path('api/register/', views.register_api),
    path('api/mostrar/', views.mostrar_usuarios_api),
    path('api/buscar-usuario/<int:user_id>/', views.buscar_usuario_api),
    path('api/eliminar-usuario/<int:user_id>/', views.eliminar_usuario_api),
]