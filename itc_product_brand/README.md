# ITC - Marcas de Producto | Odoo 17

Versión: **17.0.1.0.1**

## Objetivo
Convertir **Marca** en una dimensión maestra independiente de Categoría de Producto y exponerla en el análisis estándar de facturas para Pivot, Spreadsheet y Dashboards.

## Incluye
- Catálogo `product.brand`
- Campo `Marca` (`brand_id`) en `product.template`
- Búsqueda y Agrupar por Marca en productos
- Campo `brand_id` en `account.invoice.report`
- Filtro y Agrupar por Marca en Análisis de facturas
- Marca disponible como dimensión para Pivot / Spreadsheet / Dashboard

## Instalación Odoo.sh
1. Subir la carpeta `itc_product_brand` directamente a la raíz del repositorio.
2. Hacer commit en la rama de STAGING.
3. Esperar build verde.
4. En Odoo: Apps > Actualizar lista de aplicaciones.
5. Buscar `ITC - Marcas de Producto`.
6. Instalar.
7. Abrir un producto y capturar una Marca.
8. Ir a Facturación > Informes > Análisis de facturas.
9. Validar que aparezca `Marca` como filtro y en Agrupar por.
10. Crear un Pivot de prueba y después insertarlo en Spreadsheet/Dashboard.

## Prueba mínima antes de producción
- Crear 3 marcas.
- Asignarlas a 10-20 productos con facturas históricas.
- Validar agrupación por Marca.
- Validar filtro por Marca.
- Confirmar que Venta, Cantidad y Margen total NO cambian al quitar el agrupamiento.
- Validar notas de crédito/devoluciones.
- Validar multi-compañía si aplica.

## Desinstalación
La desinstalación elimina el catálogo/campo provistos por este módulo. Por tanto, antes de desinstalar una base con datos reales, exportar:
- ID externo o referencia interna del producto
- Producto
- Marca

## Upgrade futuro
No modifica archivos core de Odoo. Usa herencia estándar. La extensión de `account.invoice.report` debe revisarse al migrar de versión porque el SQL del reporte puede cambiar.

## Principio de diseño
**Marca y Categoría son dimensiones distintas.** Este módulo no reemplaza ni modifica las categorías existentes.
