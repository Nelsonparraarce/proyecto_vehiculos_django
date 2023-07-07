from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('vehiculo/add/', views.add_vehiculo, name='add_vehiculo'),
    path('vehiculos/', views.listar_vehiculos, name='listar_vehiculos'),
    path('login/', views.login_view, name='login'),
    path('registro', views.registro_view, name='registro'),
    path('logout', views.logout_view, name='logout'),

]
