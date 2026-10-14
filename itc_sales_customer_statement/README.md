# ITC - Estado de cuenta para vendedores — Odoo 17

Versión 17.0.1.1.1. Consulta automática de cartera usando el campo estándar
**Vendedor** (`res.partner.user_id`) del cliente comercial principal.
No hay que registrar clientes uno por uno ni sincronizar listas.

## Instalar o actualizar en Odoo.sh

1. Copia la carpeta completa `itc_sales_customer_statement` del ZIP a tu
   repositorio, reemplazando los archivos de la versión anterior.
2. Sube los cambios a una rama de pruebas de Odoo.sh y espera la compilación.
3. En Aplicaciones, busca `itc_sales_customer_statement`. Si ya estaba
   instalado, pulsa **Actualizar**, no desinstalar. Si es la primera instalación,
   actualiza la lista de aplicaciones y pulsa Activar.
4. Asigna al vendedor el grupo **Consultar cartera de clientes asignados**, en
   Ajustes → Usuarios y compañías → Usuarios → Consulta de cartera comercial.
   Si no aparece, agrega el usuario desde Grupos en modo desarrollador.
5. En Contactos, abre el cliente principal y comprueba su campo Vendedor en
   Ventas y compras. Debe apuntar al usuario que consultará el reporte.
6. Entra como ese vendedor, selecciona la empresa correspondiente y abre el
   cliente → **Estado de cuenta**.

Los usuarios con el anterior permiso «Consultar cartera autorizada» lo conservan:
se mantiene su identificador y solo cambia el nombre mostrado.
El vendedor del contacto principal es el criterio; no se utiliza el vendedor
de cada factura ni el responsable de cobranza. Si el contacto es hijo, se usa
la asignación de su cliente principal. Un cliente sin vendedor no da acceso.

## Actualización desde 17.0.1.0.1

La lista manual «Cartera comercial → Clientes autorizados» se elimina del menú.
Los datos de esa versión se conservan por compatibilidad, pero **no conceden
acceso y ya no se consultan para el reporte**. El antiguo grupo de administración
también se conserva para actualizar sin perder referencias; no es necesario
asignarlo. No tienes que llenar esa lista ni ejecutar una sincronización.

La actualización no cambia los vendedores que ya tienen tus contactos,
facturas, pagos, conciliaciones ni los permisos contables existentes.
Reasignar el cliente a otro vendedor o dejar el campo vacío revoca el acceso
anterior al recargar el reporte; no retira PDF descargados ni contenido visible.

## Consulta y saldos

Abre una pestaña de consulta actualizada al cargar, con fecha, documento,
vencimiento, días vencidos y saldos. No permite modificar facturas, conciliar,
registrar pagos ni enviar recordatorios. Para PDF, usa **Imprimir / Guardar PDF**
y selecciona Guardar como PDF en el navegador.

Incluye únicamente partidas publicadas, abiertas, en cuentas `asset_receivable`
de una empresa, del cliente principal y sus contactos hijos. Incluye créditos y
pagos/anticipos abiertos en esas cuentas con signo negativo. Una factura con
varios plazos puede aparecer en varios renglones. Las partidas conciliadas,
borradores y anticipos en cuentas de pasivo no se incluyen. Es cartera pendiente,
no un mayor histórico de todos los movimientos.

- Importe de partida: balance contable original de la partida en moneda de empresa.
- Saldo pendiente: residual firmado de la partida en moneda de empresa.
- Saldo moneda documento: residual firmado en la moneda de cada partida.
- Saldo neto: suma de saldos pendientes incluyendo créditos.
- Cargos vencidos: residuales positivos con vencimiento anterior a hoy, sin
  descontar créditos no conciliados; sin vencimiento se utiliza la fecha de partida.

Los totales no mezclan monedas: se expresan en moneda de empresa a valores
contables residuales, sin revaluar al tipo de cambio actual.
El reporte se limita a una empresa permitida al usuario. Los contactos
compartidos pueden consultarse en sus empresas autorizadas; el saldo de otra
empresa no se mezcla. Los contactos con empresa específica se limitan a ella.

## Seguridad y permisos estándar

Cada carga valida sesión, grupo, acceso estándar al contacto, empresa permitida
y vendedor del cliente principal antes de la consulta contable. La consulta usa
elevación de permisos con filtros fijos; no se concede al grupo ninguna ACL de
Contabilidad y solo se muestran los datos previstos en el reporte. Conocer una
URL no permite consultar el cliente de otro vendedor. Los encabezados HTTP
deshabilitan el caché y los datos del cliente se escapan al generar HTML.

**El campo Vendedor y la jerarquía de contactos son ahora la fuente de autorización.**
Quien ya tenga permiso estándar para cambiar ese vendedor o mover contactos
entre clientes podrá afectar qué cartera se consulta. Este módulo no bloquea
esas operaciones estándar ni cambia reglas sobre Contactos; si ese control es
necesario, debe gestionarse con los permisos de asignación de tu base.
No se puede mantener asignación dinámica y afirmar que esos cambios nunca
alteran el acceso. La administración de asignaciones debe quedar en manos
del personal que corresponda según tu operación.

No elimina permisos que un usuario ya tenga por Facturación, Contabilidad,
Ventas u otros módulos. Tampoco restringe el historial ni adjuntos de Contactos.
Un administrador no ve automáticamente la cartera de todos los vendedores
mediante este reporte: para consultarla, debe ser el vendedor asignado.

## Pruebas en staging

El paquete se verificó estáticamente fuera de Odoo; no se ejecutaron las pruebas
incluidas en una base Odoo. Valida antes de producción:

1. Un vendedor con el grupo abre un cliente que ya tiene asignado, sin lista manual.
2. Otro vendedor, un usuario sin grupo y un cliente sin vendedor no obtienen acceso.
3. Reasignar al cliente cambia el acceso al recargar la URL.
4. Clientes hijos nuevos se incluyen automáticamente.
5. Otra empresa sin autorización devuelve acceso denegado.
6. El saldo cuadra con Contabilidad: pago parcial, crédito abierto y varios plazos.
7. Si hay moneda extranjera, compara residuales contables en ambas monedas.
8. La lista manual anterior no aparece y sus autorizaciones no conceden acceso.

Se incluyen nueve pruebas Odoo (ocho de modelo y una HTTP), para accesos,
reasignación, grupos, pagos parciales, contactos hijos y renderizado seguro.
Para ejecutarlas en una base desechable con Odoo 17, ajusta rutas:

```bash
odoo-bin -d base_pruebas --addons-path=/ruta/odoo/addons,/ruta/custom_addons -u itc_sales_customer_statement --test-enable --test-tags /itc_sales_customer_statement --stop-after-init
```

Usa `-i` para instalación inicial. No ejecutes esa orden en producción.

## Quitar y migrar

Desinstala desde Odoo mientras los archivos todavía estén en Git; después
retira la carpeta del repositorio. La desinstalación elimina los elementos
propios y los datos manuales heredados; no borra documentos contables.

Paquete exclusivamente para Odoo 17 Community/Enterprise y Odoo.sh. Depende
de `account` y `web`, sin bibliotecas externas. Para versiones posteriores,
revisa sintaxis de vistas, APIs de acceso, campos contables y pruebas. Cambiar
solo el número de versión no garantiza compatibilidad.

Licencia LGPL-3.0-or-later; consulta LICENSE.

La versión 17.0.1.1.1 no crea un icono en el menú general. Al actualizar elimina los dos menús propios de versiones anteriores; conserva el botón Estado de cuenta en Contactos. Recarga Odoo después de actualizar.
