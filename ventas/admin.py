from django.contrib import admin
from .models import Cliente, Factura, DetalleFactura


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'cedula', 'telefono', 'tipo_cliente', 'activo', 'fecha_creacion']
    list_filter = ['tipo_cliente', 'activo']
    search_fields = ['nombre', 'cedula', 'telefono', 'email']
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion']


class DetalleFacturaInline(admin.TabularInline):
    model = DetalleFactura
    extra = 1
    fields = ['producto', 'cantidad', 'precio_unitario', 'subtotal']
    readonly_fields = ['subtotal']
    autocomplete_fields = ['producto']


@admin.register(Factura)
class FacturaAdmin(admin.ModelAdmin):
    list_display = ['numero_factura', 'cliente_display', 'vendedor', 'fecha_venta', 'total', 'estado']
    list_filter = ['estado', 'fecha_venta', 'vendedor']
    search_fields = ['numero_factura', 'cliente__nombre', 'cliente_nombre']
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion', 'subtotal', 'total']
    inlines = [DetalleFacturaInline]
    autocomplete_fields = ['cliente']
    
    def cliente_display(self, obj):
        return obj.cliente.nombre if obj.cliente else (obj.cliente_nombre or 'Cliente General')
    cliente_display.short_description = 'Cliente'
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.vendedor = request.user
        super().save_model(request, obj, form, change)


@admin.register(DetalleFactura)
class DetalleFacturaAdmin(admin.ModelAdmin):
    list_display = ['factura', 'producto', 'cantidad', 'precio_unitario', 'subtotal']
    list_filter = ['factura__fecha_venta']
    search_fields = ['factura__numero_factura', 'producto__nombre', 'producto__codigo']
    readonly_fields = ['subtotal']

