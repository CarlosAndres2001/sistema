from django.db import models
from produccion.models import Producto
from usuarios.models import Usuario

class Cliente(models.Model):
    id_cliente = models.AutoField(primary_key=True)
    nombre_cliente = models.CharField(max_length=100)
    nro_documento = models.CharField(unique=True, max_length=20)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    estado = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        db_table = 'CLIENTE'

class FichaEntrega(models.Model):
    id_ficha_entrega = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey('usuarios.Usuario', models.DO_NOTHING, db_column='id_usuario')
    fecha_hora = models.DateTimeField()
    id_pedido = models.ForeignKey('Pedido', models.DO_NOTHING, db_column='id_pedido')
    estado = models.CharField(max_length=25, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'FICHA_ENTREGA'

class Pedido(models.Model):
    id_pedido = models.AutoField(primary_key=True)
    id_cliente = models.ForeignKey(Cliente, models.DO_NOTHING, db_column='id_cliente')
    id_usuario = models.ForeignKey('usuarios.Usuario', models.DO_NOTHING, db_column='id_usuario')
    fecha_hora = models.DateTimeField()
    monto_total = models.DecimalField(max_digits=18, decimal_places=0, blank=True, null=True)
    estado = models.CharField(max_length=30, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)
    descuento = models.DecimalField(max_digits=18, decimal_places=0, blank=True, null=True)
    

    class Meta:
        managed = False
        db_table = 'PEDIDO'

class DetallePedido(models.Model):
    id_detalle_pedido = models.AutoField(primary_key=True)
    id_producto = models.ForeignKey('produccion.Producto', models.DO_NOTHING, db_column='id_producto')
    cantidad_producto = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=18, decimal_places=0)
    id_pedido = models.ForeignKey(Pedido, models.DO_NOTHING, db_column='id_pedido')

    class Meta:
        managed = False
        db_table = 'DETALLE_PEDIDO'
        
class DetalleDevolucion(models.Model):
    id_detalle_devolucion = models.AutoField(primary_key=True)
    id_producto = models.ForeignKey('produccion.Producto', models.DO_NOTHING, db_column='id_producto')
    cantidad = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'DETALLE_DEVOLUCION'

class Devolucion(models.Model):
    id_devolucion = models.AutoField(primary_key=True)
    id_cliente = models.ForeignKey(Cliente, models.DO_NOTHING, db_column='id_cliente')
    id_usuario = models.ForeignKey('usuarios.Usuario', models.DO_NOTHING, db_column='id_usuario')
    fecha_hora = models.DateTimeField()
    descripcion_motivo = models.TextField(db_collation='Modern_Spanish_CI_AS', blank=True, null=True)
    id_detalle_devolucion = models.ForeignKey(DetalleDevolucion, models.DO_NOTHING, db_column='id_detalle_devolucion')
    estado = models.CharField(max_length=30, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'DEVOLUCION'

class MetodoPago(models.Model):
    id_metodo_pago = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=50, db_collation='Modern_Spanish_CI_AS')

    class Meta:
        managed = False
        db_table = 'METODO_PAGO'

class Pago(models.Model):
    id_pago = models.AutoField(primary_key=True)
    id_metodo_pago = models.ForeignKey(MetodoPago, models.DO_NOTHING, db_column='id_metodo_pago')
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_pago = models.DateTimeField()
    id_pedido = models.ForeignKey('Pedido', models.DO_NOTHING, db_column='id_pedido')
    estado = models.CharField(max_length=30, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'PAGO'

class DetalleReposicion(models.Model):
    id_detalle_reposicion = models.AutoField(primary_key=True)
    id_producto = models.ForeignKey('produccion.Producto', models.DO_NOTHING, db_column='id_producto')
    cantidad = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'DETALLE_REPOSICION'
        
class Reposicion(models.Model):
    id_reposicion = models.AutoField(primary_key=True)
    id_cliente = models.ForeignKey(Cliente, models.DO_NOTHING, db_column='id_cliente')
    id_usuario = models.ForeignKey('usuarios.Usuario', models.DO_NOTHING, db_column='id_usuario')
    fecha_hora = models.DateTimeField()
    descripcion_motivo = models.TextField(db_collation='Modern_Spanish_CI_AS', blank=True, null=True)
    id_detalle_devolucion = models.ForeignKey(DetalleDevolucion, models.DO_NOTHING, db_column='id_detalle_devolucion')
    id_devolucion = models.ForeignKey(Devolucion, models.DO_NOTHING, db_column='id_devolucion')
    estado = models.CharField(max_length=30, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'REPOSICION'

class CasaCambio(models.Model):
    id_operacion = models.AutoField(primary_key=True)
    fecha = models.DateTimeField()
    corte_100 = models.IntegerField()
    corte_50 = models.IntegerField()
    corte_20 = models.IntegerField()
    corte_10 = models.IntegerField()
    corte_5 = models.IntegerField()
    corte_1 = models.IntegerField()
    total_calculado = models.DecimalField(max_digits=10, decimal_places=2)
    id_usuario = models.IntegerField()
    estado = models.IntegerField()
    id_moneda = models.IntegerField()
    observaciones = models.CharField(max_length=255)
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'casa_cambio'