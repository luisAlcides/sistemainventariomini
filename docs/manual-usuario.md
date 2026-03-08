# Manual de Usuario — Sistema Minisúper D'Pérez

Sistema web de gestión para facturación, control de inventario y reportes del **Minisúper D'Pérez**. Este manual describe cómo usar el sistema desde el navegador.

---

## 1. Acceso al sistema

### 1.1 Iniciar sesión

1. Abra el navegador y vaya a la dirección del sistema (por ejemplo: `https://sistemainventariomini-production.up.railway.app/`).
2. Si no está autenticado, será redirigido a **Iniciar sesión**.
3. Ingrese su **Usuario** y **Contraseña**.
4. Pulse **Iniciar sesión**.
5. Si los datos son correctos, entrará al **Dashboard**.

**Nota:** Si aparece "Usuario o contraseña incorrectos", verifique usuario y contraseña. El administrador del sistema puede restablecer contraseñas desde el panel de administración de Django.

### 1.2 Cerrar sesión

- En la barra superior derecha, haga clic en **Salir** para cerrar sesión de forma segura.

### 1.3 Navegación principal

En la barra superior (menú negro) encontrará:

| Opción        | Descripción breve                          |
|---------------|--------------------------------------------|
| **Dashboard** | Resumen general y accesos rápidos          |
| **Facturación** | Listado de facturas y nueva factura      |
| **Inventario**  | Stock, entradas de compra y ajustes      |
| **Catálogos**   | Productos, clientes, categorías, etc.    |
| **Reportes**    | Ventas, productos, clientes, gráficos    |
| **Configuración** | Información del sistema y usuarios       |

En móvil, el menú se muestra colapsado; ábralo con el ícono de menú si está disponible.

---

## 2. Dashboard

El **Dashboard** es la pantalla principal después de iniciar sesión.

### 2.1 Tarjetas de resumen

- **Ventas del día:** Total vendido hoy en C$ (córdobas). Enlace a Facturación.
- **Productos por agotarse:** Cantidad de productos con stock por debajo del mínimo. Enlace a la lista.
- **Total productos:** Cantidad de productos en inventario. Enlace a Inventario.
- **Clientes:** Cantidad de clientes registrados. Enlace a Catálogos → Clientes.
- **Por expirar (30d):** Productos que vencen en los próximos 30 días.
- **Tendencia de ventas:** Indicador alcista, bajista o estable según el análisis del sistema.

### 2.2 Acciones rápidas

- **Nueva Factura:** Ir directo a crear una factura.
- **Registrar Entrada de Compra:** Ir a registrar una compra a proveedor.
- **Agregar Producto:** Ir a Catálogos para dar de alta un producto nuevo.

### 2.3 Últimas facturas

Se muestran las facturas más recientes (número, cliente y total). Desde ahí puede ir a **Ver todas las facturas** para listar y filtrar.

---

## 3. Facturación

### 3.1 Listado de facturas

- Ruta: menú **Facturación** (o desde Dashboard → Ver detalles de Ventas del día).

**Filtros:**

- **Buscar:** Por número de factura o nombre de cliente.
- **Estado:** Todos, Completada, Pendiente, Anulada.

Luego pulse **Buscar**. La tabla muestra: Número, Cliente, Fecha, Total, Estado y **Ver** para abrir el detalle.

### 3.2 Nueva factura

1. En Facturación, pulse **Nueva Factura** (o use la acción rápida del Dashboard).
2. **Información de la factura:**
   - **Número de factura:** Lo asigna el sistema (solo lectura).
   - **Cliente registrado (opcional):** Si el cliente está en Catálogos, selecciónelo en el desplegable (puede buscar por nombre).
   - **Nombre del cliente:** Si no elige cliente registrado, escriba aquí el nombre (ej. "Cliente general").
   - **Descuento (C$):** Monto en córdobas a descontar del total.
   - **Observaciones:** Opcional.
3. **Agregar productos:**
   - Busque y seleccione el producto (por código o nombre).
   - Indique la **cantidad**.
   - El sistema muestra precio unitario y subtotal; puede modificar el precio si está permitido.
   - Pulse el botón para **Agregar** el ítem a la factura.
   - Repita para todos los productos. Puede quitar líneas si hay botón de eliminar.
