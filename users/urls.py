from django.urls import path
from . import views

urlpatterns=[
    path('api/login/', views.login_api),
    path('api/register/', views.register_api),
    path('api/mostrar/', views.mostrar_usuarios_api),
]