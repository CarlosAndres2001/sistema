from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class Rol(models.Model):
    id_rol = models.AutoField(primary_key=True)
    nombre_rol = models.CharField(max_length=50)

    class Meta:
        db_table = 'ROL'

class Persona(models.Model):
    id_persona = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    fecha_nac = models.DateField(blank=True, null=True)
    cedula_identidad = models.CharField(unique=True, max_length=20)

    class Meta:
        db_table = 'PERSONA'


class UsuarioManager(BaseUserManager):
    def create_user(self, nombre_usu, contrasena=None, **extra_fields):
        if not nombre_usu:
            raise ValueError('El nombre de usuario es obligatorio')
        usuario = self.model(nombre_usu=nombre_usu, **extra_fields)
        usuario.set_password(contrasena)
        usuario.save(using=self._db)
        return usuario

    def create_superuser(self, nombre_usu, contrasena=None, **extra_fields):
        extra_fields.setdefault('estado', 'activo')  
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(nombre_usu, contrasena, **extra_fields)

class Usuario(AbstractBaseUser):
    id_usuario = models.AutoField(primary_key=True)
    nombre_usu = models.CharField(max_length=50, unique=True)
    contrasena = models.CharField(max_length=100)
    id_rol = models.ForeignKey('Rol', on_delete=models.CASCADE, db_column='id_rol')
    id_persona = models.ForeignKey('Persona', on_delete=models.CASCADE, db_column='id_persona')
    estado = models.CharField(max_length=30, blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  
    is_superuser = models.BooleanField(default=False)


    USERNAME_FIELD = 'nombre_usu'
    REQUIRED_FIELDS = ['id_rol', 'id_persona'] 

    objects = UsuarioManager()

    class Meta:
        db_table = 'USUARIO'

    def __str__(self):
        return self.nombre_usu
