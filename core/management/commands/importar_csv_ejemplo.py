"""
Comando para importar datos de ejemplo desde los CSV en datos_ejemplo/.
Uso: python manage.py importar_csv_ejemplo [--ruta datos_ejemplo]
Requisito: Tener al menos un usuario en el sistema (para asignar como vendedor en facturas).
"""
import csv
import os
from datetime import datetime
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db import transaction

from inventario.models import Categoria, NombreProducto, Producto, Proveedor
from ventas.models import Cliente, Factura, DetalleFactura
from usuarios.models import Usuario


class Command(BaseCommand):
    help = 'Importa datos de ejemplo desde CSV (categorías, productos, clientes, proveedores, ventas)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--ruta',
            type=str,
            default='datos_ejemplo',
            help='Carpeta donde están los CSV (por defecto: datos_ejemplo)',
        )
        parser.add_argument(
            '--limpiar',
            action='store_true',
            help='Eliminar datos existentes antes de importar (Factura, DetalleFactura, Producto, NombreProducto, Cliente, Proveedor, Categoria)',
        )

    def _ruta_csv(self, nombre, ruta_base):
        return os.path.join(ruta_base, nombre)

    def _leer_csv(self, path):
        if not os.path.exists(path):
            self.stdout.write(self.style.WARNING(f'No encontrado: {path}'))
            return []
        with open(path, 'r', encoding='utf-8') as f:
            return list(csv.DictReader(f))

    @transaction.atomic
    def handle(self, *args, **options):
        ruta_base = options['ruta']
        limpiar = options['limpiar']

        if limpiar:
            self.stdout.write('Eliminando datos existentes...')
            DetalleFactura.objects.all().delete()
            Factura.objects.all().delete()
            Producto.objects.all().delete()
            NombreProducto.objects.all().delete()
            Cliente.objects.all().delete()
            Proveedor.objects.all().delete()
            Categoria.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Datos eliminados.'))

        # 1) Categorías
        path = self._ruta_csv('categorias.csv', ruta_base)
        rows = self._leer_csv(path)
        cat_by_name = {}
        for row in rows:
            c, _ = Categoria.objects.get_or_create(
                nombre=row['nombre'].strip(),
                defaults={
                    'descripcion': (row.get('descripcion') or '').strip() or None,
                    'activa': row.get('activa', 'True').strip().lower() == 'true',
                },
            )
            cat_by_name[c.nombre] = c
        if rows:
            self.stdout.write(self.style.SUCCESS(f'  Categorías: {len(rows)} procesadas.'))

        # 2) Nombres de producto
        path = self._ruta_csv('nombres_producto.csv', ruta_base)
        rows = self._leer_csv(path)
        nombre_prod_by_name = {}
        for row in rows:
            cat = cat_by_name.get((row.get('categoria') or '').strip())
            if not cat:
                self.stdout.write(self.style.WARNING(f'  Categoría no encontrada para nombre producto: {row.get("nombre")}'))
                continue
            np, _ = NombreProducto.objects.get_or_create(
                nombre=row['nombre'].strip(),
                defaults={
                    'descripcion': (row.get('descripcion') or '').strip() or None,
                    'categoria': cat,
                    'unidad_medida': (row.get('unidad_medida') or 'unidad').strip(),
                    'activo': row.get('activo', 'True').strip().lower() == 'true',
                },
            )
            nombre_prod_by_name[np.nombre] = np
        if rows:
            self.stdout.write(self.style.SUCCESS(f'  Nombres de producto: {len(rows)} procesados.'))

        # 3) Productos
        path = self._ruta_csv('productos.csv', ruta_base)
        rows = self._leer_csv(path)
        prod_by_codigo = {}
        for row in rows:
            np = nombre_prod_by_name.get((row.get('nombre_producto') or '').strip())
            cat = cat_by_name.get((row.get('categoria') or '').strip())
            if not np or not cat:
                self.stdout.write(self.style.WARNING(f'  Nombre/categoría no encontrado para producto: {row.get("codigo")}'))
                continue
            fe = (row.get('fecha_expiracion') or '').strip()
            try:
                fecha_expiracion = datetime.strptime(fe, '%Y-%m-%d').date() if fe else None
            except ValueError:
                fecha_expiracion = None
            p, _ = Producto.objects.get_or_create(
                codigo=row['codigo'].strip(),
                defaults={
                    'nombre_producto': np,
                    'categoria': cat,
                    'descripcion': (row.get('descripcion') or '').strip() or None,
                    'precio_venta': Decimal(row.get('precio_venta', 0)),
                    'precio_compra': Decimal(row.get('precio_compra', 0)),
                    'stock_actual': int(row.get('stock_actual', 0)),
                    'stock_minimo': int(row.get('stock_minimo', 0)),
                    'unidades_por_paquete': int(row.get('unidades_por_paquete', 1)),
                    'porcentaje_ganancia': Decimal(row.get('porcentaje_ganancia', 30)),
                    'fecha_expiracion': fecha_expiracion,
                    'activo': row.get('activo', 'True').strip().lower() == 'true',
                },
            )
            prod_by_codigo[p.codigo] = p
        if rows:
            self.stdout.write(self.style.SUCCESS(f'  Productos: {len(rows)} procesados.'))

        # 4) Clientes
        path = self._ruta_csv('clientes.csv', ruta_base)
        rows = self._leer_csv(path)
        cliente_by_nombre = {}
        for row in rows:
            nombre = row['nombre'].strip()
            c, _ = Cliente.objects.get_or_create(
                nombre=nombre,
                defaults={
                    'cedula': (row.get('cedula') or '').strip() or None,
                    'telefono': (row.get('telefono') or '').strip() or None,
                    'email': (row.get('email') or '').strip() or None,
                    'direccion': (row.get('direccion') or '').strip() or None,
                    'tipo_cliente': (row.get('tipo_cliente') or 'REGULAR').strip(),
                    'activo': row.get('activo', 'True').strip().lower() == 'true',
                },
            )
            cliente_by_nombre[c.nombre] = c
        if rows:
            self.stdout.write(self.style.SUCCESS(f'  Clientes: {len(rows)} procesados.'))

        # 5) Proveedores
        path = self._ruta_csv('proveedores.csv', ruta_base)
        rows = self._leer_csv(path)
        for row in rows:
            Proveedor.objects.get_or_create(
                nombre=row['nombre'].strip(),
                defaults={
                    'ruc': (row.get('ruc') or '').strip() or None,
                    'contacto': (row.get('contacto') or '').strip() or None,
                    'telefono': (row.get('telefono') or '').strip() or None,
                    'email': (row.get('email') or '').strip() or None,
                    'direccion': (row.get('direccion') or '').strip() or None,
                    'activo': row.get('activo', 'True').strip().lower() == 'true',
                },
            )
        if rows:
            self.stdout.write(self.style.SUCCESS(f'  Proveedores: {len(rows)} procesados.'))

        # 6) Facturas (necesitan vendedor = primer usuario)
        vendedor = Usuario.objects.first()
        if not vendedor:
            self.stdout.write(
                self.style.ERROR('No hay usuarios en el sistema. Crea un usuario (ej. superusuario) y vuelve a ejecutar.')
            )
            return

        path = self._ruta_csv('facturas.csv', ruta_base)
        rows = self._leer_csv(path)
        factura_by_numero = {}
        for row in rows:
            num = (row.get('numero_factura') or '').strip()
            if not num:
                continue
            cliente_nombre = (row.get('cliente_nombre') or '').strip()
            cliente = cliente_by_nombre.get(cliente_nombre)
            fac, _ = Factura.objects.get_or_create(
                numero_factura=num,
                defaults={
                    'cliente': cliente,
                    'cliente_nombre': cliente_nombre if not cliente else None,
                    'vendedor': vendedor,
                    'fecha_venta': timezone.now(),
                    'subtotal': Decimal('0'),
                    'descuento': Decimal(row.get('descuento', 0)),
                    'total': Decimal('0'),
                    'estado': (row.get('estado') or 'COMPLETADA').strip(),
                    'observaciones': (row.get('observaciones') or '').strip() or None,
                },
            )
            factura_by_numero[fac.numero_factura] = fac
        if rows:
            self.stdout.write(self.style.SUCCESS(f'  Facturas: {len(rows)} procesadas.'))

        # 7) Detalle facturas
        path = self._ruta_csv('detalle_facturas.csv', ruta_base)
        rows = self._leer_csv(path)
        creados = 0
        for row in rows:
            num = (row.get('numero_factura') or '').strip()
            cod = (row.get('codigo_producto') or '').strip()
            factura = factura_by_numero.get(num)
            producto = prod_by_codigo.get(cod)
            if not factura or not producto:
                continue
            cantidad = int(row.get('cantidad', 1))
            precio = Decimal(row.get('precio_unitario', 0))
            _, created = DetalleFactura.objects.get_or_create(
                factura=factura,
                producto=producto,
                defaults={
                    'cantidad': cantidad,
                    'precio_unitario': precio,
                    'subtotal': cantidad * precio,
                },
            )
            if created:
                creados += 1
        if rows:
            self.stdout.write(self.style.SUCCESS(f'  Detalles de factura: {creados} creados (totales recalculados por el sistema).'))

        self.stdout.write(self.style.SUCCESS('\nImportación desde CSV completada.'))
