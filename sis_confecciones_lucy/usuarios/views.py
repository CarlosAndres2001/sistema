from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Persona, Usuario, Rol
from django.contrib.auth.hashers import make_password
from django.db import transaction    
from django.contrib.auth import authenticate, login


def usuarios(request):    
    return render(request, 'usuarios/usuario.html')

def crear_rol(request):
    if request.method == 'POST':
        nombre_rol = request.POST.get('nombre_rol')
        if nombre_rol:
            rol = Rol(nombre_rol=nombre_rol)
            rol.save()
            messages.success(request, "Rol creado exitosamente.")
            return redirect('registrar_usuario') 
        else:
            messages.error(request, "El nombre del rol es obligatorio.")
            return render(request, 'usuarios/usuario.html')
    return render(request, 'usuarios/usuario.html')
   

def registrar_usuario(request):
    roles = Rol.objects.all()  
    if request.method == 'POST':
        try:
            with transaction.atomic():  

                nombre = request.POST.get('nombre')
                apellido = request.POST.get('apellido')
                fecha_nac = request.POST.get('fecha_nac')
                cedula_identidad = request.POST.get('cedula_identidad')

                persona = Persona.objects.create(
                    nombre=nombre,
                    apellido=apellido,
                    fecha_nac=fecha_nac if fecha_nac else None,
                    cedula_identidad=cedula_identidad
                )

                nombre_usu = request.POST.get('nombre_usu')
                contrasena = request.POST.get('contrasena')  
                estado = request.POST.get('estado')
                id_rol = request.POST.get('roles') 

                if not id_rol:
                    messages.error(request, 'Debe seleccionar un rol.')
                    return redirect('registrar_usuario')

                contrasena_hashed = make_password(contrasena)

                try:
                    rol = Rol.objects.get(id_rol=id_rol)
                except Rol.DoesNotExist:
                    messages.error(request, 'Rol no encontrado.')
                    return redirect('registrar_usuario')

                Usuario.objects.create(
                    nombre_usu=nombre_usu,
                    contrasena=contrasena_hashed,  
                    estado=estado,
                    id_rol=rol,
                    id_persona=persona
                )

                messages.success(request, 'Usuario registrado exitosamente.')
                return redirect('registrar_usuario')

        except Exception as e:
            messages.error(request, f'Error al registrar usuario: {e}')
            return redirect('registrar_usuario')
    
    else:
        return render(request, 'usuarios/usuario.html', {'roles': roles})

    

