from django.db import models
from usuarios.models import Usuario
from compras.models import Insumo

class Categoria(models.Model):
    id_categoria = models.AutoField(primary_key=True)
    nombre_categoria = models.CharField(max_length=50)

    class Meta:
        db_table = 'CATEGORIA'

class Subcategoria(models.Model):
    id_subcategoria = models.AutoField(primary_key=True)
    nombre_subcategoria = models.CharField(max_length=50)
    id_categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, db_column='id_categoria')

    class Meta:
        db_table = 'SUBCATEGORIA'

class Producto(models.Model):
    id_producto = models.AutoField(primary_key=True)
    nombre_producto = models.CharField(max_length=100)
    costo = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    id_subcategoria = models.ForeignKey(Subcategoria, on_delete=models.CASCADE, db_column='id_subcategoria')
    unida_medida = models.CharField(max_length=20, blank=True, null=True)
    estado = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        db_table = 'PRODUCTO'
        
class ProductoInsumo(models.Model):
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE, db_column='id_producto')
    id_insumo = models.ForeignKey('compras.Insumo', on_delete=models.CASCADE, db_column='id_insumo')
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'PRODUCTO_INSUMO'

class DetalleTraspaso(models.Model):
    id_detalle_traspaso = models.AutoField(primary_key=True)
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE, db_column='id_producto', blank=True, null=True)
    id_insumo = models.ForeignKey('compras.Insumo', on_delete=models.CASCADE, db_column='id_insumo', blank=True, null=True)
    cantidad_insumo = models.IntegerField(blank=True, null=True)
    cantidad_producto = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'DETALLE_TRASPASO'

class Traspaso(models.Model):
    id_traspaso = models.AutoField(primary_key=True)
    fecha_hora = models.DateTimeField()
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, db_column='id_usuario')
    id_detalle_traspaso = models.ForeignKey(DetalleTraspaso, on_delete=models.CASCADE, db_column='id_detalle_traspaso')

    class Meta:
        db_table = 'TRASPASO'

class DetalleEgreso(models.Model):
    id_detalle_egreso = models.AutoField(primary_key=True)
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE, db_column='id_producto')
    cantidad = models.IntegerField()

    class Meta:
        db_table = 'DETALLE_EGRESO'

class Egreso(models.Model):
    id_egreso = models.AutoField(primary_key=True)
    fecha_hora = models.DateTimeField()
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, db_column='id_usuario')
    id_detalle_egreso = models.ForeignKey(DetalleEgreso, on_delete=models.CASCADE, db_column='id_detalle_egreso')

    class Meta:
        db_table = 'EGRESO'
