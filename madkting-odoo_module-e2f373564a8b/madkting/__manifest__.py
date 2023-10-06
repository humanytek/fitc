# -*- coding: utf-8 -*-
{
    'name': "Yuju",

    'summary': """
        Integration with Yuju's platform""",

    'description': """
        Module integration with Yuju's software platform.
        - Create orders into your odoo software from marketplaces like Mercado Libre, Amazon, etc..
        - Create products from Yuju platform into odoo
        - Update your stock from odoo to your Yuju account.
    """,

    'author': "Gerardo A Lopez Vega @glopzvega",
    'email': "gerardo.lopez@yuju.io",
    'website': "https://yuju.io/",
    'category': 'Sales',
    'version': '1.2.4',
    'license': 'Other proprietary',

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'sale_management',
        'stock',
        'component_event'
    ],
    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        # 'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
    "cloc_exclude": [
        # "lib/common.py", # exclude a single file
        # "data/*.xml",    # exclude all XML files in a specific folder
        "controllers/**/*",  # exclude all files in a folder hierarchy recursively
        "log/**/*",  # exclude all files in a folder hierarchy recursively
        "models/**/*",  # exclude all files in a folder hierarchy recursively
        "notifier/**/*",  # exclude all files in a folder hierarchy recursively
        "requirements/**/*",  # exclude all files in a folder hierarchy recursively
        "responses/**/*",  # exclude all files in a folder hierarchy recursively
        "security/**/*",  # exclude all files in a folder hierarchy recursively
        "views/**/*",  # exclude all files in a folder hierarchy recursively
    ]
}

# Version 0.0.2
# *** Agrega validacion para buscar rfc cliente antes de crearlo.

# Version 0.0.3
# *** Agrega logs para debug y agrega los campos type y detailed_type en el metodo
#  de validacion de campos en la actualizacion de productos

# Version 0.0.4
# *** Se quitan impuestos por default de la linea de la venta si no se enviaron desde Yuju

# Version 0.0.5
# *** Valida si la orden fue confirmada y no se elimina la orden si no se puede confirmar, se agrega mensaje en el post_message

# Version 0.0.6
# *** Actualiza campos custom facturas

# Version 0.0.7
# *** desindexa productos archivados

# Version 0.0.8
# *** Agrega configuracion para validar barcode

# Version 0.0.9
# *** Agrega configuracion ubicaciones multiples consulta stock

# Version 1.0.0
# *** Agrega validaciones en actualizacion, valida sku y el id de yuju, se agrega configuracion para evitar Ids y SKU duplicados

# Version 1.0.1
# *** Actualiza reglas para validar actualizacion

# Version 1.1.0
# *** Agrega configuracion para cancelar ordenes si tienen movimientos de almacen

# Version 1.1.1
# *** Agrega configuracion para actualizar almacen en linea de la orden

# Version 1.1.2
# *** Agrega valildacion de stock debug

# Version 1.1.3
# *** Modifica funcion obtener stock

# Version 1.1.4
# *** Agrega configuracion obtener stock a la mano o stock disponible

# Version 1.1.5
# *** Actualiza metodo confirmar orden si tiene stock disponible

# Version 1.1.6
# *** Agrega metodo obtener stock

# Version 1.1.7
# *** Agrega metodo enviar webhook manualmente

# Version 1.1.8
# *** Agrega configuracion validar fulfillment para confirmar la orden

# Version 1.1.9
# *** Agrega configuracion quitar impuestos por default

# Version 1.2.0
# *** Actualiza funcionalidad para mapeo de campos y defaults

# Version 1.2.1
# *** Agrega cambio de tipo en mapeo de campos

# Version 1.2.2
# *** Agrega configuracion catalogo compartido de productos en multiempresa

# Version 1.2.3
# *** Agrega configuracion multi empresa

# Version 1.2.4
# *** Fix error on product mapping writing string clears product_id field