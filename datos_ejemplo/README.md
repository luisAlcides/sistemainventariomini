# Datos de ejemplo para importación CSV

Esta carpeta contiene archivos CSV con **más de 100 registros** repartidos en todas las áreas del sistema:

| Archivo | Registros | Descripción |
|---------|-----------|-------------|
| `categorias.csv` | 8 | Categorías de productos (Abarrotes, Lácteos, Bebidas, etc.) |
| `nombres_producto.csv` | 25 | Nombres de producto del catálogo (por categoría) |
| `productos.csv` | 27 | Productos con código, precios y stock |
| `clientes.csv` | 25 | Clientes (nombre, cédula, teléfono, tipo, etc.) |
| `proveedores.csv` | 25 | Proveedores (nombre, RUC, contacto, etc.) |
| `facturas.csv` | 20 | Facturas de venta (número, cliente, descuento, estado) |
| `detalle_facturas.csv` | 46 | Líneas de detalle (producto, cantidad, precio por factura) |

**Total: más de 176 registros** entre todas las áreas.

## Cómo importar

Desde la raíz del proyecto (donde está `manage.py`):

```bash
# Importar todos los CSV (por defecto busca la carpeta datos_ejemplo)
python manage.py importar_csv_ejemplo

# Especificar otra carpeta
python manage.py importar_csv_ejemplo --ruta ruta/a/mis/csv

# Borrar datos existentes de estas tablas y luego importar
python manage.py importar_csv_ejemplo --limpiar
```

**Requisito:** Debe existir al menos un usuario en el sistema (por ejemplo, creado con `createsuperuser`). Ese usuario se usará como vendedor en las facturas importadas.

El comando importa en este orden: Categorías → Nombres de producto → Productos → Clientes → Proveedores → Facturas → Detalles de factura. Los totales de las facturas se recalculan automáticamente al crear los detalles.
