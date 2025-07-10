from django.urls import path
from . import views

app_name = 'ordenes'

urlpatterns = [
    path('', views.orden_list, name='list'),              # Para list.html
    path('crear/', views.orden_create, name='create'),    # Para form.html (crear)
    path('<int:pk>/', views.orden_detail, name='detail'), # Para detail.html
    path('<int:pk>/editar/', views.orden_edit, name='edit'), # Para form.html (editar)
    path('<int:pk>/eliminar/', views.orden_delete, name='delete'), # Para eliminar
    path('ajax/vehiculos/', views.load_vehiculos, name='load_vehiculos'), # AJAX para cargar vehículos
]