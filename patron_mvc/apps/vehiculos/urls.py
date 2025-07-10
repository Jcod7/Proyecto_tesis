from django.urls import path
from . import views

app_name = 'vehiculos'

urlpatterns = [
    path('', views.vehiculo_list, name='list'),              # Para list.htm
    path('crear/', views.vehiculo_create, name='create'),    # Para form.html (crear)
    path('<int:pk>/', views.vehiculo_detail, name='detail'), # Para detail.htm
    path('<int:pk>/editar/', views.vehiculo_edit, name='edit'), # Para form.html (editar)
    path('<int:pk>/eliminar/', views.vehiculo_delete, name='delete'), # Para eliminar
]
