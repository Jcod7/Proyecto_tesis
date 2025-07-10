from django.urls import path
from . import views

app_name = 'clientes'

urlpatterns = [
    path('', views.cliente_list, name='list'),              # Para list.html
    path('crear/', views.cliente_create, name='create'),    # Para form.html (crear)
    path('<int:pk>/', views.cliente_detail, name='detail'), # Para detail.html
    path('<int:pk>/editar/', views.cliente_edit, name='edit'), # Para form.html (editar)
    path('<int:pk>/eliminar/', views.cliente_delete, name='delete'), # Para eliminar
]