4. **Resumen y pago:**
   - Se actualizan automáticamente **Subtotal**, **Descuento** y **Total a pagar**.
   - **Método de pago:** Efectivo o Transferencia.
   - **Efectivo:** Ingrese "Pagó con (C$)" y el sistema calcula el **Cambio (vuelto)**.
   - **Transferencia:** Solo confirme; no se pide monto en pantalla.
5. Pulse **Guardar factura** (o el botón equivalente). Si la factura se completa correctamente:
   - El **stock** se descuenta automáticamente por cada producto vendido.
   - Puede ver el mensaje de éxito y, según diseño, redirección al detalle o listado.

**Importante:** Debe haber al menos un producto en la factura y stock suficiente; si no, el sistema mostrará error y no guardará.

### 3.3 Ver detalle de una factura

- En el listado de facturas, pulse **Ver** en la fila deseada.
- Se muestra número, cliente, fecha, subtotal, descuento, total, estado y el detalle de productos (cantidad, precio, subtotal por línea).

### 3.4 Anular una factura

- Desde el **detalle** de la factura, si el estado lo permite, aparece la opción **Anular factura**.
- Confirme la anulación. El sistema:
  - Cambia el estado de la factura a **Anulada**.
  - **Restaura el stock** de los productos que estaban en esa factura.

Solo pueden anularse facturas en estado permitido (por ejemplo Pendiente o según configuración); las ya anuladas no se pueden volver a activar desde esta pantalla.

---

## 4. Inventario

### 4.1 Página principal de inventario

- Ruta: menú **Inventario**.

Ahí se ve:

- **Total productos**, **Por agotarse**, **Por expirar** y botón **Nueva Entrada**.
- Tablas de **Productos por agotarse** y **Productos próximos a expirar** (si los hay), con enlaces a listados completos.
- Enlaces: **Ver Productos** y **Entradas de Compra**.

### 4.2 Lista de productos (inventario)

- Desde Inventario → **Ver Productos**.
- Listado de productos con información de stock y precios. Puede buscar/filtrar si la pantalla lo permite.
- **Ver detalle** de un producto: stock actual, mínimo, fechas, movimientos recientes.
- **Editar:** Modificar datos del producto (precios, stock mínimo, etc.) según permisos.

### 4.3 Productos por agotarse / por expirar

- **Por agotarse:** Productos con stock actual menor o igual al stock mínimo. Enlaces desde Dashboard e Inventario.
- **Por expirar:** Productos con fecha de vencimiento próxima. Enlaces desde Dashboard e Inventario.

Use estos reportes para reordenar o dar salida a productos antes de que venzan.

### 4.4 Entradas de compra

Registrar compras a proveedores para que el sistema **aumente el stock** automáticamente.

1. Inventario → **Entradas de Compra** → **Nueva Entrada** (o botón "Nueva Entrada" en la portada de Inventario).
2. Complete:
   - **Proveedor** (debe estar dado de alta en Catálogos).
   - **Número de factura** del proveedor (opcional).
   - **Fecha de compra**.
   - **Observaciones** (opcional).
3. Agregue **detalles:** producto, cantidad, precio unitario, fecha de vencimiento (si aplica).
4. Guarde. El sistema actualiza el stock de cada producto y queda registrada la entrada.

Desde **Entradas** puede ver el listado y el **detalle** de cada entrada (proveedor, fecha, total, ítems).

### 4.5 Ajustes de inventario

Para correcciones manuales de stock (entrada o salida por mermas, conteos, etc.):

1. Inventario → **Ajustes** → **Nuevo ajuste** (o ruta equivalente).
2. Seleccione el **producto**, **tipo** (Entrada o Salida), **cantidad** y **motivo/observaciones**.
3. Guarde. El sistema registra el ajuste y actualiza el stock.

Listado de ajustes en **Inventario → Ajustes**.

---

## 5. Catálogos

Desde el menú **Catálogos** se gestionan los datos maestros. La portada muestra tarjetas con totales y enlaces a cada subcatálogo.

### 5.1 Nombres de productos

- Catálogo maestro de “nombres” de productos (ej. “Arroz”, “Aceite”).  
- Desde aquí se crean y editan nombres que luego se usan al crear **Productos** (ítems con código, precio y stock).

