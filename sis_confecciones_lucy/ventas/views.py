from pyexpat.errors import messages
from django.contrib import messages
from .models import Cliente, CasaCambio
from django.shortcuts import render, redirect
from datetime import datetime, date, time
from django.utils.dateparse import parse_date
from datetime import date


def clientes(request):
    return render(request, 'ventas/clientes.html')

def ventaa(request):
    return render(request, 'ventas/ventaaa.html')

def pagos(request):
    return render(request, 'ventas/pagos.html')

def registrar_cliente(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        nro_documento = request.POST.get('nit')
        telefono = request.POST.get('telefono')
        estado = request.POST.get('estado')

        if Cliente.objects.filter(nro_documento=nro_documento).exists():
            messages.error(request, 'El número de documento registrado pertenece a otro cliente.')
            return render(request, 'ventas/clientes.html')
        
        Cliente.objects.create(
            nombre_cliente=nombre,
            nro_documento=nro_documento,
            telefono=telefono,
            estado=estado
        )

        messages.success(request, 'Cliente registrado correctamente')
        return render(request, 'ventas/clientes.html')

    return render(request, 'ventas/clientes.html')

def lista_clientes(request):
    clientes = Cliente.objects.all() 
    return render(request, 'ventas/listar_clientes.html', {'clientes': clientes})
 
def registrar_venta(request):
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
            id_moneda = to_int(request.POST.get('moneda'))
            id_usuario = to_int(request.POST.get('id_usuario'))
            total_calculado = float(request.POST.get('total_calculado', 0))
            observaciones = request.POST.get('obs')
            precio_venta = float(request.POST.get('precio_unitario', 0))

            nueva_venta = CasaCambio.objects.create(
                fecha=fecha,
                corte_100=corte_100,
                corte_50=corte_50,
                corte_20=corte_20,
                corte_10=corte_10,
                corte_5=corte_5,
                corte_1=corte_1,
                id_usuario=id_usuario,
                total_calculado=total_calculado,
                id_moneda=id_moneda,
                estado=1,
                observaciones=observaciones,
                precio_venta = precio_venta
            )

            messages.success(request, 'Venta registrada exitosamente.')
            return redirect('ticket_venta', venta_id=nueva_venta.id_operacion)

        except Exception as e:
            messages.error(request, f'Error al registrar la venta: {str(e)}')
            return redirect('registrar_venta')

    return render(request, 'ventas/ventaaa.html')

def ticket_venta(request, venta_id):
    venta = CasaCambio.objects.get(id_operacion=venta_id)
    return render(request, 'ventas/comprobante_venta.html', {'venta': venta})



def lista_ventas(request):
    fecha_desde = request.GET.get('fecha_desde')
    fecha_hasta = request.GET.get('fecha_hasta')

    if fecha_desde and fecha_hasta:
        # Asegúrate de convertir a objetos date
        fecha_desde = parse_date(fecha_desde)
        fecha_hasta = parse_date(fecha_hasta)

        ventas = CasaCambio.objects.filter(fecha__date__range=(fecha_desde, fecha_hasta))
    else:
        # Si no hay filtro, solo mostrar ventas de hoy
        hoy = date.today()
        ventas = CasaCambio.objects.filter(fecha__date=hoy)

    context = {
        'ventas': ventas,
        'fecha_desde': request.GET.get('fecha_desde', ''),
        'fecha_hasta': request.GET.get('fecha_hasta', ''),
    }
    return render(request, 'ventas/reporte_ventas.html', context)

