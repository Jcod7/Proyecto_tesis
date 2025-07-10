from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    
    ROLE_CHOICES = [
        ('ADMIN', 'Administrador'),
        ('MECANICO', 'Mecánico'),
        ('RECEPCIONISTA', 'Recepcionista'),
        ('GERENTE', 'Gerente'),
    ]
    
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default='MECANICO')
    telefono = models.CharField(max_length=20, blank=True)
    activo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        help_text=_('The groups this user belongs to.'),
        related_name='customuser_set',
    )

    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name='customuser_permissions_set',
    )
    
    def __str__(self):
        return f"{self.username} - {self.get_role_display()}"
    
    def get_nombre_completo(self):
        return f"{self.first_name} {self.last_name}".strip() or self.username
