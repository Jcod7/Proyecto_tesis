from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    # Autenticación
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    
    # CRUD de usuarios
    path('', views.usuario_list, name='list'),
    path('crear/', views.usuario_create, name='create'),
    path('<int:pk>/', views.usuario_detail, name='detail'),
    path('<int:pk>/editar/', views.usuario_edit, name='edit'),
    path('<int:pk>/eliminar/', views.usuario_delete, name='delete'),
    path('<int:pk>/toggle-status/', views.usuario_toggle_status, name='toggle_status'),
]
