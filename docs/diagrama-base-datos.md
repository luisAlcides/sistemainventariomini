# Diagrama de Base de Datos Relacional - Sistema de Inventario Mini

## Diagrama ER (Entidad-Relación)

```mermaid
erDiagram
    %% ========== MÓDULO USUARIOS ==========
    Rol {
        int id PK
        varchar codigo UK "ADMIN, VEND, BODEG"
        varchar nombre
        text descripcion
        bool activo
        datetime fecha_creacion
        datetime fecha_actualizacion
    }

    Usuario {
        int id PK
        varchar username UK
        varchar password
        varchar first_name
        varchar last_name
        varchar email
        varchar cedula UK
        varchar telefono
        text direccion
        int rol_id FK
        bool activo
        datetime fecha_creacion
        datetime fecha_actualizacion
    }

    %% ========== MÓDULO INVENTARIO ==========
    Categoria {
        int id PK
        varchar nombre UK
        text descripcion
        bool activa
        datetime fecha_creacion
        datetime fecha_actualizacion
    }

    NombreProducto {
        int id PK
        varchar nombre UK
        text descripcion
        int categoria_id FK
        varchar unidad_medida
        bool activo
        datetime fecha_creacion
        datetime fecha_actualizacion
    }

    Producto {
        int id PK
        varchar codigo UK
        int nombre_producto_id FK
        text descripcion
        int categoria_id FK
        decimal precio_venta
        decimal precio_compra
        decimal costo_promedio
        decimal porcentaje_ganancia
        bool actualizar_precio_automatico
        int stock_actual
        int stock_minimo
        int unidades_por_paquete
        date fecha_expiracion
        varchar unidad_medida
        bool activo
        datetime fecha_creacion
        datetime fecha_actualizacion
    }

    Proveedor {
        int id PK
        varchar nombre
        varchar ruc
        varchar contacto
        varchar telefono
        varchar email
        text direccion
        bool activo
        datetime fecha_creacion
        datetime fecha_actualizacion
    }

    EntradaCompra {
        int id PK
        varchar numero_factura
        int proveedor_id FK
        date fecha_compra
        decimal total
        text observaciones
        int usuario_registro_id FK
        datetime fecha_creacion
        datetime fecha_actualizacion
    }

    DetalleEntradaCompra {
        int id PK
        int entrada_compra_id FK
        int producto_id FK
        int cantidad
        decimal precio_unitario
        decimal subtotal
        date fecha_vencimiento
    }

    AjusteInventario {
        int id PK
        int producto_id FK
        varchar tipo_ajuste "ENTRADA, SALIDA"
        varchar motivo
        int cantidad_anterior
        int cantidad_nueva
        int diferencia
        text observaciones
        int usuario_registro_id FK
        datetime fecha_ajuste
        datetime fecha_creacion
    }

    %% ========== MÓDULO VENTAS ==========
    Cliente {
        int id PK
        varchar nombre
        varchar cedula
        varchar telefono
        varchar email
        text direccion
        varchar tipo_cliente "REGULAR, FRECUENTE, MAYORISTA"
        bool activo
        datetime fecha_creacion
        datetime fecha_actualizacion
    }

    Factura {
        int id PK
        varchar numero_factura UK
        int cliente_id FK "nullable"
        varchar cliente_nombre "venta sin cliente"
        int vendedor_id FK
        datetime fecha_venta
        decimal subtotal
        decimal descuento
        decimal total
        varchar estado "PENDIENTE, COMPLETADA, ANULADA"
        text observaciones
        datetime fecha_creacion
        datetime fecha_actualizacion
    }

    DetalleFactura {
        int id PK
        int factura_id FK
        int producto_id FK
        int cantidad
        decimal precio_unitario
        decimal subtotal
    }

    %% ========== MÓDULO CIENCIA DE DATOS ==========
    ProductosRecomendados {
        int id PK
        int producto_base_id FK "nullable"
        int producto_recomendado_id FK
        varchar tipo_recomendacion
        decimal score
        json contexto
        int usuario_id FK "nullable"
        bool mostrado
        bool aceptado
        datetime fecha_recomendacion
        datetime fecha_creacion
    }

    %% ========== RELACIONES ==========
    Rol ||--o{ Usuario : "tiene"
    Usuario ||--o{ Factura : "vende"
    Usuario ||--o{ EntradaCompra : "registra"
    Usuario ||--o{ AjusteInventario : "registra"
    Usuario ||--o{ ProductosRecomendados : "recibe"

    Categoria ||--o{ NombreProducto : "agrupa"
    Categoria ||--o{ Producto : "agrupa"
    NombreProducto ||--o{ Producto : "instancia"

    Proveedor ||--o{ EntradaCompra : "provee"
    EntradaCompra ||--o{ DetalleEntradaCompra : "contiene"
    Producto ||--o{ DetalleEntradaCompra : "detalle"
    Producto ||--o{ AjusteInventario : "ajuste"

    Cliente ||--o{ Factura : "compra"
    Usuario ||--o{ Factura : "vendedor"
    Factura ||--o{ DetalleFactura : "contiene"
    Producto ||--o{ DetalleFactura : "línea"

    Producto ||--o{ ProductosRecomendados : "producto_base"
    Producto ||--o{ ProductosRecomendados : "producto_recomendado"
```

## Resumen de tablas por módulo

| Módulo        | Tablas |
|---------------|--------|
| **usuarios**  | Rol, Usuario |
| **inventario**| Categoria, NombreProducto, Producto, Proveedor, EntradaCompra, DetalleEntradaCompra, AjusteInventario |
| **ventas**    | Cliente, Factura, DetalleFactura |
| **ciencia_datos** | ProductosRecomendados |

## Cardinalidades principales

- **Rol** → **Usuario**: 1:N (un rol tiene muchos usuarios).
- **Usuario** → **Factura**: 1:N (un vendedor tiene muchas facturas).
- **Cliente** → **Factura**: 1:N (un cliente puede tener muchas facturas; factura puede no tener cliente).
- **Factura** → **DetalleFactura**: 1:N (una factura tiene muchas líneas).
- **Producto** → **DetalleFactura**: 1:N (un producto aparece en muchas líneas de factura).
- **Categoria** → **NombreProducto** / **Producto**: 1:N.
- **NombreProducto** → **Producto**: 1:N (varios productos pueden compartir el mismo nombre/catálogo).
- **Proveedor** → **EntradaCompra**: 1:N.
- **EntradaCompra** → **DetalleEntradaCompra**: 1:N.
- **Producto** → **DetalleEntradaCompra**, **AjusteInventario**: 1:N.
- **Producto** → **ProductosRecomendados**: N:M vía producto_base y producto_recomendado.

## Notas

- **Usuario** extiende `AbstractUser` de Django (incluye username, password, first_name, last_name, email, is_staff, is_active, date_joined, etc.).
- **unique_together**: (factura, producto) en DetalleFactura; (entrada_compra, producto) en DetalleEntradaCompra.
- Claves foráneas con `PROTECT` impiden borrar el registro referenciado si hay dependencias; `CASCADE` borra en cascada (ej. detalle al borrar factura).
