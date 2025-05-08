from django.shortcuts import render, redirect
from .models import Compra, DetalleCompra, Proveedor, Insumo, Deposito, SolicitudCompra, DetalleSolicitud, Usuario, CasaCambioCompra
from django.contrib import messages
from django.db import transaction
from django.http import HttpRequest
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

def crear_proveedor(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        direccion = request.POST['direccion']
        telefono = request.POST['telefono']
        try:
            proveedor = Proveedor.objects.create(
                nombre=nombre,
                direccion=direccion,
                telefono=telefono)
            messages.success(request, 'Proveedor creado con éxito')
            return redirect('crear_proveedor')
        except Exception as e:
            messages.error(request, 'Error al crear el proveedor')
    return render(request, 'compras/proveedor.html')

def crear_depositos(request):
    if request.method == 'POST':
        nombre_deposito = request.POST.get('nombre_deposito')
        
        try:
            deposito = Deposito.objects.create(
                nombre_deposito=nombre_deposito
            )
            messages.success(request, 'Deposito creado con exito')
            return redirect('crear_depositos')
        except Exception as e:
            messages.error(request, 'Error al crear el deposito')
            
    return render(request,'compras/depositos.html')

def crear_insumo(request):
    if request.method == 'POST':
        nombre_insumo = request.POST.get('nombre_insumo')
        descripcion = request.POST.get('descripcion')
        color = request.POST.get('color')
        unidad_medida=request.POST.get('unidad_medida')

        try:
            insumo = Insumo.objects.create(
                nombre_insumo=nombre_insumo,
                descripcion=descripcion,
                color=color,
                unidad_medida=unidad_medida
            )
            messages.success(request, "Insumo creado exitosamente.")
            return redirect('crear_insumo') 
        except Exception as e:
            messages.error(request, f"Error al crear el insumo: {e}")
    
    return render(request, 'compras/insumo.html')   

@login_required
def solicitud_compra(request):
    if request.method == 'POST':
        try:
            fecha = request.POST.get('fecha')
            estado = "Válido"
            id_usuario = request.user

            id_insumos = request.POST.getlist('id_insumo[]')
            cantidades = request.POST.getlist('cantidad[]')

            if not all([fecha, id_insumos, cantidades]):
                messages.error(request, "Por favor, completa todos los campos obligatorios.")
                return redirect('solicitud_compra')

            with transaction.atomic():
                solicitud = SolicitudCompra.objects.create(
                    estado=estado,
                    fecha=fecha,
                    id_usuario=id_usuario
                )

                for id_insumo, cantidad in zip(id_insumos, cantidades):
                    id_insumo = Insumo.objects.get(id_insumo=id_insumo)
                    DetalleSolicitud.objects.create(
                        id_solicitud_compra=solicitud,
                        id_insumo=id_insumo,
                        cantidad=cantidad
                    )

            messages.success(request, "Solicitud de compra registrada exitosamente.")
            return redirect('solicitud_compra')

        except Exception as e:
            messages.error(request, f"Error al registrar la solicitud: {e}")
            return redirect('solicitud_compra')
    if 'q' in request.GET:
        query = request.GET.get('q')
        
        insumos = Insumo.objects.filter(nombre_insumo__icontains=query)
        
        insumos_list = [
            {'id_insumo': insumo.id_insumo, 'nombre_insumo': insumo.nombre_insumo}
            for insumo in insumos
        ]
        return JsonResponse({'insumos': insumos_list})

    insumos = Insumo.objects.all()
    return render(request, 'compras/solicitud_compra.html', {'insumos': insumos,})
 
@login_required 
def registrar_compra(request):
    if request.method == 'POST':
        try:
            fecha_hora = request.POST.get('fecha_hora')
            monto_total = request.POST.get('monto_total')
            id_proveedor = request.POST.get('id_proveedor')
            id_usuario = request.user  

            id_insumos = request.POST.getlist('id_insumo[]')
            cantidades = request.POST.getlist('cantidad[]')
            precios_unitarios = request.POST.getlist('precio_unitario[]')

            if not all([fecha_hora, monto_total, id_proveedor, id_insumos]):
                messages.error(request, "Por favor, completa todos los campos obligatorios.")
                return redirect('registrar_compra')

            estado = "Válido"

            with transaction.atomic():
                proveedor = Proveedor.objects.get(id_proveedor=id_proveedor)
                compra = Compra.objects.create(
                    fecha_hora=fecha_hora,
                    monto_total=monto_total,
                    id_proveedor=proveedor,
                    id_usuario=id_usuario,
                    estado=estado
                )

                for id_insumo, cantidad, precio_unitario in zip(id_insumos, cantidades, precios_unitarios):
                    insumo = Insumo.objects.get(id_insumo=id_insumo)
                    DetalleCompra.objects.create(
                        id_compra=compra,
                        id_insumo=insumo,
                        cantidad=cantidad,
                        precio_unitario=precio_unitario
                    )

            messages.success(request, "Compra registrada exitosamente.")
            return redirect('registrar_compraa')

        except Exception as e:
            messages.error(request, f"Error al registrar la compra: {e}")
            return redirect('registrar_compraa')

    insumos = Insumo.objects.all()
    proveedores = Proveedor.objects.all()
    return render(request, 'compras/compra_casa.html')

def registrar_compraa(request):
    if request.method == 'POST':
        try:
            def to_int(valor):
                try:
                    return int(valor)
                except (ValueError, TypeError):
                    return 0  
            fecha = request.POST.get('fecha_hora')
            corte_100 = to_int(request.POST.get('corte_100'))
            corte_50 = to_int(request.POST.get('corte_50'))
            corte_20 = to_int(request.POST.get('corte_20'))
            corte_10 = to_int(request.POST.get('corte_10'))
            corte_5 = to_int(request.POST.get('corte_5'))
            corte_1 = to_int(request.POST.get('corte_1'))
            id_usuario = to_int(request.POST.get('id_usuario'))
            total_calculado = to_int(request.POST.get('total_calculado'))

            CasaCambioCompra.objects.create(
                fecha=fecha,
                corte_100=corte_100,
                corte_50=corte_50,
                corte_20=corte_20,
                corte_10=corte_10,
                corte_5=corte_5,
                corte_1=corte_1,
                id_usuario=id_usuario,
                total_calculado=total_calculado,
                observaciones=" "
            )

            messages.success(request, 'Compra registrada exitosamente.')
            return redirect('registrar_compraa')

        except Exception as e:
            messages.error(request, f'Error al registrar la compra: {str(e)}')
            return redirect('registrar_compraa')

    return render(request, 'compras/compra_casa.html')