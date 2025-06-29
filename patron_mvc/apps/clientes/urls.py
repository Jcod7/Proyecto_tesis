from django.urls import path
from . import views

app_name = 'clientes'

urlpatterns = [
    path('', views.cliente_list, name='list'),
    path('crear/', views.cliente_create, name='create'),
    path('<int:pk>/', views.cliente_detail, name='detail'),
]