### 5.2 Productos

- Alta y edición de **productos** con: código, nombre (o nombre de producto), categoría, precios (venta/compra), stock actual, stock mínimo, unidad, fecha de expiración, etc.
- Listado y **detalle** por producto. Los productos activos son los que se pueden vender y aparecen en entradas y ajustes.

### 5.3 Categorías

- Crear y editar **categorías** (ej. Abarrotes, Lácteos). Se usan para organizar productos y en reportes.

### 5.4 Proveedores

- Alta y edición de **proveedores** (nombre, RUC, contacto, teléfono, dirección, etc.). Necesarios para registrar **Entradas de compra**.

### 5.5 Clientes

- Alta y edición de **clientes** (nombre, cédula, teléfono, dirección, tipo: Regular, Frecuente, Mayorista).  
- Al crear una factura puede elegir un cliente registrado o escribir solo el nombre.

---

## 6. Reportes

Menú **Reportes** reúne reportes y análisis.

### 6.1 Resumen en la portada

- Ventas de hoy y del mes.
- Productos por agotarse.
- Valor total del inventario.

### 6.2 Reportes de ventas

- **Ventas del día:** Detalle de ventas del día actual.
- **Ventas por rango:** Ventas entre dos fechas.
- **Tendencia de ventas:** Análisis de tendencia (alcista/bajista/estable).

### 6.3 Reportes de productos

- **Por agotarse:** Listado de productos bajo stock mínimo.
- **Predicción desabastecimiento:** Análisis de riesgo de quedar sin stock.
- **Más vendidos:** Productos más vendidos en el período.
- **Productos complementarios:** Productos que suelen comprarse juntos (análisis).
- **Valor de inventario:** Valor total del stock (costo/valorización).

### 6.4 Reportes de clientes

- **Clientes frecuentes:** Clientes con más compras o mayor valor.

### 6.5 Gráficos

- **Ver gráficos:** Ventas por día, productos más vendidos, ventas por categoría u otros según implementación.

En cada reporte suele haber filtros (fechas, categoría, etc.); use **Buscar** o **Generar** según la pantalla.

---

## 7. Configuración

- Menú **Configuración**.
- Muestra **Información del sistema:** total de usuarios y roles activos.
- La creación y edición de usuarios y roles se realiza desde el **panel de administración de Django** (`/admin/`), al que solo accede personal autorizado (por ejemplo, Administrador).

---

## 8. Moneda y convenciones

- **Moneda:** Córdobas nicaragüenses (**C$**). Todos los montos de venta, descuentos y totales están en C$.
- **Estados de factura:** **Pendiente**, **Completada**, **Anulada**. Solo ciertos estados permiten anulación y restauración de stock.
- **Stock:** Se descuenta al **completar** una factura y se restaura al **anular** la factura. Las **entradas de compra** y los **ajustes** modifican el stock según el tipo (entrada/salida).

---

## 9. Resolución de problemas frecuentes

| Situación | Qué hacer |
|-----------|------------|
| No puedo iniciar sesión | Verificar usuario y contraseña. Si persiste, contactar al administrador. |
| "Debe agregar al menos un producto" | En nueva factura, agregar al menos una línea con producto y cantidad antes de guardar. |
| No hay stock suficiente | Revisar en Inventario el stock del producto. Registrar entrada de compra o ajuste de entrada, o reducir la cantidad en la factura. |
| No aparece un producto al facturar | Comprobar en Catálogos que el producto exista y esté **activo**. |
| No puedo elegir un proveedor en entrada | Dar de alta el proveedor en Catálogos → Proveedores. |
| No encuentro una factura | En Facturación, usar el buscador por número o cliente y el filtro por estado. |

---

## 10. Resumen de roles (referencia)

El sistema contempla roles como **Administrador**, **Vendedor** y **Bodeguero**. El acceso a las pantallas descritas en este manual requiere **iniciar sesión**. Las restricciones específicas por rol (si las hay) las define el administrador; en caso de no poder acceder a alguna opción, contacte al responsable del sistema.

---

*Manual de usuario — Sistema Minisúper D'Pérez. Actualizado para la versión actual del sistema.*
