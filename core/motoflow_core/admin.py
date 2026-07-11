from django.contrib import admin
from .models import Cliente, Motocicleta, OrdenTrabajo, EventoMuro

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'celular', 'fecha_registro')
    search_fields = ('nombre', 'celular')

@admin.register(Motocicleta)
class MotocicletaAdmin(admin.ModelAdmin):
    list_display = ('placa', 'modelo', 'propietario')
    search_fields = ('placa',)

admin.site.register(OrdenTrabajo)
admin.site.register(EventoMuro)