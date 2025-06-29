from django.urls import path
from . import views

app_name = 'ordenes'

urlpatterns = [
    path('', views.orden_list, name='list'),
    path('crear/', views.orden_create, name='create'),
    path('<int:pk>/', views.orden_detail, name='detail'),
    path('ajax/vehiculos/', views.load_vehiculos, name='load_vehiculos'),
]