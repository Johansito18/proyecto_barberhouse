from unicodedata import name
from django.urls import path

from . import views

app_name = "barberhouse"

urlpatterns = [
    path('', views.inicio, name="inicio"),

    #Citas
    path('citas/', views.citas, name="listarCitas"),

    #servicios
    path('servicios/', views.servicios, name="listarServicios"),


    #usuarios
    path('usuarios/', views.usuarios, name="listarUsuarios"),


    #Promociones
    path('promociones/', views.promociones, name="listarPromociones"),


    

]
