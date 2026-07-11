from django.db import models
import uuid

class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    celular = models.CharField(max_length=15, unique=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre

class Motocicleta(models.Model):
    placa = models.CharField(max_length=10, unique=True)
    modelo = models.CharField(max_length=100)
    propietario = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='motos')

    def __str__(self):
        return f"{self.placa} - {self.modelo}"

class OrdenTrabajo(models.Model):
    ESTADOS = [
        ('taller', 'En Taller'),
        ('listo', 'Listo para Retiro'),
        ('entregado', 'Entregado'),
    ]

    hash_seguimiento = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    moto = models.ForeignKey(Motocicleta, on_delete=models.CASCADE)
    fecha_ingreso = models.DateTimeField(auto_now_add=True)
    fecha_entrega = models.DateTimeField(null=True, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='taller')
    audio_nota = models.FileField(upload_to='audios/', null=True, blank=True) # Para el Bloque 4
    total_cobro = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Orden {self.id} - {self.moto.placa}"

class Cotizacion(models.Model):
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('aprobada', 'Aprobada'),
        ('rechazada', 'Rechazada'),
    ]
    orden = models.ForeignKey(OrdenTrabajo, on_delete=models.CASCADE, related_name='cotizaciones')
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    contexto = models.TextField(blank=True)
    foto_evidencia = models.FileField(upload_to='cotizaciones/', null=True, blank=True)
    fecha_envio = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cotización #{self.id} - Orden #{self.orden_id} - {self.estado}"


class ItemCotizacion(models.Model):
    cotizacion = models.ForeignKey(Cotizacion, on_delete=models.CASCADE, related_name='items')
    descripcion = models.CharField(max_length=255)
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.descripcion}: ${self.precio}"


class EventoMuro(models.Model):
    TIPOS = [
        ('foto', 'Foto de Evidencia'),
        ('nota', 'Nota de Voz'),
        ('tarea', 'Tarea Completada'),
    ]
    orden = models.ForeignKey(OrdenTrabajo, on_delete=models.CASCADE, related_name='eventos')
    tipo = models.CharField(max_length=10, choices=TIPOS)
    contenido_texto = models.TextField(blank=True)
    # Para guardar permanentemente si la tarea se hizo
    completada = models.BooleanField(default=False) 
    archivo = models.FileField(upload_to='muro/', null=True, blank=True)
    fecha = models.DateTimeField(auto_now_add=True)