from django.contrib import admin
from .models import Categoria, NombreProducto, Producto, EntradaCompra, DetalleEntradaCompra, AjusteInventario


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'activa', 'fecha_creacion']
    list_filter = ['activa']
    search_fields = ['nombre', 'descripcion']
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion']


@admin.register(NombreProducto)
class NombreProductoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'categoria', 'unidad_medida', 'activo', 'fecha_creacion']
    list_filter = ['categoria', 'activo']
    search_fields = ['nombre', 'descripcion']
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion']
    fieldsets = (
        ('Información Básica', {
            'fields': ('nombre', 'categoria', 'unidad_medida', 'descripcion')
        }),
        ('Estado', {
            'fields': ('activo',)
        }),
        ('Fechas', {
            'fields': ('fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )


class DetalleEntradaCompraInline(admin.TabularInline):
    model = DetalleEntradaCompra
    extra = 1
    fields = ['producto', 'cantidad', 'precio_unitario', 'subtotal']
    readonly_fields = ['subtotal']


@admin.register(EntradaCompra)
class EntradaCompraAdmin(admin.ModelAdmin):
    list_display = ['id', 'numero_factura', 'proveedor', 'fecha_compra', 'total', 'usuario_registro']
    list_filter = ['fecha_compra', 'usuario_registro']
    search_fields = ['numero_factura', 'proveedor']
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion', 'total']
    inlines = [DetalleEntradaCompraInline]
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.usuario_registro = request.user
        super().save_model(request, obj, form, change)


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'nombre_producto', 'categoria', 'precio_venta', 'stock_actual', 'stock_minimo', 'activo']
    list_filter = ['categoria', 'activo', 'nombre_producto']
    search_fields = ['codigo', 'nombre_producto__nombre', 'descripcion']
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion']
    fieldsets = (
        ('Información Básica', {
            'fields': ('codigo', 'nombre_producto', 'descripcion', 'categoria')
        }),
        ('Precios', {
            'fields': ('precio_compra', 'costo_promedio', 'porcentaje_ganancia', 'precio_venta', 'actualizar_precio_automatico')
        }),
        ('Inventario', {
            'fields': ('stock_actual', 'stock_minimo')
        }),
        ('Estado', {
            'fields': ('activo',)
        }),
        ('Fechas', {
            'fields': ('fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )


@admin.register(AjusteInventario)
class AjusteInventarioAdmin(admin.ModelAdmin):
    list_display = ['producto', 'tipo_ajuste', 'cantidad_anterior', 'cantidad_nueva', 'diferencia', 'usuario_registro', 'fecha_ajuste']
    list_filter = ['tipo_ajuste', 'fecha_ajuste', 'usuario_registro']
    search_fields = ['producto__nombre_producto__nombre', 'producto__codigo', 'motivo']
    readonly_fields = ['diferencia', 'fecha_creacion']
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.usuario_registro = request.user
        super().save_model(request, obj, form, change)

