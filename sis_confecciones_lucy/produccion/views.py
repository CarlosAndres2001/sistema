from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Categoria, Subcategoria,Producto, ProductoInsumo, Insumo
from django.http import HttpResponse


def gestionar_categorias(request):
    categorias = Categoria.objects.all()
    return render(request, 'produccion/categorias.html', {'categorias': categorias})

def crear_categoria(request):
    if request.method == 'POST':
        nombre_categoria = request.POST.get('nombre_categoria')
        if nombre_categoria:
            if Categoria.objects.filter(nombre_categoria=nombre_categoria).exists():
                messages.error(request, 'La categoría ya existe.')
            else:
                Categoria.objects.create(nombre_categoria=nombre_categoria)
                messages.success(request, 'Categoría creada exitosamente.')
        else:
            messages.error(request, 'El nombre de la categoría no puede estar vacío.')
        return redirect('gestionar_categorias')

def crear_subcategoria(request):
    if request.method == 'POST':
        nombre_subcategoria = request.POST.get('nombre_subcategoria')
        id_categoria = request.POST.get('id_categoria')

        if nombre_subcategoria and id_categoria:
            try:
                categoria = Categoria.objects.get(id_categoria=id_categoria)
                if Subcategoria.objects.filter(nombre_subcategoria=nombre_subcategoria, id_categoria=categoria).exists():
                    messages.error(request, 'La subcategoría ya existe en esta categoría.')
                else:
                    Subcategoria.objects.create(nombre_subcategoria=nombre_subcategoria, id_categoria=categoria)
                    messages.success(request, 'Subcategoría creada exitosamente.')
            except Categoria.DoesNotExist:
                messages.error(request, 'La categoría seleccionada no existe.')
        else:
            messages.error(request, 'Debe completar todos los campos para crear una subcategoría.')
        return redirect('gestionar_categorias')

def listar_categorias(request):
    categorias = Categoria.objects.all()
    return render(request, 'produccion/lista_categorias.html', {'categorias': categorias})

def crear_producto(request):
    if request.method == 'POST':
        nombre_producto = request.POST.get('nombre_producto')
        costo = request.POST.get('costo')
        precio_venta = request.POST.get('precio_venta')
        id_subcategoria = request.POST.get('id_subcategoria')

        try:
            subcategoria = Subcategoria.objects.get(id_subcategoria=id_subcategoria)
        except Subcategoria.DoesNotExist:
            return HttpResponse("Subcategoría no encontrada", status=400)

        producto = Producto(
            nombre_producto=nombre_producto,
            costo=costo,
            precio_venta=precio_venta,
            id_subcategoria=subcategoria,
            unida_medida=request.POST.get('unida_medida'),
            estado=request.POST.get('estado'),
        )
        producto.save()
        
        i = 0
        while True:
            insumo_id = request.POST.get(f'insumo_{i}')
            cantidad = request.POST.get(f'cantidad_{i}')
            if not insumo_id or not cantidad:
                break  
            
            try:
                insumo = Insumo.objects.get(id_insumo=insumo_id)
            except Insumo.DoesNotExist:
                continue  

            ProductoInsumo.objects.create(
                id_producto=producto,
                id_insumo=insumo,
                cantidad=cantidad,
            )
            i += 1
        
        messages.success(request, "Producto creado correctamente.") 
        return redirect('crear_producto')

    subcategorias = Subcategoria.objects.all()
    insumos = Insumo.objects.all()
    return render(request, 'produccion/productos.html', {'subcategorias': subcategorias, 'insumos': insumos})
