from django.urls import path
from . import views

app_name = 'vehiculos'

urlpatterns = [
    path('', views.vehiculo_list, name='list'),
    path('crear/', views.vehiculo_create, name='create'),
    path('<int:pk>/', views.vehiculo_detail, name='detail'),
]
