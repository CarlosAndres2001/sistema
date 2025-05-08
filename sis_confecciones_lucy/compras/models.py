from django.db import models

from usuarios.models import UsuarioManager, Usuario

class Insumo(models.Model):
    id_insumo = models.AutoField(primary_key=True)
    nombre_insumo = models.CharField(max_length=100, db_collation='Modern_Spanish_CI_AS')
    descripcion = models.TextField(db_collation='Modern_Spanish_CI_AS', blank=True, null=True)
    color = models.CharField(max_length=50, db_collation='Modern_Spanish_CI_AS') 
    unidad_medida = models.CharField(max_length=20, db_collation='Modern_Spanish_CI_AS') 

    class Meta:
        managed = False
        db_table = 'INSUMO'

class Proveedor(models.Model):
    id_proveedor = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, db_collation='Modern_Spanish_CI_AS')
    direccion = models.TextField(db_collation='Modern_Spanish_CI_AS', blank=True, null=True)
    telefono = models.CharField(max_length=15, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'PROVEEDOR'
        
class Compra(models.Model):
    id_compra = models.AutoField(primary_key=True)
    fecha_hora = models.DateTimeField()
    monto_total = models.DecimalField(max_digits=10, decimal_places=2)
    id_proveedor = models.ForeignKey('Proveedor', on_delete=models.DO_NOTHING, db_column='id_proveedor')
    id_usuario = models.ForeignKey('usuarios.Usuario', on_delete=models.DO_NOTHING, db_column='id_usuario')
    estado = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        db_table = 'COMPRA'
        
class DetalleCompra(models.Model):
    id_detalle_compra = models.AutoField(primary_key=True)
    id_compra = models.ForeignKey(Compra, on_delete=models.CASCADE, related_name='detalles', db_column='id_compra')
    id_insumo = models.ForeignKey('Insumo', on_delete=models.DO_NOTHING, db_column='id_insumo')
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'DETALLE_COMPRA'

class SolicitudCompra(models.Model):
    id_solicitud_compra = models.AutoField(primary_key=True)
    estado = models.CharField(max_length=80, null=True, blank=True) 
    fecha = models.DateTimeField(auto_now_add=True)  
    id_usuario = models.ForeignKey('usuarios.Usuario', on_delete=models.DO_NOTHING, db_column='id_usuario')
    
    class Meta:
        managed = False
        db_table = 'SOLICITUD_COMPRA'

class DetalleSolicitud(models.Model):
    id_detalle_solicitud = models.AutoField(primary_key=True)
    id_solicitud_compra = models.ForeignKey(SolicitudCompra, on_delete=models.CASCADE, related_name='detalles', db_column='id_solicitud_compra')
    id_insumo = models.ForeignKey('Insumo', on_delete=models.DO_NOTHING, db_column='id_insumo')
    cantidad = models.PositiveIntegerField()  
    
    class Meta:
        managed = False
        db_table = 'DETALLE_SOLICITUD'
        
class Deposito(models.Model):
    id_deposito = models.AutoField(primary_key=True)
    nombre_deposito = models.CharField(max_length=100, db_collation='Modern_Spanish_CI_AS')

    class Meta:
        managed = False
        db_table = 'DEPOSITO'

class Lote(models.Model):
    id_lote = models.AutoField(primary_key=True)
    fecha_lote = models.DateField()
    id_compra = models.ForeignKey(Compra, on_delete=models.DO_NOTHING, db_column='id_compra')
    id_deposito = models.ForeignKey(Deposito, on_delete=models.DO_NOTHING, db_column='id_deposito')

    class Meta:
        managed = False
        db_table = 'LOTE'

class FichaRecepcion(models.Model):
    id_ficha_recepcion = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey('usuarios.Usuario', on_delete=models.DO_NOTHING, db_column='id_usuario')
    fecha_hora = models.DateTimeField()
    id_compra = models.ForeignKey(Compra, on_delete=models.DO_NOTHING, db_column='id_compra')
    estado = models.CharField(max_length=30, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'FICHA_RECEPCION'


class CasaCambioCompra(models.Model):
    id_operacion = models.AutoField(primary_key=True)
    fecha = models.DateTimeField()
    corte_100 = models.IntegerField()
    corte_50 = models.IntegerField()
    corte_20 = models.IntegerField()
    corte_10 = models.IntegerField()
    corte_5 = models.IntegerField()
    corte_1 = models.IntegerField()
    total_calculado = models.IntegerField()
    id_usuario = models.IntegerField()
    observaciones = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'casa_cambio_compra'