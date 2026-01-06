# Sistema de Información - Minisúper D'Pérez

Sistema web de gestión para facturación, control de inventario y ciencia de datos desarrollado con Django 5.x y PostgreSQL.

## Características

- **Gestión de Usuarios y Roles**: Sistema de autenticación con roles (Administrador, Vendedor, Bodeguero)
- **Control de Inventario**: Gestión completa de productos, categorías, entradas de compra y ajustes
- **Facturación**: Sistema de ventas con facturas y clientes
- **Ciencia de Datos**: Registro de productos recomendados para futuros modelos de ML
- **Descuento Automático de Stock**: Signals que actualizan el inventario automáticamente al facturar

## Stack Tecnológico

- **Backend**: Django 5.x con Python
- **Base de Datos**: PostgreSQL
- **Frontend**: Tailwind CSS

## Requisitos Previos

- Python 3.10 o superior
- PostgreSQL 12 o superior
- pip (gestor de paquetes de Python)

## Instalación

1. **Clonar el repositorio** (o navegar al directorio del proyecto)

2. **Crear y activar un entorno virtual**:
   ```bash
   python -m venv env
   # Windows
   env\Scripts\activate
   # Linux/Mac
   source env/bin/activate
   ```

3. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar variables de entorno**:
   - Copiar `.env.example` a `.env`
   - Editar `.env` con tus credenciales de PostgreSQL:
     ```
     DB_NAME=sistemainventario_db
     DB_USER=tu_usuario
     DB_PASSWORD=tu_contraseña
     DB_HOST=localhost
     DB_PORT=5432
     ```

5. **Crear la base de datos en PostgreSQL**:
   ```sql
   CREATE DATABASE sistemainventario_db;
   ```

6. **Ejecutar migraciones**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

7. **Crear un superusuario**:
   ```bash
   python manage.py createsuperuser
   ```

8. **Ejecutar el servidor de desarrollo**:
   ```bash
   python manage.py runserver
   ```

9. **Acceder al sistema**:
   - Admin: http://127.0.0.1:8000/admin/
   - API/Interfaz: http://127.0.0.1:8000/

## Estructura del Proyecto

```
sistemainventariomini/
├── sistemainventario/      # Configuración del proyecto
│   ├── settings.py         # Configuración principal
│   ├── urls.py             # URLs principales
│   └── ...
├── usuarios/               # App de usuarios y roles
│   ├── models.py           # Usuario personalizado y Rol
│   └── ...
├── inventario/             # App de inventario
│   ├── models.py           # Producto, Categoría, EntradaCompra, AjusteInventario
│   └── ...
├── ventas/                 # App de facturación
│   ├── models.py           # Cliente, Factura, DetalleFactura
│   └── signals.py          # Signals para descuento automático de stock
├── ciencia_datos/          # App de ciencia de datos
│   └── models.py           # ProductosRecomendados
└── manage.py
```

## Modelos Principales

### Usuarios
- **Usuario**: Modelo de usuario personalizado con roles
- **Rol**: Roles del sistema (Administrador, Vendedor, Bodeguero)

### Inventario
- **Categoria**: Categorías de productos
- **Producto**: Productos con stock, precios y stock mínimo
- **EntradaCompra**: Registro de compras a proveedores
- **DetalleEntradaCompra**: Detalles de cada compra
- **AjusteInventario**: Ajustes manuales o automáticos de inventario

### Ventas
- **Cliente**: Clientes del sistema
- **Factura**: Facturas de venta
- **DetalleFactura**: Detalles de productos vendidos

### Ciencia de Datos
- **ProductosRecomendados**: Logs de recomendaciones de ML

## Funcionalidades Clave

### Signals Automáticos

1. **Descuento de Stock al Facturar**: Cuando se crea un `DetalleFactura` con estado `COMPLETADA`, el stock se descuenta automáticamente.

2. **Restauración de Stock**: Si se elimina un detalle de factura o se anula una factura, el stock se restaura automáticamente.

3. **Aumento de Stock al Comprar**: Cuando se registra una `EntradaCompra`, el stock aumenta automáticamente.

## Moneda

El sistema está configurado para usar **Córdobas Nicaragüenses (NIO)** con símbolo **C$**.

## Próximos Pasos

- Implementar interfaz de usuario con Tailwind CSS
- Crear dashboard con reportes básicos
- Implementar módulo de reportes (Ventas del día, productos por agotarse)
- Integrar modelos de Machine Learning para recomendaciones

## Licencia

Proyecto de graduación - Minisúper D'Pérez

