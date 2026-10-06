# ITC - Marcas de Producto | Odoo 17

Versión **17.0.1.0.2**

## Corrección v1.0.2
Se elimina la dependencia de `product.group_product_manager`, porque ese External ID no existe en esta instalación de Odoo 17.

El módulo ahora define su propio grupo:
**Administrador de Marcas de Producto**.

Los usuarios internos pueden leer el catálogo. Sólo los usuarios asignados al grupo Administrador de Marcas pueden crear, editar o archivar marcas.

## Instalación
1. Sustituir en GitHub el contenido de `itc_product_brand` por esta versión.
2. Commit a staging.
3. Esperar build verde.
4. Apps > Actualizar lista de aplicaciones.
5. Instalar `ITC - Marcas de Producto`.
6. Asignar al usuario administrador el grupo `Administrador de Marcas de Producto`.
7. Crear marcas y probar Análisis de facturas > Agrupar por > Marca.
